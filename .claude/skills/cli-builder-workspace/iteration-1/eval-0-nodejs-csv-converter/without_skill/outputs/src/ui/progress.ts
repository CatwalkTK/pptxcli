import cliProgress from 'cli-progress';
import chalk from 'chalk';

export type ProgressBar = cliProgress.SingleBar;

export const createProgressBar = (): ProgressBar => {
  const bar = new cliProgress.SingleBar(
    {
      format:
        chalk.cyan('  Converting ') +
        chalk.white('{bar}') +
        chalk.cyan(' {percentage}%') +
        chalk.gray(' | {value}/{total} rows | ETA: {eta}s'),
      barCompleteChar: '\u2588',
      barIncompleteChar: '\u2591',
      hideCursor: true,
      clearOnComplete: false,
      stopOnComplete: true,
    },
    cliProgress.Presets.shades_classic,
  );

  return bar;
};

export const showSpinner = (message: string): { stop: (finalMessage: string) => void } => {
  const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
  let frameIndex = 0;

  const interval = setInterval(() => {
    process.stdout.write(
      `\r  ${chalk.cyan(frames[frameIndex])} ${chalk.white(message)}`,
    );
    frameIndex = (frameIndex + 1) % frames.length;
  }, 80);

  return {
    stop: (finalMessage: string): void => {
      clearInterval(interval);
      process.stdout.write(`\r  ${chalk.green('✓')} ${chalk.white(finalMessage)}\n`);
    },
  };
};
