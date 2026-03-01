# Node.js / TypeScript CLI — Full Reference

## Table of Contents

1. [Project Scaffolding](#project-scaffolding)
2. [Package.json Configuration](#packagejson-configuration)
3. [TypeScript Setup](#typescript-setup)
4. [Command Routing with Commander](#command-routing-with-commander)
5. [Styled Output with Chalk](#styled-output-with-chalk)
6. [ASCII Banners with Figlet](#ascii-banners-with-figlet)
7. [Interactive Prompts](#interactive-prompts)
8. [Progress & Spinners](#progress--spinners)
9. [Tables](#tables)
10. [Configuration Management](#configuration-management)
11. [Error Handling](#error-handling)
12. [Testing CLIs](#testing-clis)
13. [Distribution](#distribution)

---

## Project Scaffolding

```bash
mkdir my-cli && cd my-cli
npm init -y

# Core deps
npm install commander chalk figlet

# Interactive
npm install @inquirer/prompts

# Progress & display
npm install ora cli-table3 boxen

# Dev deps
npm install -D typescript @types/node tsx @types/figlet
```

### Directory Layout

```
my-cli/
├── bin/
│   └── cli.js              # #!/usr/bin/env node shim
├── src/
│   ├── index.ts             # Main entry
│   ├── ui/
│   │   ├── banner.ts        # ASCII art + branding
│   │   ├── theme.ts         # Color constants
│   │   ├── spinner.ts       # Ora wrapper
│   │   └── table.ts         # Table formatting
│   ├── commands/
│   │   ├── index.ts         # Re-exports all commands
│   │   ├── init.ts
│   │   ├── build.ts
│   │   └── serve.ts
│   ├── lib/
│   │   ├── config.ts        # Config loading
│   │   └── core.ts          # Business logic
│   └── types.ts             # Shared types
├── tests/
│   ├── commands/
│   │   └── init.test.ts
│   └── lib/
│       └── core.test.ts
├── package.json
├── tsconfig.json
└── README.md
```

---

## Package.json Configuration

```json
{
  "name": "my-cli",
  "version": "1.0.0",
  "description": "What this CLI does",
  "type": "module",
  "bin": {
    "my-cli": "./bin/cli.js"
  },
  "files": ["bin/", "dist/"],
  "scripts": {
    "dev": "tsx src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "vitest"
  },
  "engines": {
    "node": ">=18"
  }
}
```

**bin/cli.js** (the entry shim):

```javascript
#!/usr/bin/env node
import '../dist/index.js';
```

---

## TypeScript Setup

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true
  },
  "include": ["src/**/*"]
}
```

---

## Command Routing with Commander

### Basic Setup

```typescript
import { Command } from 'commander';

const program = new Command()
  .name('my-cli')
  .version('1.0.0')
  .description('Tool description');
```

### Subcommands

```typescript
program
  .command('init')
  .description('Initialize a new project')
  .argument('[name]', 'project name')
  .option('-t, --template <name>', 'template to use', 'default')
  .option('--no-install', 'skip dependency installation')
  .action(async (name, opts) => {
    // ...
  });

program
  .command('build')
  .description('Build the project')
  .option('-w, --watch', 'watch for changes')
  .option('-o, --output <dir>', 'output directory', 'dist')
  .action(async (opts) => {
    // ...
  });
```

### Global Options

```typescript
program
  .option('-v, --verbose', 'verbose output')
  .option('--no-color', 'disable colors')
  .option('-c, --config <path>', 'config file path');

// Access global options inside commands:
program.commands.forEach((cmd) => {
  cmd.hook('preAction', (thisCmd) => {
    const globalOpts = thisCmd.optsWithGlobals();
    if (globalOpts.verbose) {
      process.env.VERBOSE = 'true';
    }
    if (globalOpts.noColor) {
      process.env.NO_COLOR = '1';
    }
  });
});
```

### Help Customization

```typescript
program.addHelpText('after', `
Examples:
  $ my-cli init my-project
  $ my-cli init --template typescript
  $ my-cli build --watch
`);
```

---

## Styled Output with Chalk

### Theme File

```typescript
// src/ui/theme.ts
import chalk, { type ChalkInstance } from 'chalk';

type Theme = {
  readonly primary: ChalkInstance;
  readonly secondary: ChalkInstance;
  readonly success: ChalkInstance;
  readonly warning: ChalkInstance;
  readonly error: ChalkInstance;
  readonly info: ChalkInstance;
  readonly dim: ChalkInstance;
  readonly bold: ChalkInstance;
  readonly heading: ChalkInstance;
  readonly code: ChalkInstance;
  readonly link: ChalkInstance;
};

export const theme: Theme = {
  primary: chalk.cyan,
  secondary: chalk.magenta,
  success: chalk.green,
  warning: chalk.yellow,
  error: chalk.red,
  info: chalk.blue,
  dim: chalk.dim,
  bold: chalk.bold,
  heading: chalk.cyan.bold.underline,
  code: chalk.gray,
  link: chalk.blue.underline,
};

// Utility: conditional color (respects NO_COLOR)
export const colorize = (fn: ChalkInstance, text: string): string =>
  process.env.NO_COLOR ? text : fn(text);
```

### Usage

```typescript
import { theme } from './ui/theme.js';

console.log(theme.heading('Configuration'));
console.log(`  ${theme.dim('Output:')} ${theme.primary('/dist')}`);
console.log(theme.success('  Done!'));
console.log(theme.error('  Error: file not found'));
```

---

## ASCII Banners with Figlet

### Banner Module

```typescript
// src/ui/banner.ts
import figlet from 'figlet';
import chalk from 'chalk';
import { theme } from './theme.js';

type BannerOptions = {
  name: string;
  version: string;
  tagline?: string;
  font?: figlet.Fonts;
};

export const showBanner = ({
  name,
  version,
  tagline,
  font = 'ANSI Shadow',
}: BannerOptions): void => {
  const art = figlet.textSync(name, { font });
  console.log(theme.primary(art));

  if (tagline) {
    console.log(theme.dim(`  ${tagline}`));
  }

  console.log(theme.dim(`  v${version}`));
  console.log();
};

// Compact banner for subcommands
export const showCompactBanner = (name: string, version: string): void => {
  console.log(`${theme.primary.bold(name)} ${theme.dim(`v${version}`)}`);
  console.log();
};
```

### Recommended Fonts

| Font | Style | Best For |
|------|-------|----------|
| `ANSI Shadow` | Bold, modern | Most CLIs |
| `Slant` | Italic, elegant | Developer tools |
| `Standard` | Clean, readable | Compact banners |
| `Big` | Large, blocky | Impact |
| `Small` | Compact | Narrow terminals |
| `Cybermedium` | Techy | Dev/hacker tools |

---

## Interactive Prompts

### @inquirer/prompts (Recommended)

```typescript
import {
  input,
  select,
  confirm,
  checkbox,
  password,
  number,
} from '@inquirer/prompts';

// Text input with validation
const name = await input({
  message: 'Project name:',
  default: 'my-project',
  validate: (v) => {
    if (!/^[a-z0-9-]+$/.test(v)) return 'Use lowercase, numbers, hyphens only';
    return true;
  },
});

// Select one
const framework = await select({
  message: 'Framework:',
  choices: [
    { name: 'React', value: 'react', description: 'Component-based UI' },
    { name: 'Vue', value: 'vue', description: 'Progressive framework' },
    { name: 'Svelte', value: 'svelte', description: 'Compile-time framework' },
  ],
});

// Multi-select
const features = await checkbox({
  message: 'Features:',
  choices: [
    { name: 'TypeScript', value: 'ts', checked: true },
    { name: 'ESLint', value: 'eslint' },
    { name: 'Prettier', value: 'prettier' },
    { name: 'Testing', value: 'test' },
  ],
});

// Confirm
const proceed = await confirm({
  message: 'Create project with these settings?',
  default: true,
});
```

### Non-Interactive Fallback

Always support `--yes` or `--no-input` for CI:

```typescript
const getOptions = async (cliOpts: CliOpts): Promise<Options> => {
  if (cliOpts.yes) {
    return {
      name: cliOpts.name ?? 'my-project',
      template: cliOpts.template ?? 'default',
      install: true,
    };
  }

  // Interactive prompts
  return {
    name: await input({ message: 'Project name:' }),
    template: await select({ message: 'Template:', choices: [...] }),
    install: await confirm({ message: 'Install deps?' }),
  };
};
```

---

## Progress & Spinners

### Ora Spinner

```typescript
// src/ui/spinner.ts
import ora, { type Ora } from 'ora';

export const withSpinner = async <T>(
  message: string,
  fn: (spinner: Ora) => Promise<T>,
): Promise<T> => {
  const spinner = ora(message).start();
  try {
    const result = await fn(spinner);
    spinner.succeed();
    return result;
  } catch (error) {
    spinner.fail();
    throw error;
  }
};

// Usage:
await withSpinner('Installing dependencies...', async (spinner) => {
  await installDeps();
  spinner.text = 'Configuring project...';
  await configure();
});
```

### Multi-Step Progress

```typescript
const steps = [
  { message: 'Creating project structure...', fn: createStructure },
  { message: 'Installing dependencies...', fn: installDeps },
  { message: 'Configuring toolchain...', fn: configure },
  { message: 'Initializing git...', fn: gitInit },
];

for (const [i, step] of steps.entries()) {
  const prefix = `[${i + 1}/${steps.length}]`;
  await withSpinner(`${prefix} ${step.message}`, step.fn);
}
```

---

## Tables

```typescript
import Table from 'cli-table3';
import { theme } from './ui/theme.js';

const table = new Table({
  head: [
    theme.primary('Command'),
    theme.primary('Description'),
  ],
  style: { head: [], border: [] },
});

table.push(
  ['init', 'Create a new project'],
  ['build', 'Build for production'],
  ['serve', 'Start dev server'],
);

console.log(table.toString());
```

---

## Configuration Management

```typescript
// src/lib/config.ts
import { readFile } from 'fs/promises';
import { resolve } from 'path';

type Config = {
  output: string;
  template: string;
  features: string[];
};

const DEFAULT_CONFIG: Config = {
  output: 'dist',
  template: 'default',
  features: [],
};

const CONFIG_FILES = [
  'mytool.config.json',
  '.mytoolrc.json',
  '.mytoolrc',
];

export const loadConfig = async (cwd = process.cwd()): Promise<Config> => {
  for (const file of CONFIG_FILES) {
    try {
      const content = await readFile(resolve(cwd, file), 'utf-8');
      const parsed = JSON.parse(content) as Partial<Config>;
      return { ...DEFAULT_CONFIG, ...parsed };
    } catch {
      continue;
    }
  }
  return DEFAULT_CONFIG;
};
```

---

## Error Handling

```typescript
// src/lib/errors.ts
export class CliError extends Error {
  constructor(
    message: string,
    public readonly exitCode: number = 1,
    public readonly hint?: string,
  ) {
    super(message);
    this.name = 'CliError';
  }
}

// In entry point:
const run = async (): Promise<void> => {
  try {
    await program.parseAsync();
  } catch (error) {
    if (error instanceof CliError) {
      console.error(theme.error(`\n  Error: ${error.message}`));
      if (error.hint) {
        console.error(theme.dim(`  Hint: ${error.hint}`));
      }
      process.exit(error.exitCode);
    }
    // Unknown errors
    console.error(theme.error('\n  Unexpected error occurred'));
    if (process.env.VERBOSE) {
      console.error(error);
    } else {
      console.error(theme.dim('  Run with --verbose for details'));
    }
    process.exit(1);
  }
};

run();
```

---

## Testing CLIs

### Vitest Setup

```typescript
// tests/commands/init.test.ts
import { describe, it, expect, vi } from 'vitest';
import { execSync } from 'child_process';

describe('init command', () => {
  it('creates project with default template', () => {
    const result = execSync(
      'tsx src/index.ts init test-project --yes',
      { encoding: 'utf-8', cwd: tmpDir },
    );
    expect(result).toContain('Project created');
  });
});
```

### Testing Output

```typescript
// Capture stdout for assertions
const { stdout, stderr, exitCode } = await exec('my-cli --version');
expect(stdout.trim()).toMatch(/^\d+\.\d+\.\d+$/);
expect(exitCode).toBe(0);
```

---

## Distribution

### npm Publish

```json
{
  "name": "@scope/my-cli",
  "bin": { "my-cli": "./bin/cli.js" },
  "files": ["bin/", "dist/", "README.md"],
  "publishConfig": { "access": "public" }
}
```

```bash
npm run build
npm publish
# Users: npx @scope/my-cli init
```

### Standalone Binary (pkg / esbuild)

```bash
# Bundle with esbuild
npx esbuild src/index.ts --bundle --platform=node --outfile=dist/cli.cjs

# Or create native binaries
npx pkg dist/cli.cjs -t node18-win-x64,node18-macos-x64,node18-linux-x64
```
