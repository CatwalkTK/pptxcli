import chalk from 'chalk';

export const displayBanner = (): void => {
  const banner = `
${chalk.cyan.bold('  ██████ ███████ ██    ██ ██████      ██ ███████  ██████  ███    ██')}
${chalk.cyan.bold(' ██      ██      ██    ██      ██     ██ ██      ██    ██ ████   ██')}
${chalk.cyan.bold(' ██      ███████ ██    ██  █████      ██ ███████ ██    ██ ██ ██  ██')}
${chalk.cyan.bold(' ██           ██  ██  ██  ██     ██   ██      ██ ██    ██ ██  ██ ██')}
${chalk.cyan.bold('  ██████ ███████   ████   ███████  █████  ███████  ██████  ██   ████')}

${chalk.gray('  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')}
${chalk.white.bold('  CSV to JSON Converter')} ${chalk.gray('v1.0.0')}
${chalk.gray('  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')}
`;

  console.log(banner);
};
