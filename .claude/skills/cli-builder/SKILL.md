---
name: cli-builder
description: "Build professional interactive CLI applications with polished UX — ASCII art banners, colored output, interactive prompts, subcommand routing, progress indicators, and status lines. Use this skill whenever the user wants to create a CLI tool, command-line application, terminal utility, console program, or any tool that runs in the terminal with subcommands, flags, or interactive prompts. Trigger keywords: 'CLI', 'command line', 'terminal app', 'console tool', 'subcommand', 'argparse', 'commander', 'typer', 'click'. Also trigger when the user asks to add a banner, styled output, progress bar, or interactive menu to a script, or says things like 'make it look nice in the terminal', 'ターミナルで動くツール', 'コマンドラインツール'. Supports both Node.js/TypeScript and Python. Does NOT apply to: REST APIs, web frontends, shell one-liners, CI/CD pipelines, GUI applications, or simple scripts without user interaction."
---

# CLI Builder

Build production-grade CLI applications with delightful terminal UX. This skill covers the full journey from project scaffolding to polished, distributable CLI tools.

## Design Philosophy

A great CLI feels like a conversation, not a command. It greets you, guides you, shows progress, and handles errors gracefully. Think of the experience when you run `npm create vite@latest` or `npx create-next-app` — that's the bar.

The PPTX VIBE style is a good reference for what "personality" looks like in a CLI:

```
 ██████  ██████  ████████ ██   ██
 ██   ██ ██   ██    ██     ██ ██
 ██████  ██████     ██      ███
 ██      ██         ██     ██ ██
 ██      ██         ██    ██   ██
  ░▒▓█ Tool Name █▓▒░
```

Followed by a status line showing current context. This pattern — banner, context, then action — creates a professional feel.

## Decision: Node.js or Python?

Ask the user which stack to use if unclear. Here's a quick guide:

| Factor | Node.js/TypeScript | Python |
|--------|-------------------|--------|
| Best for | npm-distributed tools, JS ecosystem | Data tools, system scripts, ML pipelines |
| Banner lib | `figlet` + `chalk` | `pyfiglet` + `rich` |
| Prompts | `@inquirer/prompts` | `questionary` or `rich.prompt` |
| Parsing | `commander` or `yargs` | **`typer`** (preferred) or `click` |
| Progress | `ora`, `cli-progress` | `rich.progress`, `tqdm` |
| Tables | `cli-table3` | `rich.table` |
| Distribution | `npm publish`, `npx` | `pip install`, `pipx` |

## Architecture Pattern

Every CLI built with this skill follows this layered structure:

```
┌─────────────────────────────────┐
│  Presentation Layer             │  Banner, colors, prompts, spinners
├─────────────────────────────────┤
│  Command Router                 │  Subcommands, args, flags, help
├─────────────────────────────────┤
│  Business Logic                 │  Core functionality (imported modules)
├─────────────────────────────────┤
│  I/O Layer                      │  File system, network, config
└─────────────────────────────────┘
```

Separate these concerns from the start. **Always create `ui/`, `commands/`, and `lib/` directories** — this isn't optional, it's the core of maintainable CLI architecture. The command router should be thin — it parses input, calls business logic, and formats output. Business logic should never import chalk/rich or print directly.

For Node.js projects, **always use TypeScript** — it catches argument type errors at build time and makes refactoring safe. For Python projects, **prefer typer over click** — typer uses type annotations for argument parsing, which means less boilerplate and better IDE support.

## Node.js/TypeScript CLI

Read `references/nodejs-cli.md` for the full guide. Here's the quick-start:

### Project Setup

```bash
mkdir my-cli && cd my-cli
npm init -y
npm install commander chalk figlet @inquirer/prompts ora cli-table3
npm install -D typescript @types/node tsx
```

### Minimal Structure

```
my-cli/
├── src/
│   ├── index.ts          # Entry point + command router
│   ├── ui/
│   │   ├── banner.ts     # ASCII art banner
│   │   ├── theme.ts      # Color palette
│   │   └── spinner.ts    # Progress indicators
│   ├── commands/
│   │   ├── init.ts       # Each command is a module
│   │   └── build.ts
│   └── lib/
│       └── core.ts       # Business logic (no UI imports)
├── package.json
├── tsconfig.json
└── bin/
    └── cli.js            # Shim: #!/usr/bin/env node
```

### Entry Point Pattern

```typescript
#!/usr/bin/env node
import { Command } from 'commander';
import chalk from 'chalk';
import figlet from 'figlet';

const showBanner = (): void => {
  const banner = figlet.textSync('MY CLI', { font: 'ANSI Shadow' });
  console.log(chalk.cyan(banner));
  console.log(chalk.dim('  v1.0.0 — Your tool description'));
  console.log();
};

const program = new Command()
  .name('my-cli')
  .version('1.0.0')
  .description('What this CLI does')
  .hook('preAction', () => showBanner());

program
  .command('init')
  .description('Initialize a new project')
  .option('-t, --template <name>', 'template to use', 'default')
  .action(async (opts) => {
    // Delegate to command handler
    const { runInit } = await import('./commands/init.js');
    await runInit(opts);
  });

program.parse();
```

### Color Theme Pattern

```typescript
// src/ui/theme.ts
import chalk from 'chalk';

export const theme = {
  primary: chalk.cyan,
  success: chalk.green,
  warning: chalk.yellow,
  error: chalk.red,
  dim: chalk.dim,
  bold: chalk.bold,
  heading: chalk.cyan.bold,
  highlight: chalk.magenta,
} as const;
```

### Interactive Prompts

```typescript
import { select, input, confirm } from '@inquirer/prompts';

const template = await select({
  message: 'Choose a template:',
  choices: [
    { name: 'Minimal', value: 'minimal', description: 'Bare essentials' },
    { name: 'Full', value: 'full', description: 'All features included' },
  ],
});

const name = await input({
  message: 'Project name:',
  validate: (v) => v.length > 0 || 'Name is required',
});

const proceed = await confirm({ message: 'Create project?' });
```

### Progress Indicator

```typescript
import ora from 'ora';

const spinner = ora('Installing dependencies...').start();
try {
  await installDeps();
  spinner.succeed('Dependencies installed');
} catch (e) {
  spinner.fail('Installation failed');
  throw e;
}
```

## Python CLI

Read `references/python-cli.md` for the full guide. Here's the quick-start:

### Project Setup

```bash
mkdir my-cli && cd my-cli
python -m venv .venv && source .venv/bin/activate
pip install typer rich pyfiglet questionary
```

### Minimal Structure

```
my-cli/
├── src/
│   └── my_cli/
│       ├── __init__.py
│       ├── __main__.py   # Entry: python -m my_cli
│       ├── cli.py        # Command router (Typer app)
│       ├── ui/
│       │   ├── banner.py
│       │   └── theme.py
│       ├── commands/
│       │   ├── init.py
│       │   └── build.py
│       └── lib/
│           └── core.py   # Business logic
├── pyproject.toml
└── tests/
```

### Entry Point Pattern

```python
# cli.py
import typer
from rich.console import Console
from pyfiglet import figlet_format

app = typer.Typer(help="What this CLI does")
console = Console()

def show_banner() -> None:
    banner = figlet_format("MY CLI", font="slant")
    console.print(f"[cyan]{banner}[/cyan]")
    console.print("[dim]  v1.0.0 — Your tool description[/dim]\n")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        show_banner()
        raise typer.Exit()

@app.command()
def init(
    template: str = typer.Option("default", help="Template to use"),
    name: str = typer.Option(..., prompt="Project name"),
) -> None:
    """Initialize a new project."""
    show_banner()
    from .commands.init import run_init
    run_init(template=template, name=name)
```

### Rich Output

```python
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.panel import Panel

console = Console()

# Tables
table = Table(title="Available Templates")
table.add_column("Name", style="cyan")
table.add_column("Description")
table.add_row("minimal", "Bare essentials")
table.add_row("full", "All features included")
console.print(table)

# Progress
for item in track(items, description="Processing..."):
    process(item)

# Panels
console.print(Panel("Project created!", title="Success", style="green"))
```

## Common Patterns (Both Stacks)

### 1. Configuration File

Support `<tool>.config.json` or `.<tool>rc` in the project root:

```typescript
// Node.js
import { cosmiconfig } from 'cosmiconfig';
const explorer = cosmiconfig('mytool');
const config = await explorer.search();
```

```python
# Python
from pathlib import Path
import tomllib

def load_config() -> dict:
    for name in ["mytool.toml", ".mytoolrc", "pyproject.toml"]:
        path = Path(name)
        if path.exists():
            return tomllib.loads(path.read_text())
    return {}
```

### 2. Error Handling

Never show raw stack traces to users. Catch known errors and display friendly messages:

```typescript
// Node.js
process.on('uncaughtException', (err) => {
  console.error(theme.error(`\n  Error: ${err.message}`));
  console.error(theme.dim('  Run with --verbose for details'));
  process.exit(1);
});
```

```python
# Python
@app.callback()
def main():
    try:
        ...
    except KnownError as e:
        console.print(f"[red]Error:[/red] {e.message}")
        raise typer.Exit(1)
```

### 3. Status Line Pattern (PPTX VIBE Style)

After the banner, show a brief status summary:

```
  ░▒▓█ Tool Name █▓▒░

  Config:    ~/.mytool/config.json
  Output:    ./dist/
  Available: init | build | deploy | help
```

### 4. Help Text

Invest in clear, example-rich help:

```
USAGE
  $ my-cli init [--template <name>]

EXAMPLES
  $ my-cli init                    # Interactive mode
  $ my-cli init --template full    # Use full template
  $ my-cli init --name my-project  # Skip name prompt
```

### 5. ASCII Banner Generator Script

Use `scripts/generate_banner.py` to preview different figlet fonts for your CLI name. Run it to explore options before committing to a font.

## Testing Your CLI

Write tests from the start — CLI tools are easy to test because they have clear inputs and outputs.

**Node.js** (vitest or jest):
```typescript
import { execSync } from 'child_process';

test('--version shows version', () => {
  const output = execSync('npx tsx src/index.ts --version').toString();
  expect(output.trim()).toMatch(/\d+\.\d+\.\d+/);
});

test('convert command works', () => {
  const output = execSync('npx tsx src/index.ts convert test.csv').toString();
  expect(output).toContain('Success');
});
```

**Python** (pytest + typer.testing):
```python
from typer.testing import CliRunner
from my_cli.cli import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0

def test_init_command():
    result = runner.invoke(app, ["init", "--name", "test-proj", "--no-install"])
    assert result.exit_code == 0
    assert "test-proj" in result.stdout
```

## Checklist

Before shipping, verify:

- [ ] Banner displays correctly (test narrow terminals: 80 cols)
- [ ] `--help` works for every command and subcommand
- [ ] `--version` shows current version
- [ ] Errors show friendly messages, not stack traces
- [ ] Colors degrade gracefully (`NO_COLOR` env var support)
- [ ] Interactive prompts have sensible defaults
- [ ] Non-interactive mode works (for CI/piping): `--yes` / `--no-input`
- [ ] Exit codes are meaningful (0 = success, 1 = error, 2 = usage)
- [ ] Config file is documented
- [ ] README includes install + usage examples
- [ ] Basic tests exist for each command

## Resources

- `references/nodejs-cli.md` — Full Node.js/TypeScript CLI guide with advanced patterns
- `references/python-cli.md` — Full Python CLI guide with advanced patterns
- `scripts/generate_banner.py` — Preview ASCII art fonts for your banner
- `templates/` — Starter project templates
