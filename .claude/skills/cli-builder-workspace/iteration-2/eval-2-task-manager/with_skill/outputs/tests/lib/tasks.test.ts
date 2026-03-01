import { describe, it, expect } from 'vitest';
import { addTask, completeTask, getTaskSummary, getPendingTasks, getDoneTasks } from '../../src/lib/tasks.js';
import type { TaskStore } from '../../src/types.js';

const emptyStore: TaskStore = {
  nextId: 1,
  tasks: [],
};

describe('addTask', () => {
  it('should add a task with correct fields', () => {
    const { store, task } = addTask(emptyStore, 'Buy groceries');

    expect(task.id).toBe(1);
    expect(task.title).toBe('Buy groceries');
    expect(task.status).toBe('pending');
    expect(task.createdAt).toBeDefined();
    expect(task.completedAt).toBeNull();
    expect(store.nextId).toBe(2);
    expect(store.tasks).toHaveLength(1);
  });

  it('should increment ID for each new task', () => {
    const { store: store1 } = addTask(emptyStore, 'Task 1');
    const { store: store2 } = addTask(store1, 'Task 2');

    expect(store2.tasks).toHaveLength(2);
    expect(store2.tasks[0].id).toBe(1);
    expect(store2.tasks[1].id).toBe(2);
    expect(store2.nextId).toBe(3);
  });

  it('should not mutate the original store', () => {
    const original = { ...emptyStore, tasks: [...emptyStore.tasks] };
    addTask(emptyStore, 'New task');

    expect(emptyStore.nextId).toBe(original.nextId);
    expect(emptyStore.tasks.length).toBe(original.tasks.length);
  });
});

describe('completeTask', () => {
  it('should mark a pending task as done', () => {
    const { store: storeWithTask } = addTask(emptyStore, 'Test task');
    const { store: updatedStore, task } = completeTask(storeWithTask, 1);

    expect(task).not.toBeNull();
    expect(task?.status).toBe('done');
    expect(task?.completedAt).toBeDefined();
    expect(updatedStore.tasks[0].status).toBe('done');
  });

  it('should return null task when ID not found', () => {
    const { store: storeWithTask } = addTask(emptyStore, 'Test task');
    const { task } = completeTask(storeWithTask, 999);

    expect(task).toBeNull();
  });

  it('should return the same store when task already done', () => {
    const { store: storeWithTask } = addTask(emptyStore, 'Test task');
    const { store: doneStore } = completeTask(storeWithTask, 1);
    const { store: doubleDoneStore, task } = completeTask(doneStore, 1);

    expect(task?.status).toBe('done');
    expect(doubleDoneStore).toBe(doneStore);
  });
});

describe('getTaskSummary', () => {
  it('should return zeros for empty store', () => {
    const summary = getTaskSummary(emptyStore);

    expect(summary.total).toBe(0);
    expect(summary.pending).toBe(0);
    expect(summary.done).toBe(0);
    expect(summary.completionRate).toBe(0);
  });

  it('should count tasks correctly', () => {
    const { store: s1 } = addTask(emptyStore, 'Task 1');
    const { store: s2 } = addTask(s1, 'Task 2');
    const { store: s3 } = addTask(s2, 'Task 3');
    const { store: s4 } = completeTask(s3, 1);

    const summary = getTaskSummary(s4);

    expect(summary.total).toBe(3);
    expect(summary.pending).toBe(2);
    expect(summary.done).toBe(1);
    expect(summary.completionRate).toBe(33);
  });
});

describe('getPendingTasks', () => {
  it('should return only pending tasks', () => {
    const { store: s1 } = addTask(emptyStore, 'Pending');
    const { store: s2 } = addTask(s1, 'Also pending');
    const { store: s3 } = completeTask(s2, 1);

    const pending = getPendingTasks(s3);

    expect(pending).toHaveLength(1);
    expect(pending[0].title).toBe('Also pending');
  });
});

describe('getDoneTasks', () => {
  it('should return only completed tasks', () => {
    const { store: s1 } = addTask(emptyStore, 'Task 1');
    const { store: s2 } = addTask(s1, 'Task 2');
    const { store: s3 } = completeTask(s2, 1);

    const done = getDoneTasks(s3);

    expect(done).toHaveLength(1);
    expect(done[0].title).toBe('Task 1');
    expect(done[0].status).toBe('done');
  });
});
