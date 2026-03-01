import { loadStore } from '../lib/store.js';
import { getAllTasks, getPendingTasks, getDoneTasks, getTaskSummary } from '../lib/tasks.js';
import { showCompactBanner, showStatusLine } from '../ui/banner.js';
import { renderTaskTable } from '../ui/table.js';
import { theme } from '../ui/theme.js';

type ListOptions = {
  readonly all?: boolean;
  readonly done?: boolean;
};

export const runList = async (opts: ListOptions): Promise<void> => {
  showCompactBanner();

  const store = await loadStore();
  const summary = getTaskSummary(store);

  showStatusLine(summary);

  if (summary.total === 0) {
    console.log(theme.dim('  No tasks yet. Add one with:'));
    console.log(`  ${theme.primary('taskr add "Your first task"')}`);
    console.log();
    return;
  }

  if (opts.all) {
    renderTaskTable(getAllTasks(store), 'All Tasks');
  } else if (opts.done) {
    renderTaskTable(getDoneTasks(store), 'Completed Tasks');
  } else {
    const pending = getPendingTasks(store);
    renderTaskTable(pending, 'Pending Tasks');

    if (summary.done > 0) {
      console.log(theme.dim(`  ${summary.done} completed task(s) hidden. Use --all or --done to show.`));
      console.log();
    }
  }
};
