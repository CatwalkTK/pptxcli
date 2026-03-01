export type TaskStatus = 'pending' | 'done';

export type Task = {
  readonly id: number;
  readonly title: string;
  readonly status: TaskStatus;
  readonly createdAt: string;
  readonly completedAt: string | null;
};

export type TaskStore = {
  readonly nextId: number;
  readonly tasks: readonly Task[];
};

export type TaskSummary = {
  readonly total: number;
  readonly pending: number;
  readonly done: number;
  readonly completionRate: number;
};
