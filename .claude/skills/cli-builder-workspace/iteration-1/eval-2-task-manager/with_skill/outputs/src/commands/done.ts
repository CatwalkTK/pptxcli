// src/commands/done.ts
// Command handler for marking a task as completed
// Thin layer: parses input, calls business logic, formats output

import { theme } from '../ui/theme.js';
import { showMiniHeader } from '../ui/banner.js';
import { formatTaskDone, formatSummary } from '../ui/formatters.js';
import { loadStore, saveStore, getStoragePath } from '../lib/store.js';
import { completeTask, getStats } from '../lib/tasks.js';

export const runDone = (taskId: string): void => {
  showMiniHeader('Complete Task');

  const id = parseInt(taskId, 10);
  if (isNaN(id) || id <= 0) {
    console.log(theme.error('  Error: Please provide a valid task ID (positive number)'));
    console.log(theme.dim('  Usage: taskr done <id>'));
    console.log();
    process.exit(1);
  }

  const storagePath = getStoragePath();
  const store = loadStore(storagePath);
  const result = completeTask(store, id);

  saveStore(storagePath, result.store);

  console.log(formatTaskDone(result.task));

  const stats = getStats(result.store);
  console.log(formatSummary(stats.total, stats.pending, stats.done));
};
