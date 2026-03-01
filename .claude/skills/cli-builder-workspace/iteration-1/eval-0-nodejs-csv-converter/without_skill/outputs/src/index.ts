#!/usr/bin/env node

import { Command } from 'commander';
import { displayBanner } from './ui/banner';
import { convertCommand } from './commands/convert';

const program = new Command();

displayBanner();

program
  .name('csv2json')
  .description('A CLI tool to convert CSV files to JSON format')
  .version('1.0.0');

program
  .command('convert')
  .description('Convert a CSV file to JSON format')
  .argument('<input>', 'Path to the input CSV file')
  .option('-o, --output <path>', 'Output file path for the JSON result')
  .option('-d, --delimiter <char>', 'CSV delimiter character', ',')
  .option('-p, --pretty', 'Pretty-print the JSON output', true)
  .option('--no-pretty', 'Disable pretty-printing')
  .option('--no-header', 'Treat first row as data (no header row)')
  .action(convertCommand);

program.parse(process.argv);

if (!process.argv.slice(2).length) {
  program.outputHelp();
}
