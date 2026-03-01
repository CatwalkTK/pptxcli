// src/commands/add.ts
// Command handler for adding a new task
// Thin layer: parses input, calls business logic, formats output

import { theme } from '../ui/theme.js';
import { showMiniHeader } from '../ui/banner.js';
import { formatTaskAdded, formatSummary } from '../ui/formatters.js';
import { loadStore, saveStore, getStoragePath } from '../lib/store.js';
import { createTask, getStats } from '../lib/tasks.js';

export const runAdd = (title: string): void => {
  showMiniHeader('Add Task');

  const storagePath = getStoragePath();
  const store = loadStore(storagePath);
  const result = createTask(store, title);

  saveStore(storagePath, result.store);

  console.log(formatTaskAdded(result.task));

  const stats = getStats(result.store);
  console.log(formatSummary(stats.total, stats.pending, stats.done));
};
