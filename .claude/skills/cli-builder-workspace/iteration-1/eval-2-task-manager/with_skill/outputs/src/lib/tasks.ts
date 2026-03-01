// src/lib/tasks.ts
// Business Logic Layer — pure task operations
// No UI imports, no direct I/O. Operates on immutable data structures.

import type {
  Task,
  TaskStore,
  TaskStats,
  TaskFilter,
  AddTaskResult,
  CompleteTaskResult,
} from './types.js';

export const createTask = (store: TaskStore, title: string): AddTaskResult => {
  const trimmed = title.trim();
  if (trimmed.length === 0) {
    throw new Error('Task title cannot be empty');
  }
  if (trimmed.length > 200) {
    throw new Error('Task title cannot exceed 200 characters');
  }

  const task: Task = {
    id: store.nextId,
    title: trimmed,
    done: false,
    createdAt: new Date().toISOString(),
    completedAt: null,
  };

  const updatedStore: TaskStore = {
    nextId: store.nextId + 1,
    tasks: [...store.tasks, task],
  };

  return { task, store: updatedStore };
};

export const completeTask = (store: TaskStore, taskId: number): CompleteTaskResult => {
  const taskIndex = store.tasks.findIndex((t) => t.id === taskId);

  if (taskIndex === -1) {
    throw new Error(`Task with ID ${taskId} not found`);
  }

  const existing = store.tasks[taskIndex];

  if (existing === undefined) {
    throw new Error(`Task with ID ${taskId} not found`);
  }

  if (existing.done) {
    throw new Error(`Task ${taskId} is already completed`);
  }

  const updatedTask: Task = {
    ...existing,
    done: true,
    completedAt: new Date().toISOString(),
  };

  const updatedTasks = store.tasks.map((t, i) =>
    i === taskIndex ? updatedTask : t
  );

  const updatedStore: TaskStore = {
    ...store,
    tasks: updatedTasks,
  };

  return { task: updatedTask, store: updatedStore };
};

export const filterTasks = (store: TaskStore, filter: TaskFilter): readonly Task[] => {
  switch (filter) {
    case 'pending':
      return store.tasks.filter((t) => !t.done);
    case 'done':
      return store.tasks.filter((t) => t.done);
    case 'all':
    default:
      return store.tasks;
  }
};

export const getStats = (store: TaskStore): TaskStats => {
  const total = store.tasks.length;
  const done = store.tasks.filter((t) => t.done).length;
  const pending = total - done;
  return { total, pending, done };
};
