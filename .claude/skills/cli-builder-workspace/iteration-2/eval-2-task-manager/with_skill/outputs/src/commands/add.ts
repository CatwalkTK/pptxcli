import { loadStore, saveStore } from '../lib/store.js';
import { addTask } from '../lib/tasks.js';
import { showCompactBanner } from '../ui/banner.js';
import { renderTaskSingle } from '../ui/table.js';
import { theme, icons } from '../ui/theme.js';

export const runAdd = async (title: string): Promise<void> => {
  showCompactBanner();

  if (!title.trim()) {
    console.log(`  ${icons.cross} ${theme.error('Error:')} Task title cannot be empty.`);
    console.log(theme.dim('  Hint: taskr add "Buy groceries"'));
    console.log();
    process.exit(1);
  }

  const store = await loadStore();
  const result = addTask(store, title.trim());
  await saveStore(result.store);

  renderTaskSingle(result.task, theme.success('Task added successfully!'));
};
