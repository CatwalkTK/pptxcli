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
  readonly taskId: ChalkInstance;
  readonly pending: ChalkInstance;
  readonly done: ChalkInstance;
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
  taskId: chalk.yellow.bold,
  pending: chalk.yellow,
  done: chalk.green,
};

export const icons = {
  pending: chalk.yellow('○'),
  done: chalk.green('●'),
  add: chalk.green('+'),
  check: chalk.green('✔'),
  cross: chalk.red('✖'),
  arrow: chalk.cyan('▸'),
  bar: chalk.dim('│'),
  divider: chalk.dim('─'.repeat(50)),
} as const;

export const colorize = (fn: ChalkInstance, text: string): string =>
  process.env.NO_COLOR ? text : fn(text);
