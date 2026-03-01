// src/ui/theme.ts
// Color palette and styling constants for the CLI
// Presentation Layer — no business logic here

import chalk from 'chalk';

export const theme = {
  // Core palette
  primary: chalk.cyan,
  success: chalk.green,
  warning: chalk.yellow,
  error: chalk.red,
  dim: chalk.dim,
  bold: chalk.bold,
  heading: chalk.cyan.bold,
  highlight: chalk.magenta,

  // Semantic colors
  taskId: chalk.dim,
  taskTitle: chalk.white.bold,
  taskDone: chalk.green.strikethrough,
  taskPending: chalk.yellow,
  timestamp: chalk.dim,
  accent: chalk.magentaBright,
  separator: chalk.dim,

  // Status badges
  badge: {
    pending: chalk.bgYellow.black(' PENDING '),
    done: chalk.bgGreen.black(' DONE '),
    total: chalk.bgCyan.black(' TOTAL '),
  },

  // Box-drawing characters
  box: {
    topLeft: '\u250C',
    topRight: '\u2510',
    bottomLeft: '\u2514',
    bottomRight: '\u2518',
    horizontal: '\u2500',
    vertical: '\u2502',
    teeRight: '\u251C',
    teeLeft: '\u2524',
  },
} as const;
