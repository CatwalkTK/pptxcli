// ============================================================
// commands.js - Command handlers for the task manager
// ============================================================

const store = require('./store');
const {
  renderTaskList,
  renderStats,
  renderStatusBar,
  renderSuccess,
  renderError,
  renderWarning,
} = require('./renderer');
const c = require('./colors');

// ── ADD ────────────────────────────────────────────────────

const handleAdd = (args) => {
  let priority = 'medium';
  let tag = null;
  const descParts = [];

  let i = 0;
  while (i < args.length) {
    if ((args[i] === '-p' || args[i] === '--priority') && args[i + 1]) {
      const p = args[i + 1].toLowerCase();
      if (['high', 'medium', 'low'].includes(p)) {
        priority = p;
      } else {
        renderError(`Invalid priority "${args[i + 1]}". Use: high, medium, low`);
        return;
      }
      i += 2;
      continue;
    }
    if ((args[i] === '-t' || args[i] === '--tag') && args[i + 1]) {
      tag = args[i + 1].replace(/^#/, '');
      i += 2;
      continue;
    }
    descParts.push(args[i]);
    i += 1;
  }

  const description = descParts.join(' ').trim();

  if (!description) {
    renderError('Please provide a task description.');
    console.log(c.muted(`  Usage: ${c.info('add [-p priority] [-t tag] <description>')}`));
    console.log('');
    return;
  }

  const task = store.addTask(description, { priority, tag });
  renderSuccess(`Task ${c.info(`#${String(task.id).padStart(2, '0')}`)} added`);

  const details = [];
  details.push(`"${c.white(task.description)}"`);
  if (task.priority !== 'medium') {
    const colorFn =
      task.priority === 'high' ? c.brightRed : c.brightBlue;
    details.push(colorFn(`[${task.priority.toUpperCase()}]`));
  }
  if (task.tag) {
    details.push(c.accent(`#${task.tag}`));
  }
  console.log(`  ${details.join('  ')}`);
  console.log('');

  const stats = store.getStats();
  renderStatusBar(stats);
};

// ── LIST ───────────────────────────────────────────────────

const handleList = (args) => {
  const showAll = args.includes('--all') || args.includes('-a');
  let tag = null;
  let priority = null;

  for (let i = 0; i < args.length; i++) {
    if ((args[i] === '--tag' || args[i] === '-t') && args[i + 1]) {
      tag = args[i + 1].replace(/^#/, '');
    }
    if ((args[i] === '--priority' || args[i] === '-p') && args[i + 1]) {
      priority = args[i + 1].toLowerCase();
    }
  }

  const filter = {};
  if (!showAll) {
    filter.status = 'pending';
  }
  if (tag) {
    filter.tag = tag;
  }
  if (priority) {
    filter.priority = priority;
  }

  const tasks = store.getTasks(filter);

  let title = 'PENDING TASKS';
  if (showAll) title = 'ALL TASKS';
  if (tag) title += ` #${tag}`;
  if (priority) title += ` [${priority.toUpperCase()}]`;

  renderTaskList(tasks, title);

  const stats = store.getStats();
  renderStatusBar(stats);
};

// ── DONE ───────────────────────────────────────────────────

const handleDone = (args) => {
  if (args.length === 0) {
    renderError('Please provide a task ID.');
    console.log(c.muted(`  Usage: ${c.info('done <task-id> [<task-id> ...]')}`));
    console.log('');
    return;
  }

  let successCount = 0;
  let failCount = 0;

  for (const arg of args) {
    const id = parseInt(arg, 10);
    if (isNaN(id)) {
      renderError(`Invalid task ID: "${arg}"`);
      failCount += 1;
      continue;
    }

    const task = store.markDone(id);
    if (task) {
      renderSuccess(
        `Task ${c.info(`#${String(id).padStart(2, '0')}`)} completed: ${c.dim(c.strikethrough(task.description))}`
      );
      successCount += 1;
    } else {
      renderError(`Task ${c.info(`#${String(id).padStart(2, '0')}`)} not found.`);
      failCount += 1;
    }
  }

  if (successCount > 0) {
    const stats = store.getStats();
    renderStatusBar(stats);
  }
};

// ── REMOVE ─────────────────────────────────────────────────

const handleRemove = (args) => {
  if (args.length === 0) {
    renderError('Please provide a task ID.');
    console.log(c.muted(`  Usage: ${c.info('remove <task-id>')}`));
    console.log('');
    return;
  }

  const id = parseInt(args[0], 10);
  if (isNaN(id)) {
    renderError(`Invalid task ID: "${args[0]}"`);
    return;
  }

  const task = store.removeTask(id);
  if (task) {
    renderSuccess(
      `Task ${c.info(`#${String(id).padStart(2, '0')}`)} removed: "${task.description}"`
    );
    const stats = store.getStats();
    renderStatusBar(stats);
  } else {
    renderError(`Task #${id} not found.`);
  }
};

// ── CLEAR ──────────────────────────────────────────────────

const handleClear = (args) => {
  if (!args.includes('--done')) {
    renderError('Please specify what to clear.');
    console.log(c.muted(`  Usage: ${c.info('clear --done')}  (removes completed tasks)`));
    console.log('');
    return;
  }

  const count = store.clearDone();
  if (count > 0) {
    renderSuccess(`Cleared ${c.highlight(String(count))} completed task${count > 1 ? 's' : ''}.`);
  } else {
    renderWarning('No completed tasks to clear.');
  }

  const stats = store.getStats();
  renderStatusBar(stats);
};

// ── STATS ──────────────────────────────────────────────────

const handleStats = () => {
  const stats = store.getStats();
  renderStats(stats);
};

module.exports = {
  handleAdd,
  handleList,
  handleDone,
  handleRemove,
  handleClear,
  handleStats,
};
