#!/usr/bin/env node
import { Command } from 'commander';
import { showBanner, showStatusLine } from './ui/banner.js';
import { theme } from './ui/theme.js';
import { loadStore } from './lib/store.js';
import { getTaskSummary } from './lib/tasks.js';

const program = new Command()
  .name('taskr')
  .version('1.0.0')
  .description('A slick terminal-based task manager with style');

// Default action: show banner + status
program
  .action(async () => {
    showBanner();
    const store = await loadStore();
    const summary = getTaskSummary(store);
    showStatusLine(summary);
  });

// add command
program
  .command('add')
  .description('Add a new task')
  .argument('<title>', 'Task title (use quotes for multi-word titles)')
  .action(async (title: string) => {
    const { runAdd } = await import('./commands/add.js');
    await runAdd(title);
  });

// list command
program
  .command('list')
  .alias('ls')
  .description('List tasks')
  .option('-a, --all', 'Show all tasks (pending + completed)')
  .option('-d, --done', 'Show only completed tasks')
  .action(async (opts: { all?: boolean; done?: boolean }) => {
    const { runList } = await import('./commands/list.js');
    await runList(opts);
  });

// done command
program
  .command('done')
  .description('Mark a task as completed')
  .argument('<id>', 'Task ID to mark as done')
  .action(async (id: string) => {
    const { runDone } = await import('./commands/done.js');
    await runDone(id);
  });

// Custom help text
program.addHelpText('after', `
${theme.heading('Examples:')}
  $ taskr add "Buy groceries"          Add a new task
  $ taskr add "Write unit tests"       Add another task
  $ taskr list                         Show pending tasks
  $ taskr list --all                   Show all tasks
  $ taskr list --done                  Show completed tasks
  $ taskr done 1                       Mark task #1 as done
  $ taskr                              Show banner + status

${theme.heading('Data Storage:')}
  Tasks are saved to ~/.taskr/tasks.json
  Set TASKR_DATA_PATH to use a custom location.
`);

// Global error handling
const run = async (): Promise<void> => {
  try {
    await program.parseAsync();
  } catch (error) {
    if (error instanceof Error) {
      console.error(theme.error(`\n  Error: ${error.message}`));
    } else {
      console.error(theme.error('\n  Unexpected error occurred'));
    }
    if (process.env.VERBOSE) {
      console.error(error);
    } else {
      console.error(theme.dim('  Run with VERBOSE=1 for details'));
    }
    process.exit(1);
  }
};

run();
