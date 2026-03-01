// src/lib/types.ts
// Shared type definitions for the task manager
// No imports from UI or I/O layers

export type Task = {
  readonly id: number;
  readonly title: string;
  readonly done: boolean;
  readonly createdAt: string;
  readonly completedAt: string | null;
};

export type TaskStore = {
  readonly nextId: number;
  readonly tasks: readonly Task[];
};

export type TaskStats = {
  readonly total: number;
  readonly pending: number;
  readonly done: number;
};

export type AddTaskResult = {
  readonly task: Task;
  readonly store: TaskStore;
};

export type CompleteTaskResult = {
  readonly task: Task;
  readonly store: TaskStore;
};

export type TaskFilter = 'all' | 'pending' | 'done';
