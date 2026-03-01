import Table from 'cli-table3';
import { theme, icons } from './theme.js';
import type { Task } from '../types.js';

const formatDate = (iso: string): string => {
  const date = new Date(iso);
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${month}/${day} ${hours}:${minutes}`;
};

export const renderTaskTable = (tasks: readonly Task[], title: string): void => {
  if (tasks.length === 0) {
    console.log(theme.dim(`  No ${title.toLowerCase()} tasks.`));
    console.log();
    return;
  }

  const table = new Table({
    head: [
      theme.primary('ID'),
      theme.primary('Status'),
      theme.primary('Task'),
      theme.primary('Created'),
      theme.primary('Completed'),
    ],
    style: { head: [], border: [] },
    colWidths: [8, 10, 36, 14, 14],
    wordWrap: true,
  });

  for (const task of tasks) {
    const statusIcon = task.status === 'done' ? icons.done : icons.pending;
    const statusText = task.status === 'done'
      ? theme.done('done')
      : theme.pending('pending');
    const titleText = task.status === 'done'
      ? theme.dim(task.title)
      : task.title;

    table.push([
      theme.taskId(`#${task.id}`),
      `${statusIcon} ${statusText}`,
      titleText,
      theme.dim(formatDate(task.createdAt)),
      task.completedAt ? theme.dim(formatDate(task.completedAt)) : theme.dim('-'),
    ]);
  }

  console.log(`  ${theme.heading(title)}`);
  console.log(table.toString());
  console.log();
};

export const renderTaskSingle = (task: Task, action: string): void => {
  const statusIcon = task.status === 'done' ? icons.done : icons.pending;
  console.log(`  ${icons.arrow} ${action}`);
  console.log(`    ${statusIcon} ${theme.taskId(`#${task.id}`)} ${task.title}`);
  console.log();
};
