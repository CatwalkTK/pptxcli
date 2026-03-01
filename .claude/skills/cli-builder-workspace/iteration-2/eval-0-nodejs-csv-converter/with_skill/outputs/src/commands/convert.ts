import { resolve } from 'path';
import { convertCsvToJson } from '../lib/converter.js';
import { createProgressBar, showConversionSummary } from '../ui/progress.js';
import { theme } from '../ui/theme.js';
import type { ConvertOptions } from '../types.js';

type ConvertCommandOptions = {
  readonly output?: string;
  readonly delimiter: string;
  readonly pretty: boolean;
  readonly noHeader: boolean;
  readonly encoding: BufferEncoding;
};

export const runConvert = async (
  inputFile: string,
  opts: ConvertCommandOptions,
): Promise<void> => {
  const inputPath = resolve(inputFile);

  console.log(`  ${theme.dim('Input:')}  ${theme.bold(inputPath)}`);
  if (opts.output) {
    console.log(`  ${theme.dim('Output:')} ${theme.bold(resolve(opts.output))}`);
  }
  console.log();

  const convertOptions: ConvertOptions = {
    input: inputFile,
    output: opts.output,
    delimiter: opts.delimiter,
    pretty: opts.pretty,
    noHeader: opts.noHeader,
    encoding: opts.encoding,
  };

  let progressBar: ReturnType<typeof createProgressBar> | null = null;
  let progressInitialized = false;

  const result = await convertCsvToJson(convertOptions, (current, total) => {
    if (!progressInitialized && total > 0) {
      progressBar = createProgressBar({ total, label: 'Converting' });
      progressInitialized = true;
    }
    if (progressBar) {
      progressBar.update(current);
    }
  });

  if (progressBar) {
    progressBar.stop();
  }

  showConversionSummary(
    inputPath,
    result.outputPath,
    result.rowCount,
    result.durationMs,
  );
};
