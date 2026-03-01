// ─────────────────────────────────────────────
// Terminal UI helpers — colors, box drawing, banner
// ─────────────────────────────────────────────

// ANSI color helpers (no dependencies)
const esc = (code) => `\x1b[${code}m`;
const reset = esc(0);

export const c = {
  bold:      (s) => `${esc(1)}${s}${reset}`,
  dim:       (s) => `${esc(2)}${s}${reset}`,
  italic:    (s) => `${esc(3)}${s}${reset}`,
  underline: (s) => `${esc(4)}${s}${reset}`,
  red:       (s) => `${esc(31)}${s}${reset}`,
  green:     (s) => `${esc(32)}${s}${reset}`,
  yellow:    (s) => `${esc(33)}${s}${reset}`,
  blue:      (s) => `${esc(34)}${s}${reset}`,
  magenta:   (s) => `${esc(35)}${s}${reset}`,
  cyan:      (s) => `${esc(36)}${s}${reset}`,
  white:     (s) => `${esc(37)}${s}${reset}`,
  gray:      (s) => `${esc(90)}${s}${reset}`,
  bgBlue:    (s) => `${esc(44)}${esc(37)}${s}${reset}`,
  bgMagenta: (s) => `${esc(45)}${esc(37)}${s}${reset}`,
  bgCyan:    (s) => `${esc(46)}${esc(30)}${s}${reset}`,
  bgGreen:   (s) => `${esc(42)}${esc(30)}${s}${reset}`,
  bgYellow:  (s) => `${esc(43)}${esc(30)}${s}${reset}`,
  bgRed:     (s) => `${esc(41)}${esc(37)}${s}${reset}`,
};

// Box-drawing characters
const box = {
  tl: '\u256d', tr: '\u256e',
  bl: '\u2570', br: '\u256f',
  h:  '\u2500', v:  '\u2502',
  lT: '\u251c', rT: '\u2524',
};

export const drawBox = (lines, width = 56) => {
  const top    = `  ${c.cyan(box.tl + box.h.repeat(width) + box.tr)}`;
  const bottom = `  ${c.cyan(box.bl + box.h.repeat(width) + box.br)}`;
  const sep    = `  ${c.cyan(box.lT + box.h.repeat(width) + box.rT)}`;

  const padLine = (text, rawLen) => {
    const pad = width - rawLen;
    return `  ${c.cyan(box.v)} ${text}${' '.repeat(Math.max(0, pad - 1))}${c.cyan(box.v)}`;
  };

  return { top, bottom, sep, padLine };
};

// Strip ANSI escape codes to calculate visible length
export const visibleLength = (str) =>
  str.replace(/\x1b\[[0-9;]*m/g, '').length;

export const printBanner = () => {
  const W = 56;
  const { top, bottom, sep, padLine } = drawBox([], W);

  const bannerArt = [
    ' ______  ___   ____  _  __ ____  ',
    '/_  __/ / _ | / __/ / |/ // __ \\ ',
    ' / /   / __ |_\\ \\  /    // /_/ / ',
    '/_/   /_/ |_/___/ /_/|_/ \\____/  ',
  ];

  console.log('');
  console.log(top);

  for (const line of bannerArt) {
    const colored = c.bold(c.cyan(line));
    console.log(padLine(colored, line.length));
  }

  console.log(sep);

  const subtitle = '  Task Manager  ';
  const tagline = c.bgCyan(c.bold(subtitle));
  const taglineVis = subtitle.length;
  const leftPad = Math.floor((W - taglineVis) / 2);
  const rightPad = W - taglineVis - leftPad;
  console.log(
    `  ${c.cyan(box.v)}${' '.repeat(leftPad)}${tagline}${' '.repeat(rightPad)}${c.cyan(box.v)}`
  );

  const version = 'v1.0.0';
  const versionColored = c.dim(version);
  const versionLeft = Math.floor((W - version.length) / 2);
  const versionRight = W - version.length - versionLeft;
  console.log(
    `  ${c.cyan(box.v)}${' '.repeat(versionLeft)}${versionColored}${' '.repeat(versionRight)}${c.cyan(box.v)}`
  );

  console.log(bottom);
  console.log('');
};

export const printStatus = (stats) => {
  const W = 56;
  const { top, bottom, sep, padLine } = drawBox([], W);

  console.log(top);

  const title = c.bold(' STATUS DASHBOARD');
  console.log(padLine(title, ' STATUS DASHBOARD'.length));

  console.log(sep);

  // Progress bar
  const pct = stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0;
  const barWidth = 30;
  const filled = Math.round((pct / 100) * barWidth);
  const empty = barWidth - filled;
  const progressBar = c.green('\u2588'.repeat(filled)) + c.gray('\u2591'.repeat(empty));
  const progressLabel = `  Progress: ${progressBar} ${c.bold(pct + '%')}`;
  const progressRaw = `  Progress: ${'#'.repeat(filled)}${'.'.repeat(empty)} ${pct}%`;
  console.log(padLine(progressLabel, progressRaw.length));

  console.log(sep);

  // Stats grid
  const lines = [
    [
      `  ${c.blue('\u25cf')} Total: ${c.bold(String(stats.total))}`,
      `Total: . ${stats.total}`,
    ],
    [
      `  ${c.green('\u2713')} Done:  ${c.bold(c.green(String(stats.completed)))}`,
      `Done:  . ${stats.completed}`,
    ],
    [
      `  ${c.yellow('\u25cb')} Open:  ${c.bold(c.yellow(String(stats.pending)))}`,
      `Open:  . ${stats.pending}`,
    ],
    [
      `  ${c.red('\u25b2')} High:  ${c.bold(c.red(String(stats.highPriority)))}`,
      `High:  . ${stats.highPriority}`,
    ],
  ];

  for (const [colored, raw] of lines) {
    console.log(padLine(colored, raw.length + 2));
  }

  console.log(sep);

  const todayLine = `  Today: +${stats.addedToday} added  ${c.green('\u2713')} ${stats.completedToday} completed`;
  const todayRaw  = `  Today: +${stats.addedToday} added  v ${stats.completedToday} completed`;
  console.log(padLine(todayLine, todayRaw.length));

  console.log(bottom);
  console.log('');
};

export const printHelp = () => {
  console.log(c.bold('  COMMANDS:'));
  console.log('');
  console.log(`    ${c.cyan('taskr add')} ${c.dim('<title>')} ${c.dim('[--priority high|normal|low]')}`);
  console.log(`    ${c.gray('    Add a new task to your list')}`);
  console.log('');
  console.log(`    ${c.cyan('taskr list')} ${c.dim('[--all | --done | --open]')}`);
  console.log(`    ${c.gray('    Display tasks (default: open tasks)')}`);
  console.log('');
  console.log(`    ${c.cyan('taskr done')} ${c.dim('<id>')}`);
  console.log(`    ${c.gray('    Mark a task as completed')}`);
  console.log('');
  console.log(`    ${c.cyan('taskr help')}`);
  console.log(`    ${c.gray('    Show this help message')}`);
  console.log('');
};

export const PRIORITY_BADGES = {
  high:   c.bgRed(c.bold(' HIGH ')),
  normal: c.bgBlue(c.bold(' MED  ')),
  low:    c.bgGreen(c.bold(' LOW  ')),
};

export const formatTask = (task) => {
  const checkbox = task.done
    ? c.green(c.bold('\u2713'))
    : c.yellow('\u25cb');

  const id = c.dim(`#${String(task.id).padStart(3, '0')}`);
  const badge = PRIORITY_BADGES[task.priority] || PRIORITY_BADGES.normal;

  const titleText = task.done
    ? c.dim(c.italic(task.title))
    : c.white(c.bold(task.title));

  const date = new Date(task.createdAt);
  const dateStr = c.dim(
    `${date.getMonth() + 1}/${date.getDate()}`
  );

  return `  ${checkbox}  ${id}  ${badge}  ${titleText}  ${dateStr}`;
};

export const printTaskList = (tasks, filter = 'open') => {
  let filtered;
  let heading;

  if (filter === 'all') {
    filtered = tasks;
    heading = 'ALL TASKS';
  } else if (filter === 'done') {
    filtered = tasks.filter((t) => t.done);
    heading = 'COMPLETED TASKS';
  } else {
    filtered = tasks.filter((t) => !t.done);
    heading = 'OPEN TASKS';
  }

  // Sort: high priority first, then by id
  const priorityOrder = { high: 0, normal: 1, low: 2 };
  const sorted = [...filtered].sort((a, b) => {
    if (a.done !== b.done) return a.done ? 1 : -1;
    const pa = priorityOrder[a.priority] ?? 1;
    const pb = priorityOrder[b.priority] ?? 1;
    if (pa !== pb) return pa - pb;
    return a.id - b.id;
  });

  console.log(c.bold(`  ${heading}`));
  console.log(`  ${c.cyan('\u2500'.repeat(50))}`);

  if (sorted.length === 0) {
    console.log('');
    console.log(c.dim('    No tasks found. Add one with: taskr add "My task"'));
    console.log('');
    return;
  }

  console.log('');
  for (const task of sorted) {
    console.log(formatTask(task));
  }
  console.log('');
  console.log(c.dim(`  ${sorted.length} task${sorted.length !== 1 ? 's' : ''} shown`));
  console.log('');
};
