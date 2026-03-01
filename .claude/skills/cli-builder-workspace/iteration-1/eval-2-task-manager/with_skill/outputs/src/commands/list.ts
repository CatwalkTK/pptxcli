// src/commands/list.ts
// Command handler for listing tasks
// Thin layer: loads data, applies filter, formats output

import { theme } from '../ui/theme.js';
import { showMiniHeader } from '../ui/banner.js';
import { formatTaskList, formatSummary } from '../ui/formatters.js';
import { loadStore, getStoragePath } from '../lib/store.js';
import { filterTasks, getStats } from '../lib/tasks.js';
import type { TaskFilter } from '../lib/types.js';

export const runList = (options: { filter: TaskFilter }): void => {
  const filterLabel =
    options.filter === 'all' ? 'All Tasks' :
    options.filter === 'pending' ? 'Pending Tasks' :
    'Completed Tasks';

  showMiniHeader(filterLabel);

  const storagePath = getStoragePath();
  const store = loadStore(storagePath);
  const tasks = filterTasks(store, options.filter);

  console.log(formatTaskList(tasks));

  const stats = getStats(store);
  console.log(formatSummary(stats.total, stats.pending, stats.done));
};
