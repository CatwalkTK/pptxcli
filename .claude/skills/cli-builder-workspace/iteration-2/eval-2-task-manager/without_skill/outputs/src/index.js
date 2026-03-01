#!/usr/bin/env node

// ─────────────────────────────────────────────────────
//  TASKR - Terminal Task Manager
//  A stylish CLI for managing your tasks with flair
// ─────────────────────────────────────────────────────

import { printBanner } from './ui.js';
import {
  handleAdd,
  handleList,
  handleDone,
  handleStatus,
  handleHelp,
} from './commands.js';

const main = () => {
  const args = process.argv.slice(2);
  const command = args[0]?.toLowerCase();
  const commandArgs = args.slice(1);

  // Always print the banner
  printBanner();

  switch (command) {
    case 'add':
      handleAdd(commandArgs);
      break;

    case 'list':
    case 'ls':
      handleList(commandArgs);
      break;

    case 'done':
    case 'complete':
      handleDone(commandArgs);
      break;

    case 'help':
    case '--help':
    case '-h':
      handleHelp();
      break;

    case undefined:
      // No command — show status dashboard + help
      handleStatus();
      handleHelp();
      break;

    default:
      console.log(`  Unknown command: "${command}"`);
      console.log('');
      handleHelp();
      process.exit(1);
  }
};

main();
