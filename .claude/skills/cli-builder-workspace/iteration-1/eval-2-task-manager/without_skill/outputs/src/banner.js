// ============================================================
// banner.js - Startup banner and display utilities
// ============================================================

const c = require('./colors');

const BANNER_ART = `
${c.rgb(0, 200, 255, '  ████████╗ █████╗ ███████╗██╗  ██╗')}
${c.rgb(0, 180, 255, '  ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝')}
${c.rgb(0, 160, 255, '     ██║   ███████║███████╗█████╔╝ ')}
${c.rgb(0, 140, 255, '     ██║   ██╔══██║╚════██║██╔═██╗ ')}
${c.rgb(0, 120, 255, '     ██║   ██║  ██║███████║██║  ██╗')}
${c.rgb(0, 100, 255, '     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝')}

${c.rgb(255, 100, 50, '  ███████╗ ██████╗ ██████╗  ██████╗ ███████╗')}
${c.rgb(255, 120, 50, '  ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝')}
${c.rgb(255, 140, 50, '  █████╗  ██║   ██║██████╔╝██║  ███╗█████╗  ')}
${c.rgb(255, 160, 50, '  ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  ')}
${c.rgb(255, 180, 50, '  ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗')}
${c.rgb(255, 200, 50, '  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝')}
`;

const DIVIDER_CHAR = '─';
const BULLET = '›';

const getTermWidth = () => {
  try {
    return process.stdout.columns || 60;
  } catch {
    return 60;
  }
};

const divider = (char = DIVIDER_CHAR, color = c.gray) => {
  const width = getTermWidth();
  return color(char.repeat(width));
};

const centeredText = (text, color = c.white) => {
  const width = getTermWidth();
  const stripped = c.strip(text);
  const padding = Math.max(0, Math.floor((width - stripped.length) / 2));
  return ' '.repeat(padding) + color(text);
};

const showBanner = () => {
  console.log('');
  console.log(BANNER_ART);
  console.log(centeredText('░▒▓█ Terminal Task Manager █▓▒░', c.bold));
  console.log(centeredText(`v1.0.0`, c.muted));
  console.log('');
  console.log(divider('═', c.dim));
  console.log('');
};

const showHelp = () => {
  const cmd = (name, desc) => {
    return `  ${c.info(name.padEnd(28))} ${c.muted(BULLET)} ${desc}`;
  };

  console.log(c.highlight('  COMMANDS'));
  console.log('');
  console.log(cmd('add <task description>',    'Add a new task'));
  console.log(cmd('add -p high <description>', 'Add task with priority (low/medium/high)'));
  console.log(cmd('add -t <tag> <description>','Add task with a tag'));
  console.log(cmd('list',                      'List all pending tasks'));
  console.log(cmd('list --all',                'List all tasks including done'));
  console.log(cmd('list --tag <tag>',          'Filter tasks by tag'));
  console.log(cmd('done <task-id>',            'Mark a task as completed'));
  console.log(cmd('done <id1> <id2> ...',      'Mark multiple tasks as done'));
  console.log(cmd('remove <task-id>',          'Remove a task permanently'));
  console.log(cmd('clear --done',              'Clear all completed tasks'));
  console.log(cmd('stats',                     'Show task statistics'));
  console.log(cmd('help',                      'Show this help message'));
  console.log('');
  console.log(divider('─', c.dim));
  console.log('');
};

module.exports = { showBanner, showHelp, divider, centeredText, BULLET };
