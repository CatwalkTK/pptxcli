import * as fs from 'fs';
import * as path from 'path';
import { parse } from 'csv-parse';
import chalk from 'chalk';
import ora from 'ora';

type CsvRecord = Record<string, string>;

interface ConvertOptions {
  readonly output?: string;
  readonly pretty?: boolean;
  readonly delimiter?: string;
}

interface ConvertResult {
  readonly inputPath: string;
  readonly outputPath: string;
  readonly recordCount: number;
  readonly durationMs: number;
}

const resolveOutputPath = (inputPath: string, outputOption?: string): string => {
  if (outputOption) {
    const outputDir = path.dirname(outputOption);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    return path.resolve(outputOption);
  }

  const parsed = path.parse(inputPath);
  return path.resolve(parsed.dir, `${parsed.name}.json`);
};

const validateInputFile = (filePath: string): string => {
  const resolvedPath = path.resolve(filePath);

  if (!fs.existsSync(resolvedPath)) {
    throw new Error(`Input file not found: ${resolvedPath}`);
  }

  const ext = path.extname(resolvedPath).toLowerCase();
  if (ext !== '.csv') {
    throw new Error(`Expected a .csv file, but got: ${ext}`);
  }

  return resolvedPath;
};

const parseCsvFile = (filePath: string, delimiter: string): Promise<CsvRecord[]> => {
  return new Promise((resolve, reject) => {
    const records: CsvRecord[] = [];
    const fileStream = fs.createReadStream(filePath, { encoding: 'utf-8' });

    const parser = parse({
      columns: true,
      skip_empty_lines: true,
      trim: true,
      delimiter,
      bom: true,
    });

    fileStream
      .pipe(parser)
      .on('data', (record: CsvRecord) => {
        records.push(record);
      })
      .on('end', () => {
        resolve(records);
      })
      .on('error', (err: Error) => {
        reject(new Error(`Failed to parse CSV: ${err.message}`));
      });
  });
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

export const convertCsvToJson = async (
  inputPath: string,
  options: ConvertOptions,
): Promise<ConvertResult> => {
  const startTime = Date.now();

  // Validate input
  const resolvedInput = validateInputFile(inputPath);
  const outputPath = resolveOutputPath(resolvedInput, options.output);

  const inputStats = fs.statSync(resolvedInput);
  console.log(chalk.blue('  Input:  ') + chalk.white(resolvedInput));
  console.log(chalk.blue('  Size:   ') + chalk.white(formatFileSize(inputStats.size)));
  console.log(chalk.blue('  Output: ') + chalk.white(outputPath));
  console.log();

  // Parse CSV with spinner
  const parseSpinner = ora({
    text: chalk.cyan('Reading and parsing CSV file...'),
    prefixText: ' ',
    spinner: 'dots',
  }).start();

  const records = await parseCsvFile(resolvedInput, options.delimiter ?? ',');

  parseSpinner.succeed(
    chalk.green(`Parsed ${chalk.bold(records.length.toString())} records successfully`),
  );

  // Show column info
  if (records.length > 0) {
    const columns = Object.keys(records[0]);
    console.log(
      chalk.gray(`   Columns: ${columns.map((c) => chalk.white(c)).join(', ')}`),
    );
  }

  // Convert to JSON with spinner
  const writeSpinner = ora({
    text: chalk.cyan('Converting to JSON and writing file...'),
    prefixText: ' ',
    spinner: 'dots',
  }).start();

  const indent = options.pretty !== false ? 2 : 0;
  const jsonContent = JSON.stringify(records, null, indent);

  fs.writeFileSync(outputPath, jsonContent, { encoding: 'utf-8' });

  const outputStats = fs.statSync(outputPath);
  writeSpinner.succeed(
    chalk.green(
      `JSON file written (${chalk.bold(formatFileSize(outputStats.size))})`,
    ),
  );

  const durationMs = Date.now() - startTime;

  // Summary
  console.log();
  console.log(chalk.gray('  ─────────────────────────────────────'));
  console.log(chalk.green.bold('  Conversion complete!'));
  console.log(chalk.gray(`  Records: ${chalk.white(records.length.toString())}`));
  console.log(chalk.gray(`  Time:    ${chalk.white(`${durationMs}ms`)}`));
  console.log(chalk.gray(`  Output:  ${chalk.white(outputPath)}`));
  console.log();

  return {
    inputPath: resolvedInput,
    outputPath,
    recordCount: records.length,
    durationMs,
  };
};
