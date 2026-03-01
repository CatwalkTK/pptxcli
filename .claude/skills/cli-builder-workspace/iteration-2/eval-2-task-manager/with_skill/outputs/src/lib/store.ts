import { readFile, writeFile, mkdir } from 'fs/promises';
import { dirname, resolve } from 'path';
import { homedir } from 'os';
import type { TaskStore } from '../types.js';

const DEFAULT_STORE: TaskStore = {
  nextId: 1,
  tasks: [],
};

const getStorePath = (): string => {
  const customPath = process.env.TASKR_DATA_PATH;
  if (customPath) {
    return resolve(customPath);
  }
  return resolve(homedir(), '.taskr', 'tasks.json');
};

export const loadStore = async (): Promise<TaskStore> => {
  const storePath = getStorePath();
  try {
    const content = await readFile(storePath, 'utf-8');
    const parsed = JSON.parse(content) as Partial<TaskStore>;
    return {
      nextId: parsed.nextId ?? 1,
      tasks: parsed.tasks ?? [],
    };
  } catch {
    return DEFAULT_STORE;
  }
};

export const saveStore = async (store: TaskStore): Promise<void> => {
  const storePath = getStorePath();
  const dir = dirname(storePath);
  await mkdir(dir, { recursive: true });
  const content = JSON.stringify(store, null, 2);
  await writeFile(storePath, content, 'utf-8');
};
