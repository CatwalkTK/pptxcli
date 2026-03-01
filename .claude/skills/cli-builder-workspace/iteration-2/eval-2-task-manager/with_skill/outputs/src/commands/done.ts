import { loadStore, saveStore } from '../lib/store.js';
import { completeTask } from '../lib/tasks.js';
import { showCompactBanner } from '../ui/banner.js';
import { renderTaskSingle } from '../ui/table.js';
import { theme, icons } from '../ui/theme.js';

export const runDone = async (idStr: string): Promise<void> => {
  showCompactBanner();

  const id = parseInt(idStr, 10);
  if (isNaN(id) || id <= 0) {
    console.log(`  ${icons.cross} ${theme.error('Error:')} Invalid task ID "${idStr}".`);
    console.log(theme.dim('  Hint: taskr done 1'));
    console.log();
    process.exit(1);
  }

  const store = await loadStore();
  const result = completeTask(store, id);

  if (!result.task) {
    console.log(`  ${icons.cross} ${theme.error('Error:')} Task #${id} not found.`);
    console.log(theme.dim('  Hint: Use "taskr list --all" to see all tasks.'));
    console.log();
    process.exit(1);
  }

  if (result.task.status === 'done' && result.store === store) {
    console.log(`  ${icons.arrow} Task ${theme.taskId(`#${id}`)} is already completed.`);
    console.log();
    return;
  }

  await saveStore(result.store);

  renderTaskSingle(result.task, theme.success('Task completed!'));
};
