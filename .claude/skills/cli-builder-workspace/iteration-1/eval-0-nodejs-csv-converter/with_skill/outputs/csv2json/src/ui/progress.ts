import cliProgress from 'cli-progress';
import chalk from 'chalk';
import { theme } from './theme.js';

type ProgressBarOptions = {
  readonly total: number;
  readonly label?: string;
};

export const createProgressBar = ({ total, label = 'Converting' }: ProgressBarOptions): cliProgress.SingleBar => {
  const bar = new cliProgress.SingleBar({
    format: `  ${theme.primary('{bar}')} ${chalk.dim('|')} ${theme.bold('{percentage}%')} ${chalk.dim('|')} ${theme.dim('{value}/{total} rows')} ${chalk.dim('|')} ${theme.accent(label)}`,
    barCompleteChar: '\u2588',
    barIncompleteChar: '\u2591',
    hideCursor: true,
    barsize: 30,
    stopOnComplete: true,
    clearOnComplete: false,
  });

  bar.start(total, 0);
  return bar;
};

export const showConversionSummary = (stats: {
  readonly inputFile: string;
  readonly outputFile: string;
  readonly rowCount: number;
  readonly durationMs: number;
  readonly inputSizeBytes: number;
  readonly outputSizeBytes: number;
}): void => {
  console.log();
  console.log(theme.success('  ✔ Conversion complete!'));
  console.log();
  console.log(`  ${theme.dim('Input:')}    ${theme.bold(stats.inputFile)}`);
  console.log(`  ${theme.dim('Output:')}   ${theme.bold(stats.outputFile)}`);
  console.log(`  ${theme.dim('Rows:')}     ${theme.primary(String(stats.rowCount))}`);
  console.log(`  ${theme.dim('Size:')}     ${formatBytes(stats.inputSizeBytes)} ${theme.dim('->')} ${formatBytes(stats.outputSizeBytes)}`);
  console.log(`  ${theme.dim('Duration:')} ${theme.primary(`${stats.durationMs}ms`)}`);
  console.log();
};

const formatBytes = (bytes: number): string => {
  if (bytes === 0) return theme.dim('0 B');
  const units = ['B', 'KB', 'MB', 'GB'] as const;
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  const value = (bytes / Math.pow(1024, i)).toFixed(1);
  return theme.primary(`${value} ${units[i]}`);
};
