import figlet from 'figlet';
import { theme, icons } from './theme.js';
import type { TaskSummary } from '../types.js';

export const showBanner = (): void => {
  const art = figlet.textSync('TASKR', { font: 'ANSI Shadow' });
  console.log(theme.primary(art));
  console.log(theme.dim('  ░▒▓█ Terminal Task Manager █▓▒░'));
  console.log(theme.dim('  v1.0.0'));
  console.log();
};

export const showCompactBanner = (): void => {
  console.log(`${theme.primary.bold('TASKR')} ${theme.dim('v1.0.0')}`);
  console.log();
};

export const showStatusLine = (summary: TaskSummary): void => {
  const progressBar = buildProgressBar(summary.completionRate, 20);

  console.log(`  ${theme.dim('Tasks:')}     ${theme.bold(String(summary.total))} total`);
  console.log(`  ${theme.dim('Pending:')}   ${theme.pending(String(summary.pending))}`);
  console.log(`  ${theme.dim('Completed:')} ${theme.done(String(summary.done))}`);
  console.log(`  ${theme.dim('Progress:')}  ${progressBar} ${theme.dim(`${summary.completionRate}%`)}`);
  console.log(`  ${theme.dim('Commands:')}  add ${theme.dim('|')} list ${theme.dim('|')} done ${theme.dim('|')} help`);
  console.log();
};

const buildProgressBar = (percent: number, width: number): string => {
  const filled = Math.round((percent / 100) * width);
  const empty = width - filled;

  const filledStr = theme.success('█'.repeat(filled));
  const emptyStr = theme.dim('░'.repeat(empty));

  return `${filledStr}${emptyStr}`;
};
