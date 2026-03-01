// ============================================================
// renderer.js - Task display and formatting engine
// ============================================================

const c = require('./colors');
const { divider, BULLET } = require('./banner');

// ── Priority Symbols & Colors ──────────────────────────────

const PRIORITY_DISPLAY = {
  high:   { icon: '🔴', label: 'HIGH',   color: c.brightRed },
  medium: { icon: '🟡', label: 'MED',    color: c.brightYellow },
  low:    { icon: '🔵', label: 'LOW',    color: c.brightBlue },
};

const STATUS_DISPLAY = {
  pending: { icon: '○', color: c.yellow },
  done:    { icon: '●', color: c.green },
};

// ── Time Formatting ────────────────────────────────────────

const timeAgo = (isoDate) => {
  const diff = Date.now() - new Date(isoDate).getTime();
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours   = Math.floor(minutes / 60);
  const days    = Math.floor(hours / 24);
  const weeks   = Math.floor(days / 7);

  if (weeks > 0)   return `${weeks}w ago`;
  if (days > 0)    return `${days}d ago`;
  if (hours > 0)   return `${hours}h ago`;
  if (minutes > 0) return `${minutes}m ago`;
  return 'just now';
};

// ── Task List Renderer ─────────────────────────────────────

const renderTaskList = (tasks, title = 'TASKS') => {
  if (tasks.length === 0) {
    console.log('');
    console.log(c.muted('  No tasks found.'));
    console.log(c.muted(`  Use ${c.info('add <description>')} to create one.`));
    console.log('');
    return;
  }

  console.log('');
  console.log(`  ${c.highlight(title)}  ${c.muted(`(${tasks.length} items)`)}`);
  console.log('');

  const maxIdLen = Math.max(...tasks.map((t) => String(t.id).length), 2);

  for (const task of tasks) {
    const status = STATUS_DISPLAY[task.status] || STATUS_DISPLAY.pending;
    const priority = PRIORITY_DISPLAY[task.priority] || PRIORITY_DISPLAY.medium;

    const idStr = c.muted(`#${String(task.id).padStart(maxIdLen, '0')}`);
    const statusIcon = status.color(status.icon);
    const desc =
      task.status === 'done'
        ? c.dim(c.strikethrough(task.description))
        : c.white(task.description);
    const priorityBadge = priority.color(`[${priority.label}]`);
    const tagStr = task.tag ? c.accent(`#${task.tag}`) : '';
    const timeStr = c.muted(timeAgo(task.createdAt));

    const completedStr =
      task.status === 'done' && task.completedAt
        ? c.success(` ✓ ${timeAgo(task.completedAt)}`)
        : '';

    console.log(
      `  ${statusIcon} ${idStr}  ${priorityBadge} ${desc} ${tagStr} ${timeStr}${completedStr}`
    );
  }

  console.log('');
  console.log(divider('─', c.dim));
  console.log('');
};

// ── Stats Renderer ─────────────────────────────────────────

const renderStats = (stats) => {
  console.log('');
  console.log(`  ${c.highlight('STATISTICS')}`);
  console.log('');

  // Progress bar
  const barWidth = 30;
  const filled = Math.round((stats.completionRate / 100) * barWidth);
  const empty = barWidth - filled;
  const bar =
    c.green('█'.repeat(filled)) + c.muted('░'.repeat(empty));

  console.log(`  ${c.info('Progress')}   ${bar} ${c.bold(c.white(`${stats.completionRate}%`))}`);
  console.log('');

  // Counts
  console.log(`  ${c.info('Total')}      ${c.highlight(String(stats.total))}`);
  console.log(`  ${c.yellow('○ Pending')}  ${c.yellow(String(stats.pending))}`);
  console.log(`  ${c.green('● Done')}     ${c.green(String(stats.done))}`);
  console.log('');

  // Priority breakdown
  console.log(`  ${c.info('By Priority')}`);
  console.log(`    ${c.brightRed('HIGH')}    ${stats.priorityCounts.high || 0}`);
  console.log(`    ${c.brightYellow('MEDIUM')}  ${stats.priorityCounts.medium || 0}`);
  console.log(`    ${c.brightBlue('LOW')}     ${stats.priorityCounts.low || 0}`);
  console.log('');

  // Tags
  const tagEntries = Object.entries(stats.tags);
  if (tagEntries.length > 0) {
    console.log(`  ${c.info('Tags')}`);
    for (const [tag, count] of tagEntries) {
      console.log(`    ${c.accent(`#${tag}`)}  ${c.muted(`${count} tasks`)}`);
    }
    console.log('');
  }

  // Recent activity
  console.log(
    `  ${c.info('Last 7 days')}  ${c.success(`${stats.recentDone} completed`)}`
  );
  console.log('');
  console.log(divider('─', c.dim));
  console.log('');
};

// ── Status Bar (shown after commands) ──────────────────────

const renderStatusBar = (stats) => {
  const pending = c.yellow(`○ ${stats.pending} pending`);
  const done = c.green(`● ${stats.done} done`);
  const rate = c.muted(`(${stats.completionRate}%)`);

  console.log(c.muted(`  ${BULLET} ${pending}  ${done}  ${rate}`));
  console.log('');
};

// ── Success / Error Messages ───────────────────────────────

const renderSuccess = (message) => {
  console.log(`\n  ${c.success('✓')} ${c.white(message)}\n`);
};

const renderError = (message) => {
  console.log(`\n  ${c.error('✗')} ${c.white(message)}\n`);
};

const renderWarning = (message) => {
  console.log(`\n  ${c.warn('⚠')} ${c.white(message)}\n`);
};

module.exports = {
  renderTaskList,
  renderStats,
  renderStatusBar,
  renderSuccess,
  renderError,
  renderWarning,
  timeAgo,
};
