import type { Task, TaskStore, TaskSummary } from '../types.js';

export const addTask = (store: TaskStore, title: string): { store: TaskStore; task: Task } => {
  const task: Task = {
    id: store.nextId,
    title,
    status: 'pending',
    createdAt: new Date().toISOString(),
    completedAt: null,
  };

  const updatedStore: TaskStore = {
    nextId: store.nextId + 1,
    tasks: [...store.tasks, task],
  };

  return { store: updatedStore, task };
};

export const completeTask = (store: TaskStore, id: number): { store: TaskStore; task: Task | null } => {
  const target = store.tasks.find((t) => t.id === id);
  if (!target) {
    return { store, task: null };
  }

  if (target.status === 'done') {
    return { store, task: target };
  }

  const completedTask: Task = {
    ...target,
    status: 'done',
    completedAt: new Date().toISOString(),
  };

  const updatedTasks = store.tasks.map((t) =>
    t.id === id ? completedTask : t,
  );

  return {
    store: { ...store, tasks: updatedTasks },
    task: completedTask,
  };
};

export const getTaskSummary = (store: TaskStore): TaskSummary => {
  const total = store.tasks.length;
  const done = store.tasks.filter((t) => t.status === 'done').length;
  const pending = total - done;
  const completionRate = total > 0 ? Math.round((done / total) * 100) : 0;

  return { total, pending, done, completionRate };
};

export const getPendingTasks = (store: TaskStore): readonly Task[] =>
  store.tasks.filter((t) => t.status === 'pending');

export const getDoneTasks = (store: TaskStore): readonly Task[] =>
  store.tasks.filter((t) => t.status === 'done');

export const getAllTasks = (store: TaskStore): readonly Task[] =>
  store.tasks;
