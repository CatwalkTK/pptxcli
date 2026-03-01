import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { loadStore, saveStore } from '../../src/lib/store.js';
import { mkdtemp, rm } from 'fs/promises';
import { join } from 'path';
import { tmpdir } from 'os';
import type { TaskStore } from '../../src/types.js';

describe('store', () => {
  let tempDir: string;

  beforeEach(async () => {
    tempDir = await mkdtemp(join(tmpdir(), 'taskr-test-'));
    process.env.TASKR_DATA_PATH = join(tempDir, 'tasks.json');
  });

  afterEach(async () => {
    delete process.env.TASKR_DATA_PATH;
    await rm(tempDir, { recursive: true, force: true });
  });

  it('should return default store when no file exists', async () => {
    const store = await loadStore();

    expect(store.nextId).toBe(1);
    expect(store.tasks).toHaveLength(0);
  });

  it('should save and load store round-trip', async () => {
    const store: TaskStore = {
      nextId: 3,
      tasks: [
        {
          id: 1,
          title: 'Task 1',
          status: 'done',
          createdAt: '2025-01-01T00:00:00.000Z',
          completedAt: '2025-01-02T00:00:00.000Z',
        },
        {
          id: 2,
          title: 'Task 2',
          status: 'pending',
          createdAt: '2025-01-01T00:00:00.000Z',
          completedAt: null,
        },
      ],
    };

    await saveStore(store);
    const loaded = await loadStore();

    expect(loaded.nextId).toBe(3);
    expect(loaded.tasks).toHaveLength(2);
    expect(loaded.tasks[0].title).toBe('Task 1');
    expect(loaded.tasks[0].status).toBe('done');
    expect(loaded.tasks[1].title).toBe('Task 2');
    expect(loaded.tasks[1].status).toBe('pending');
  });
});
