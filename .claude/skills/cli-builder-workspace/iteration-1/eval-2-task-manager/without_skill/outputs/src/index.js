#!/usr/bin/env node

// ============================================================
//  TaskForge CLI - Terminal Task Manager
//  ─────────────────────────────────────
//  A stylish, zero-dependency task manager for the terminal.
//
//  Commands:
//    add <description>           Add a new task
//    add -p high <description>   Add with priority
//    add -t <tag> <description>  Add with tag
//    list                        List pending tasks
//    list --all                  List all tasks
//    list --tag <tag>            Filter by tag
//    done <id>                   Mark task as done
//    remove <id>                 Remove a task
//    clear --done                Clear completed tasks
//    stats                       Show statistics
//    help                        Show help
// ============================================================

const { showBanner, showHelp } = require('./banner');
const {
  handleAdd,
  handleList,
  handleDone,
  handleRemove,
  handleClear,
  handleStats,
} = require('./commands');
const { renderError } = require('./renderer');
const c = require('./colors');

// ── Parse CLI Arguments ────────────────────────────────────

const args = process.argv.slice(2);
const command = (args[0] || '').toLowerCase();
const commandArgs = args.slice(1);

// ── Route Commands ─────────────────────────────────────────

const run = () => {
  // Always show the banner
  showBanner();

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

    case 'remove':
    case 'rm':
    case 'delete':
      handleRemove(commandArgs);
      break;

    case 'clear':
      handleClear(commandArgs);
      break;

    case 'stats':
    case 'status':
      handleStats();
      break;

    case 'help':
    case '--help':
    case '-h':
      showHelp();
      break;

    case '':
      // No command - show help + current tasks
      showHelp();
      handleList([]);
      break;

    default:
      renderError(`Unknown command: "${c.info(command)}"`);
      console.log(c.muted(`  Run ${c.info('help')} to see available commands.`));
      console.log('');
      process.exitCode = 1;
      break;
  }
};

// ── Run ────────────────────────────────────────────────────

try {
  run();
} catch (err) {
  renderError(`Unexpected error: ${err.message}`);
  if (process.env.DEBUG) {
    console.error(err.stack);
  }
  process.exitCode = 1;
}
