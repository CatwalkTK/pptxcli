import { readFile, writeFile, stat } from 'fs/promises';
import { resolve, basename, dirname } from 'path';
import { parseCsv, toRecords } from './csv-parser.js';
import type { ConvertOptions, ConvertResult } from '../types.js';

/**
 * Core conversion logic: read CSV, parse, convert, write JSON.
 * I/O + business logic -- no UI imports.
 *
 * Returns a ConvertResult with all metadata needed by the UI layer
 * to display progress and summary.
 *
 * @param options  The convert command options
 * @param onProgress  Optional callback invoked for each row (for progress bars)
 */
export const convertCsvToJson = async (
  options: ConvertOptions,
  onProgress?: (current: number, total: number) => void,
): Promise<ConvertResult> => {
  const startTime = Date.now();

  // 1. Resolve paths
  const inputPath = resolve(options.input);
  const outputPath = resolveOutputPath(inputPath, options.output);

  // 2. Read input file
  const rawCsv = await readFile(inputPath, 'utf-8');
  const inputStats = await stat(inputPath);

  // 3. Parse CSV
  const parsed = parseCsv(rawCsv, {
    delimiter: options.delimiter ?? ',',
    hasHeader: !(options.noHeader ?? false),
    trimValues: true,
    skipEmptyLines: true,
  });

  // 4. Convert to records with progress
  const records = toRecords(parsed);
  const total = records.length;

  if (onProgress) {
    for (let i = 0; i < total; i++) {
      onProgress(i + 1, total);
      // Yield to event loop periodically for progress bar rendering
      if (i % 100 === 0) {
        await new Promise((resolve) => setTimeout(resolve, 0));
      }
    }
  }

  // 5. Serialize to JSON
  const indent = (options.pretty ?? true) ? 2 : undefined;
  const jsonOutput = options.array
    ? JSON.stringify(records, null, indent)
    : JSON.stringify(records, null, indent);
  const outputBuffer = Buffer.from(jsonOutput, 'utf-8');

  // 6. Write output file
  await writeFile(outputPath, jsonOutput, 'utf-8');

  const durationMs = Date.now() - startTime;

  return {
    records,
    rowCount: total,
    headers: [...parsed.headers],
    outputPath,
    inputSizeBytes: inputStats.size,
    outputSizeBytes: outputBuffer.byteLength,
    durationMs,
  };
};

/**
 * Determine the output file path.
 * If --output is provided, use it. Otherwise, replace .csv with .json
 * in the same directory as the input file.
 */
const resolveOutputPath = (inputPath: string, output?: string): string => {
  if (output) {
    return resolve(output);
  }
  const dir = dirname(inputPath);
  const name = basename(inputPath, '.csv');
  return resolve(dir, `${name}.json`);
};
