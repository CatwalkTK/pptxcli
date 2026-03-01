import { access, constants } from 'fs/promises';
import { resolve } from 'path';
import { convertCsvToJson } from '../lib/converter.js';
import { FileNotFoundError } from '../lib/errors.js';
import { createProgressBar, showConversionSummary } from '../ui/progress.js';
import { theme } from '../ui/theme.js';
import type { ConvertOptions } from '../types.js';

/**
 * Handler for the `convert` command.
 *
 * Bridges the Business Logic layer and the Presentation Layer:
 * - Validates inputs
 * - Calls converter with a progress callback
 * - Displays summary using the UI module
 */
export const runConvert = async (inputFile: string, opts: ConvertOptions): Promise<void> => {
  // 1. Validate input file exists
  const inputPath = resolve(inputFile);
  try {
    await access(inputPath, constants.R_OK);
  } catch {
    throw new FileNotFoundError(inputPath);
  }

  // 2. Show status
  console.log(`  ${theme.dim('Input:')}  ${theme.bold(inputPath)}`);
  if (opts.output) {
    console.log(`  ${theme.dim('Output:')} ${theme.bold(resolve(opts.output))}`);
  }
  console.log();

  // 3. Read file to get row count for progress bar
  const { readFile } = await import('fs/promises');
  const rawContent = await readFile(inputPath, 'utf-8');
  const lineCount = rawContent.split('\n').filter((line) => line.trim().length > 0).length;
  const dataRowCount = Math.max(0, lineCount - (opts.noHeader ? 0 : 1));

  // 4. Create progress bar
  const progressBar = createProgressBar({
    total: dataRowCount,
    label: 'Converting',
  });

  // 5. Run conversion with progress callback
  const result = await convertCsvToJson(
    { ...opts, input: inputFile },
    (current: number, _total: number) => {
      progressBar.update(current);
    },
  );

  // Ensure bar reaches 100%
  progressBar.update(dataRowCount);
  progressBar.stop();

  // 6. Show summary
  showConversionSummary({
    inputFile: inputPath,
    outputFile: result.outputPath,
    rowCount: result.rowCount,
    durationMs: result.durationMs,
    inputSizeBytes: result.inputSizeBytes,
    outputSizeBytes: result.outputSizeBytes,
  });

  // 7. Optional: show preview in verbose mode
  if (opts.verbose && result.records.length > 0) {
    console.log(theme.heading('  Preview (first 3 rows):'));
    console.log();
    const preview = result.records.slice(0, 3);
    for (const record of preview) {
      console.log(theme.code(`  ${JSON.stringify(record)}`));
    }
    console.log();
  }
};
