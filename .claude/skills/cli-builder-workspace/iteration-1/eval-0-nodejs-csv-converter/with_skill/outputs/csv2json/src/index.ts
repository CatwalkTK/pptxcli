#!/usr/bin/env node
import { Command } from 'commander';
import { showBanner } from './ui/banner.js';
import { theme } from './ui/theme.js';
import { CliError } from './lib/errors.js';

const VERSION = '1.0.0';
const NAME = 'CSV2JSON';

const program = new Command()
  .name('csv2json')
  .version(VERSION, '-V, --version', 'display version number')
  .description('Convert CSV files to JSON with style')
  .option('--verbose', 'show detailed output')
  .option('--no-color', 'disable colored output')
  .hook('preAction', (thisCommand) => {
    const globalOpts = thisCommand.optsWithGlobals();
    if (globalOpts.noColor) {
      process.env.NO_COLOR = '1';
    }
    showBanner({
      name: NAME,
      version: VERSION,
      tagline: 'Fast, friendly CSV to JSON conversion',
      font: 'ANSI Shadow',
    });
  });

program
  .command('convert')
  .description('Convert a CSV file to JSON')
  .argument('<input>', 'path to the CSV file')
  .option('-o, --output <path>', 'output JSON file path (default: same name as input with .json extension)')
  .option('-d, --delimiter <char>', 'CSV delimiter character', ',')
  .option('--no-pretty', 'output compact JSON (no indentation)')
  .option('--no-header', 'treat CSV as having no header row')
  .option('--array', 'wrap output in a JSON array (default)')
  .action(async (inputFile: string, opts) => {
    const globalOpts = program.optsWithGlobals();
    const { runConvert } = await import('./commands/convert.js');
    await runConvert(inputFile, {
      input: inputFile,
      output: opts.output,
      delimiter: opts.delimiter,
      pretty: opts.pretty,
      noHeader: !opts.header,
      array: opts.array,
      verbose: globalOpts.verbose,
    });
  });

// Default action: show help when no command is provided
program
  .action(() => {
    showBanner({
      name: NAME,
      version: VERSION,
      tagline: 'Fast, friendly CSV to JSON conversion',
      font: 'ANSI Shadow',
    });
    console.log(theme.dim('  Available commands:'));
    console.log(`    ${theme.primary('convert')} ${theme.dim('<input>')}  Convert a CSV file to JSON`);
    console.log();
    console.log(theme.dim('  Example:'));
    console.log(`    ${theme.code('$ csv2json convert data.csv --output result.json')}`);
    console.log();
    console.log(theme.dim('  Run csv2json --help for all options.'));
    console.log();
  });

program.addHelpText('after', `
${theme.heading('Examples:')}
  $ csv2json convert data.csv
  $ csv2json convert data.csv --output result.json
  $ csv2json convert data.csv -d ";" --no-pretty
  $ csv2json convert users.csv -o users.json --verbose
`);

// --- Run ---

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
    // Unknown errors
    console.error(theme.error('\n  Unexpected error occurred'));
    if (process.env.VERBOSE === 'true' || program.opts().verbose) {
      console.error(error);
    } else {
      console.error(theme.dim('  Run with --verbose for details'));
    }
    process.exit(1);
  }
};

run();
