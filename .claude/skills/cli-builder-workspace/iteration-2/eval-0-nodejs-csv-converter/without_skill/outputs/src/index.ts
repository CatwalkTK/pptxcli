#!/usr/bin/env node

import { Command } from 'commander';
import chalk from 'chalk';

import { showBanner } from './banner';
import { convertCsvToJson } from './converter';

const program = new Command();

program
  .name('csv2json')
  .description('A CLI tool to convert CSV files to JSON format')
  .version('1.0.0');

program
  .command('convert')
  .description('Convert a CSV file to JSON')
  .argument('<input>', 'Path to the input CSV file')
  .option('-o, --output <path>', 'Output file path (defaults to same name with .json extension)')
  .option('-d, --delimiter <char>', 'CSV delimiter character', ',')
  .option('--no-pretty', 'Disable pretty-printing of JSON output')
  .action(async (input: string, options: { output?: string; pretty?: boolean; delimiter?: string }) => {
    showBanner();

    try {
      await convertCsvToJson(input, {
        output: options.output,
        pretty: options.pretty,
        delimiter: options.delimiter,
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      console.error(chalk.red.bold(`  Error: ${message}`));
      console.log();
      process.exit(1);
    }
  });

// Show banner + help when no command is given
if (process.argv.length <= 2) {
  showBanner();
  program.outputHelp();
} else {
  program.parse(process.argv);
}
