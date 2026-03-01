import { readFile, writeFile } from 'fs/promises';
import { resolve, basename, dirname } from 'path';
import { existsSync } from 'fs';
import { parseCsvContent, countLines } from './csv-parser.js';
import { CliError } from './errors.js';
import type { ConvertOptions, ConvertResult, CsvRow } from '../types.js';

const resolveOutputPath = (inputPath: string, outputOption?: string): string => {
  if (outputOption) {
    return resolve(outputOption);
  }
  const inputBasename = basename(inputPath, '.csv');
  const inputDir = dirname(resolve(inputPath));
  return resolve(inputDir, `${inputBasename}.json`);
};

export const convertCsvToJson = async (
  options: ConvertOptions,
  onProgress?: (current: number, total: number) => void,
): Promise<ConvertResult> => {
  const startTime = Date.now();
  const inputPath = resolve(options.input);

  if (!existsSync(inputPath)) {
    throw new CliError(
      `Input file not found: ${inputPath}`,
      1,
      'Check the file path and try again',
    );
  }

  const content = await readFile(inputPath, { encoding: options.encoding });

  if (content.trim().length === 0) {
    throw new CliError(
      'Input file is empty',
      1,
      'Provide a CSV file with at least one row of data',
    );
  }

  const totalLines = countLines(content);

  const { rows } = parseCsvContent(content, {
    delimiter: options.delimiter,
    hasHeader: !options.noHeader,
    encoding: options.encoding,
  });

  const processedRows: CsvRow[] = [];
  for (const [index, row] of rows.entries()) {
    processedRows.push(row);
    if (onProgress) {
      onProgress(index + 1, totalLines);
    }
  }

  const outputPath = resolveOutputPath(inputPath, options.output);
  const indent = options.pretty ? 2 : undefined;
  const jsonContent = JSON.stringify(processedRows, null, indent);

  await writeFile(outputPath, jsonContent, 'utf-8');

  const durationMs = Date.now() - startTime;

  return {
    rowCount: processedRows.length,
    outputPath,
    durationMs,
  };
};
