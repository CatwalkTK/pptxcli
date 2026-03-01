// src/ui/banner.ts
// ASCII art banner and status line display
// Presentation Layer — handles the first impression

import chalk from 'chalk';
import { theme } from './theme.js';
import type { TaskStats } from '../lib/types.js';

const BANNER = `
 ████████  █████  ███████ ██   ██ ██████
    ██    ██   ██ ██      ██  ██  ██   ██
    ██    ███████ ███████ █████   ██████
    ██    ██   ██      ██ ██  ██  ██   ██
    ██    ██   ██ ███████ ██   ██ ██   ██
`;

const TAGLINE = '  \u2591\u2592\u2593\u2588 Terminal Task Manager \u2588\u2593\u2592\u2591';

export const showBanner = (): void => {
  console.log(theme.primary(BANNER));
  console.log(theme.accent(TAGLINE));
  console.log();
};

export const showStatus = (stats: TaskStats, storagePath: string): void => {
  const pendingColor = stats.pending > 0 ? theme.warning : theme.success;
  const doneColor = stats.done > 0 ? theme.success : theme.dim;

  console.log(theme.dim('  ' + '\u2500'.repeat(40)));
  console.log(
    theme.dim('  Storage:   ') + theme.dim(storagePath)
  );
  console.log(
    theme.dim('  Tasks:     ') +
    theme.bold(`${stats.total}`) +
    theme.dim(' total') +
    theme.dim('  |  ') +
    pendingColor(`${stats.pending}`) +
    theme.dim(' pending') +
    theme.dim('  |  ') +
    doneColor(`${stats.done}`) +
    theme.dim(' done')
  );
  console.log(
    theme.dim('  Commands:  ') +
    theme.primary('add') +
    theme.dim(' | ') +
    theme.primary('list') +
    theme.dim(' | ') +
    theme.primary('done') +
    theme.dim(' | ') +
    theme.primary('help')
  );
  console.log(theme.dim('  ' + '\u2500'.repeat(40)));
  console.log();
};

export const showMiniHeader = (subtitle: string): void => {
  console.log();
  console.log(
    theme.primary('  \u2588\u2588 TASKR') +
    theme.dim(' \u2502 ') +
    theme.dim(subtitle)
  );
  console.log();
};
