import cliProgress from 'cli-progress';
import chalk from 'chalk';
import { theme } from './theme.js';

type ProgressOptions = {
  total: number;
  label?: string;
};

export const createProgressBar = ({ total, label = 'Converting' }: ProgressOptions): cliProgress.SingleBar => {
  const bar = new cliProgress.SingleBar({
    format: `  ${theme.primary(label)} ${chalk.cyan('{bar}')} {percentage}% | {value}/{total} rows | ETA: {eta}s`,
    barCompleteChar: '\u2588',
    barIncompleteChar: '\u2591',
    hideCursor: true,
    clearOnComplete: false,
    barsize: 30,
  });

  bar.start(total, 0);
  return bar;
};

export const showConversionSummary = (
  inputFile: string,
  outputFile: string,
  rowCount: number,
  durationMs: number,
): void => {
  console.log();
  console.log(theme.success('  Conversion complete!'));
  console.log();
  console.log(`  ${theme.dim('Input:')}    ${theme.bold(inputFile)}`);
  console.log(`  ${theme.dim('Output:')}   ${theme.bold(outputFile)}`);
  console.log(`  ${theme.dim('Rows:')}     ${theme.bold(String(rowCount))}`);
  console.log(`  ${theme.dim('Time:')}     ${theme.bold(`${durationMs}ms`)}`);
  console.log();
};
