import chalk from 'chalk';

const BANNER = `
  ██████ ███████ ██    ██ ██████       ██ ███████  ██████  ███    ██
 ██      ██      ██    ██      ██      ██ ██      ██    ██ ████   ██
 ██      ███████ ██    ██  █████       ██ ███████ ██    ██ ██ ██  ██
 ██           ██  ██  ██  ██     ██    ██      ██ ██    ██ ██  ██ ██
  ██████ ███████   ████   ███████  █████  ███████  ██████  ██   ████
`;

const TAGLINE = '  CSV to JSON Converter CLI  v1.0.0';
const SEPARATOR = '  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';

export const showBanner = (): void => {
  console.log(chalk.cyan.bold(BANNER));
  console.log(chalk.gray(SEPARATOR));
  console.log(chalk.yellow.bold(TAGLINE));
  console.log(chalk.gray(SEPARATOR));
  console.log();
};
