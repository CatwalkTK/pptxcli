import { addTask, completeTask, getAllTasks, getStats } from './store.js';
import { c, printStatus, printTaskList, printHelp, formatTask } from './ui.js';

// ─────────────────────────────────────────────
// Command: add
// ─────────────────────────────────────────────
export const handleAdd = (args) => {
  // Parse title and optional --priority flag
  const priorityIdx = args.findIndex((a) => a === '--priority' || a === '-p');
  let priority = 'normal';
  let titleParts;

  if (priorityIdx !== -1) {
    const pVal = args[priorityIdx + 1];
    if (['high', 'normal', 'low'].includes(pVal)) {
      priority = pVal;
    } else {
      console.log(c.red('  Error: Priority must be one of: high, normal, low'));
      process.exit(1);
    }
    titleParts = [...args.slice(0, priorityIdx), ...args.slice(priorityIdx + 2)];
  } else {
    titleParts = args;
  }

  const title = titleParts.join(' ').trim();

  if (!title) {
    console.log(c.red('  Error: Task title is required'));
    console.log(c.dim('  Usage: taskr add "Buy groceries" --priority high'));
    process.exit(1);
  }

  const task = addTask(title, priority);
  console.log('');
  console.log(c.green(c.bold('  + Task added successfully!')));
  console.log('');
  console.log(formatTask(task));
  console.log('');

  // Show mini status
  const stats = getStats();
  console.log(c.dim(`  Total: ${stats.total} | Open: ${stats.pending} | Done: ${stats.completed}`));
  console.log('');
};

// ─────────────────────────────────────────────
// Command: list
// ─────────────────────────────────────────────
export const handleList = (args) => {
  const tasks = getAllTasks();

  let filter = 'open';
  if (args.includes('--all') || args.includes('-a')) {
    filter = 'all';
  } else if (args.includes('--done') || args.includes('-d')) {
    filter = 'done';
  } else if (args.includes('--open') || args.includes('-o')) {
    filter = 'open';
  }

  console.log('');
  printTaskList(tasks, filter);
};

// ─────────────────────────────────────────────
// Command: done
// ─────────────────────────────────────────────
export const handleDone = (args) => {
  const idStr = args[0];

  if (!idStr) {
    console.log(c.red('  Error: Task ID is required'));
    console.log(c.dim('  Usage: taskr done 1'));
    process.exit(1);
  }

  const id = parseInt(idStr, 10);

  if (isNaN(id)) {
    console.log(c.red(`  Error: "${idStr}" is not a valid task ID`));
    process.exit(1);
  }

  const result = completeTask(id);

  if (!result) {
    console.log('');
    console.log(c.red(`  Error: Task #${id} not found`));
    console.log(c.dim('  Run "taskr list --all" to see all tasks'));
    console.log('');
    process.exit(1);
  }

  if (result.alreadyDone) {
    console.log('');
    console.log(c.yellow(`  Task #${id} is already completed`));
    console.log('');
    return;
  }

  console.log('');
  console.log(c.green(c.bold('  \u2713 Task completed!')));
  console.log('');
  console.log(formatTask(result));
  console.log('');

  // Celebratory message for milestones
  const stats = getStats();
  if (stats.pending === 0 && stats.total > 0) {
    console.log(c.bgGreen(c.bold('  ALL TASKS COMPLETE! You\'re a productivity machine!  ')));
    console.log('');
  } else if (stats.completedToday >= 5) {
    console.log(c.yellow(`  On fire! ${stats.completedToday} tasks completed today!`));
    console.log('');
  }

  console.log(c.dim(`  Remaining: ${stats.pending} open task${stats.pending !== 1 ? 's' : ''}`));
  console.log('');
};

// ─────────────────────────────────────────────
// Command: status (shown with banner on bare run)
// ─────────────────────────────────────────────
export const handleStatus = () => {
  const stats = getStats();
  printStatus(stats);
};

// ─────────────────────────────────────────────
// Command: help
// ─────────────────────────────────────────────
export const handleHelp = () => {
  console.log('');
  printHelp();
};
