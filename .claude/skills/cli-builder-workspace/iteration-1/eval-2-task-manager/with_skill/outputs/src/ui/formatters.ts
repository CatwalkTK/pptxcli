// src/ui/formatters.ts
// Output formatting utilities for tasks
// Presentation Layer — converts data to styled terminal output

import chalk from 'chalk';
import Table from 'cli-table3';
import { theme } from './theme.js';
import type { Task } from '../lib/types.js';

const formatDate = (iso: string): string => {
  const d = new Date(iso);
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const mins = String(d.getMinutes()).padStart(2, '0');
  return `${month}/${day} ${hours}:${mins}`;
};

const statusIcon = (done: boolean): string =>
  done
    ? theme.success('\u2714')   // checkmark
    : theme.warning('\u25CB');  // empty circle

const formatTitle = (title: string, done: boolean): string =>
  done ? theme.taskDone(title) : theme.taskTitle(title);

export const formatTaskList = (tasks: readonly Task[]): string => {
  if (tasks.length === 0) {
    return [
      '',
      theme.dim('  No tasks yet. Start by adding one:'),
      '',
      theme.primary('    taskr add "Your first task"'),
      '',
    ].join('\n');
  }

  const table = new Table({
    chars: {
      top: '\u2500', 'top-mid': '\u252C', 'top-left': '\u250C', 'top-right': '\u2510',
      bottom: '\u2500', 'bottom-mid': '\u2534', 'bottom-left': '\u2514', 'bottom-right': '\u2518',
      left: '\u2502', 'left-mid': '\u251C', mid: '\u2500', 'mid-mid': '\u253C',
      right: '\u2502', 'right-mid': '\u2524', middle: '\u2502',
    },
    head: [
      theme.heading(' # '),
      theme.heading(' Status '),
      theme.heading(' Task '),
      theme.heading(' Created '),
    ],
    colWidths: [6, 10, 42, 14],
    style: {
      head: [],
      border: ['dim'],
      compact: false,
    },
  });

  for (const task of tasks) {
    table.push([
      theme.taskId(` ${task.id} `),
      ` ${statusIcon(task.done)} `,
      ` ${formatTitle(task.title, task.done)} `,
      ` ${theme.timestamp(formatDate(task.createdAt))} `,
    ]);
  }

  return '\n' + table.toString() + '\n';
};

export const formatTaskAdded = (task: Task): string => {
  return [
    '',
    theme.success('  \u2714 Task added successfully!'),
    '',
    theme.dim('    ID:    ') + theme.bold(`${task.id}`),
    theme.dim('    Title: ') + theme.taskTitle(task.title),
    '',
  ].join('\n');
};

export const formatTaskDone = (task: Task): string => {
  return [
    '',
    theme.success('  \u2714 Task completed!'),
    '',
    theme.dim('    ID:    ') + theme.bold(`${task.id}`),
    theme.dim('    Title: ') + theme.taskDone(task.title),
    '',
  ].join('\n');
};

export const formatSummary = (total: number, pending: number, done: number): string => {
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;
  const barWidth = 20;
  const filled = Math.round((pct / 100) * barWidth);
  const empty = barWidth - filled;
  const bar =
    theme.success('\u2588'.repeat(filled)) +
    theme.dim('\u2591'.repeat(empty));

  return [
    theme.dim('  Progress: ') + bar + theme.dim(` ${pct}%`),
    theme.dim(`  ${done} done / ${pending} pending / ${total} total`),
    '',
  ].join('\n');
};
