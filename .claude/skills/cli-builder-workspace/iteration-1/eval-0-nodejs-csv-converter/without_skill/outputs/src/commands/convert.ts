import { resolve } from 'path';
import chalk from 'chalk';
import { ConvertOptions } from '../types';
import { parseCsvFile, getFileSize } from '../services/csv-parser';
import { writeJsonFile } from '../services/json-writer';
import { validateInputFile, validateDelimiter } from '../utils/validate';
import { formatFileSize, formatDuration, resolveOutputPath } from '../utils/format';
import { showSpinner } from '../ui/progress';

export const convertCommand = async (
  input: string,
  options: ConvertOptions,
): Promise<void> => {
  const startTime = Date.now();

  try {
    const inputPath = resolve(input);

    // Validate inputs
    validateInputFile(inputPath);
    validateDelimiter(options.delimiter);

    const inputSize = getFileSize(inputPath);
    const outputPath = resolve(resolveOutputPath(inputPath, options.output));

    console.log(chalk.white('  Input:     ') + chalk.yellow(inputPath));
    console.log(chalk.white('  Output:    ') + chalk.yellow(outputPath));
    console.log(chalk.white('  Delimiter: ') + chalk.yellow(`"${options.delimiter}"`));
    console.log(chalk.white('  File size: ') + chalk.yellow(formatFileSize(inputSize)));
    console.log();

    // Parse CSV
    const rows = await parseCsvFile(inputPath, {
      delimiter: options.delimiter,
      useHeader: options.header !== false,
    });

    console.log();

    // Write JSON
    const spinner = showSpinner('Writing JSON file...');
    const outputSize = writeJsonFile(outputPath, rows, {
      pretty: options.pretty,
    });
    spinner.stop('JSON file written successfully');

    // Summary
    const duration = Date.now() - startTime;

    console.log();
    console.log(chalk.gray('  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'));
    console.log(chalk.green.bold('  Conversion Complete!'));
    console.log(chalk.gray('  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'));
    console.log(chalk.white('  Rows converted: ') + chalk.cyan(rows.length.toLocaleString()));
    console.log(chalk.white('  Output size:    ') + chalk.cyan(formatFileSize(outputSize)));
    console.log(chalk.white('  Time elapsed:   ') + chalk.cyan(formatDuration(duration)));
    console.log(chalk.white('  Output file:    ') + chalk.cyan(outputPath));
    console.log();
  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : String(err);
    console.error();
    console.error(chalk.red.bold('  Error: ') + chalk.red(errorMessage));
    console.error();
    process.exit(1);
  }
};
