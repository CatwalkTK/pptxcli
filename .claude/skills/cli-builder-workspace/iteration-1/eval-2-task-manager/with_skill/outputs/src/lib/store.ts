// src/lib/store.ts
// I/O Layer — JSON file persistence for task data
// Handles reading/writing the task store to disk

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { dirname } from 'path';
import type { TaskStore } from './types.js';

const DEFAULT_STORE: TaskStore = {
  nextId: 1,
  tasks: [],
};

export const getStoragePath = (): string => {
  const envPath = process.env['TASKR_FILE'];
  if (envPath) return envPath;

  const cwd = process.cwd();
  return `${cwd}/tasks.json`;
};

export const loadStore = (filePath: string): TaskStore => {
  if (!existsSync(filePath)) {
    return { ...DEFAULT_STORE };
  }

  try {
    const raw = readFileSync(filePath, 'utf-8');
    const parsed = JSON.parse(raw) as TaskStore;

    // Validate structure
    if (
      typeof parsed.nextId !== 'number' ||
      !Array.isArray(parsed.tasks)
    ) {
      throw new Error('Invalid task store format');
    }

    return {
      nextId: parsed.nextId,
      tasks: [...parsed.tasks],
    };
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    throw new Error(`Failed to load tasks from ${filePath}: ${message}`);
  }
};

export const saveStore = (filePath: string, store: TaskStore): void => {
  try {
    const dir = dirname(filePath);
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }

    const data = JSON.stringify(store, null, 2) + '\n';
    writeFileSync(filePath, data, 'utf-8');
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    throw new Error(`Failed to save tasks to ${filePath}: ${message}`);
  }
};
