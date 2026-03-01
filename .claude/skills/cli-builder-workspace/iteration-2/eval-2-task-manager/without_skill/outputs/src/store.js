import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_FILE = path.join(__dirname, '..', 'tasks.json');

const DEFAULT_DATA = {
  tasks: [],
  nextId: 1,
  createdAt: new Date().toISOString(),
};

export const loadTasks = () => {
  try {
    if (fs.existsSync(DATA_FILE)) {
      const raw = fs.readFileSync(DATA_FILE, 'utf-8');
      return JSON.parse(raw);
    }
  } catch {
    // If file is corrupted, start fresh
  }
  return { ...DEFAULT_DATA, tasks: [], nextId: 1 };
};

export const saveTasks = (data) => {
  const dir = path.dirname(DATA_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf-8');
};

export const addTask = (title, priority = 'normal') => {
  const data = loadTasks();
  const task = {
    id: data.nextId,
    title,
    priority,
    done: false,
    createdAt: new Date().toISOString(),
    completedAt: null,
  };
  const updatedTasks = [...data.tasks, task];
  saveTasks({ ...data, tasks: updatedTasks, nextId: data.nextId + 1 });
  return task;
};

export const completeTask = (id) => {
  const data = loadTasks();
  const taskIndex = data.tasks.findIndex((t) => t.id === id);
  if (taskIndex === -1) {
    return null;
  }
  const task = data.tasks[taskIndex];
  if (task.done) {
    return { ...task, alreadyDone: true };
  }
  const updatedTask = {
    ...task,
    done: true,
    completedAt: new Date().toISOString(),
  };
  const updatedTasks = data.tasks.map((t, i) =>
    i === taskIndex ? updatedTask : t
  );
  saveTasks({ ...data, tasks: updatedTasks });
  return updatedTask;
};

export const getAllTasks = () => {
  const data = loadTasks();
  return data.tasks;
};

export const getStats = () => {
  const tasks = getAllTasks();
  const total = tasks.length;
  const completed = tasks.filter((t) => t.done).length;
  const pending = total - completed;
  const highPriority = tasks.filter((t) => t.priority === 'high' && !t.done).length;

  const todayStr = new Date().toISOString().slice(0, 10);
  const completedToday = tasks.filter(
    (t) => t.done && t.completedAt && t.completedAt.slice(0, 10) === todayStr
  ).length;
  const addedToday = tasks.filter(
    (t) => t.createdAt.slice(0, 10) === todayStr
  ).length;

  return { total, completed, pending, highPriority, completedToday, addedToday };
};
