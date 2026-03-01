#!/usr/bin/env node
// src/index.ts
// Entry point + Command Router
// Parses CLI arguments, routes to command handlers, handles errors gracefully

import { Command } from 'commander';
import { theme } from './ui/theme.js';
import { showBanner, showStatus } from './ui/banner.js';
import { loadStore, getStoragePath } from './lib/store.js';
import { getStats } from './lib/tasks.js';
import { runAdd } from './commands/add.js';
import { runList } from './commands/list.js';
import { runDone } from './commands/done.js';
import type { TaskFilter } from './lib/types.js';

// ── Global error handler ────────────────────────────────
// Never show raw stack traces to users
process.on('uncaughtException', (err: Error) => {
  console.error(theme.error(`\n  Error: ${err.message}`));
  console.error(theme.dim('  Run with --verbose for details\n'));
  process.exit(1);
});

process.on('unhandledRejection', (reason: unknown) => {
  const message = reason instanceof Error ? reason.message : String(reason);
  console.error(theme.error(`\n  Error: ${message}`));
  process.exit(1);
});

// ── Program setup ───────────────────────────────────────
const program = new Command()
  .name('taskr')
  .version('1.0.0', '-v, --version', 'Show version number')
  .description('A stylish terminal task manager');

// ── Default action (no subcommand) ──────────────────────
// Show banner + status when invoked without arguments
program.action(() => {
  showBanner();

  try {
    const storagePath = getStoragePath();
    const store = loadStore(storagePath);
    const stats = getStats(store);
    showStatus(stats, storagePath);
  } catch {
    // Fresh install, no tasks file yet — that's fine
    showStatus({ total: 0, pending: 0, done: 0 }, getStoragePath());
  }
});

// ── add <title> ─────────────────────────────────────────
program
  .command('add')
  .description('Add a new task')
  .argument('<title>', 'Task description')
  .addHelpText('after', `
  ${theme.heading('Examples:')}
    $ taskr add "Design the database schema"
    $ taskr add "Write unit tests for auth module"
    $ taskr add "Review pull request #42"
  `)
  .action((title: string) => {
    try {
      runAdd(title);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      console.error(theme.error(`\n  Error: ${message}\n`));
      process.exit(1);
    }
  });

// ── list ────────────────────────────────────────────────
program
  .command('list')
  .alias('ls')
  .description('List all tasks')
  .option('-f, --filter <type>', 'Filter tasks: all, pending, done', 'all')
  .addHelpText('after', `
  ${theme.heading('Examples:')}
    $ taskr list                 # Show all tasks
    $ taskr list --filter pending  # Show only pending tasks
    $ taskr list --filter done     # Show only completed tasks
    $ taskr ls -f pending          # Short form
  `)
  .action((opts: { filter: string }) => {
    const validFilters: readonly string[] = ['all', 'pending', 'done'];
    if (!validFilters.includes(opts.filter)) {
      console.error(theme.error(`\n  Error: Invalid filter "${opts.filter}"`));
      console.error(theme.dim('  Valid options: all, pending, done\n'));
      process.exit(1);
    }

    try {
      runList({ filter: opts.filter as TaskFilter });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      console.error(theme.error(`\n  Error: ${message}\n`));
      process.exit(1);
    }
  });

// ── done <id> ───────────────────────────────────────────
program
  .command('done')
  .description('Mark a task as completed')
  .argument('<id>', 'Task ID to mark as done')
  .addHelpText('after', `
  ${theme.heading('Examples:')}
    $ taskr done 1    # Complete task #1
    $ taskr done 5    # Complete task #5
  `)
  .action((id: string) => {
    try {
      runDone(id);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      console.error(theme.error(`\n  Error: ${message}\n`));
      process.exit(1);
    }
  });

// ── Parse and execute ───────────────────────────────────
program.parse(process.argv);
