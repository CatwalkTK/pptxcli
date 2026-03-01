// ============================================================
// store.js - JSON-based task persistence layer
// ============================================================

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');
const DATA_FILE = path.join(DATA_DIR, 'tasks.json');

const DEFAULT_DATA = {
  meta: {
    version: '1.0.0',
    createdAt: new Date().toISOString(),
    lastModified: new Date().toISOString(),
    nextId: 1,
  },
  tasks: [],
};

const ensureDataDir = () => {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
};

const load = () => {
  ensureDataDir();
  if (!fs.existsSync(DATA_FILE)) {
    save(DEFAULT_DATA);
    return { ...DEFAULT_DATA };
  }
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf-8');
    return JSON.parse(raw);
  } catch {
    // Corrupted file - back up and reset
    const backupPath = DATA_FILE + '.backup.' + Date.now();
    if (fs.existsSync(DATA_FILE)) {
      fs.copyFileSync(DATA_FILE, backupPath);
    }
    save(DEFAULT_DATA);
    return { ...DEFAULT_DATA };
  }
};

const save = (data) => {
  ensureDataDir();
  const updated = {
    ...data,
    meta: {
      ...data.meta,
      lastModified: new Date().toISOString(),
    },
  };
  fs.writeFileSync(DATA_FILE, JSON.stringify(updated, null, 2), 'utf-8');
  return updated;
};

const getNextId = (data) => {
  const id = data.meta.nextId;
  data.meta.nextId = id + 1;
  return id;
};

const addTask = (description, options = {}) => {
  const data = load();
  const id = getNextId(data);
  const now = new Date().toISOString();

  const task = {
    id,
    description: description.trim(),
    status: 'pending',
    priority: options.priority || 'medium',
    tag: options.tag || null,
    createdAt: now,
    updatedAt: now,
    completedAt: null,
  };

  const updatedData = {
    ...data,
    meta: { ...data.meta },
    tasks: [...data.tasks, task],
  };

  save(updatedData);
  return task;
};

const getTasks = (filter = {}) => {
  const data = load();
  let tasks = [...data.tasks];

  if (filter.status) {
    tasks = tasks.filter((t) => t.status === filter.status);
  }
  if (filter.tag) {
    tasks = tasks.filter((t) => t.tag && t.tag.toLowerCase() === filter.tag.toLowerCase());
  }
  if (filter.priority) {
    tasks = tasks.filter((t) => t.priority === filter.priority);
  }

  // Sort: high priority first, then by creation date
  const priorityOrder = { high: 0, medium: 1, low: 2 };
  tasks.sort((a, b) => {
    const pDiff = (priorityOrder[a.priority] || 1) - (priorityOrder[b.priority] || 1);
    if (pDiff !== 0) return pDiff;
    return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
  });

  return tasks;
};

const markDone = (id) => {
  const data = load();
  const taskIndex = data.tasks.findIndex((t) => t.id === id);
  if (taskIndex === -1) return null;

  const now = new Date().toISOString();
  const updatedTask = {
    ...data.tasks[taskIndex],
    status: 'done',
    updatedAt: now,
    completedAt: now,
  };

  const updatedTasks = data.tasks.map((t, i) => (i === taskIndex ? updatedTask : t));
  save({ ...data, tasks: updatedTasks });
  return updatedTask;
};

const removeTask = (id) => {
  const data = load();
  const task = data.tasks.find((t) => t.id === id);
  if (!task) return null;

  const updatedTasks = data.tasks.filter((t) => t.id !== id);
  save({ ...data, tasks: updatedTasks });
  return task;
};

const clearDone = () => {
  const data = load();
  const doneCount = data.tasks.filter((t) => t.status === 'done').length;
  const updatedTasks = data.tasks.filter((t) => t.status !== 'done');
  save({ ...data, tasks: updatedTasks });
  return doneCount;
};

const getStats = () => {
  const data = load();
  const tasks = data.tasks;
  const pending = tasks.filter((t) => t.status === 'pending');
  const done = tasks.filter((t) => t.status === 'done');

  const priorityCounts = { high: 0, medium: 0, low: 0 };
  for (const t of pending) {
    priorityCounts[t.priority] = (priorityCounts[t.priority] || 0) + 1;
  }

  const tags = {};
  for (const t of tasks) {
    if (t.tag) {
      tags[t.tag] = (tags[t.tag] || 0) + 1;
    }
  }

  // Completion rate for the last 7 days
  const sevenDaysAgo = new Date();
  sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
  const recentDone = done.filter(
    (t) => t.completedAt && new Date(t.completedAt) >= sevenDaysAgo
  ).length;

  return {
    total: tasks.length,
    pending: pending.length,
    done: done.length,
    completionRate: tasks.length > 0 ? Math.round((done.length / tasks.length) * 100) : 0,
    priorityCounts,
    tags,
    recentDone,
    lastModified: data.meta.lastModified,
  };
};

module.exports = {
  addTask,
  getTasks,
  markDone,
  removeTask,
  clearDone,
  getStats,
  load,
};
