import chalk, { type ChalkInstance } from 'chalk';

type Theme = {
  readonly primary: ChalkInstance;
  readonly secondary: ChalkInstance;
  readonly success: ChalkInstance;
  readonly warning: ChalkInstance;
  readonly error: ChalkInstance;
  readonly info: ChalkInstance;
  readonly dim: ChalkInstance;
  readonly bold: ChalkInstance;
  readonly heading: ChalkInstance;
  readonly code: ChalkInstance;
  readonly accent: ChalkInstance;
};

export const theme: Theme = {
  primary: chalk.cyan,
  secondary: chalk.magenta,
  success: chalk.green,
  warning: chalk.yellow,
  error: chalk.red,
  info: chalk.blue,
  dim: chalk.dim,
  bold: chalk.bold,
  heading: chalk.cyan.bold.underline,
  code: chalk.gray,
  accent: chalk.hex('#FF6B6B'),
};

export const colorize = (fn: ChalkInstance, text: string): string =>
  process.env.NO_COLOR ? text : fn(text);
