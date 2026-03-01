#!/usr/bin/env node
import { Command } from 'commander';
import { showBanner } from './ui/banner.js';
import { theme } from './ui/theme.js';
import { CliError } from './lib/errors.js';

const VERSION = '1.0.0';
const NAME = 'csv2json';

const program = new Command()
  .name(NAME)
  .version(VERSION)
  .description('Convert CSV files to JSON format with style')
  .hook('preAction', () => {
    showBanner({
      name: 'csv2json',
      version: VERSION,
      tagline: 'Fast & elegant CSV to JSON conversion',
      font: 'ANSI Shadow',
    });
  });

program
  .command('convert')
  .description('Convert a CSV file to JSON')
  .argument('<input>', 'path to the CSV file to convert')
  .option('-o, --output <path>', 'output file path (default: same name with .json extension)')
  .option('-d, --delimiter <char>', 'CSV delimiter character', ',')
  .option('-p, --pretty', 'pretty-print the JSON output', true)
  .option('--no-pretty', 'minify the JSON output')
  .option('--no-header', 'treat the first row as data, not headers')
  .option('-e, --encoding <encoding>', 'file encoding', 'utf-8')
  .addHelpText('after', `
Examples:
  $ csv2json convert data.csv
  $ csv2json convert data.csv --output result.json
  $ csv2json convert data.csv -o output.json --delimiter ";"
  $ csv2json convert data.csv --no-pretty
  $ csv2json convert data.csv --no-header -e utf-8
`)
  .action(async (input: string, opts) => {
    const { runConvert } = await import('./commands/convert.js');
    await runConvert(input, opts);
  });

program.addHelpText('after', `
Examples:
  $ csv2json convert input.csv
  $ csv2json convert input.csv -o output.json
  $ csv2json --help
`);

const run = async (): Promise<void> => {
  try {
    await program.parseAsync();
  } catch (error) {
    if (error instanceof CliError) {
      console.error(theme.error(`\n  Error: ${error.message}`));
      if (error.hint) {
        console.error(theme.dim(`  Hint: ${error.hint}`));
      }
      process.exit(error.exitCode);
    }
    console.error(theme.error('\n  Unexpected error occurred'));
    if (process.env.VERBOSE) {
      console.error(error);
    } else {
      console.error(theme.dim('  Run with --verbose for details'));
    }
    process.exit(1);
  }
};

run();
