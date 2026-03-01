# Python CLI — Full Reference

## Table of Contents

1. [Project Scaffolding](#project-scaffolding)
2. [Pyproject.toml Configuration](#pyprojecttoml-configuration)
3. [Command Routing with Typer](#command-routing-with-typer)
4. [Alternative: Click](#alternative-click)
5. [Rich Output](#rich-output)
6. [ASCII Banners with Pyfiglet](#ascii-banners-with-pyfiglet)
7. [Interactive Prompts](#interactive-prompts)
8. [Progress Indicators](#progress-indicators)
9. [Tables & Panels](#tables--panels)
10. [Configuration Management](#configuration-management)
11. [Error Handling](#error-handling)
12. [Testing CLIs](#testing-clis)
13. [Distribution](#distribution)

---

## Project Scaffolding

```bash
mkdir my-cli && cd my-cli
python -m venv .venv

# Activate (OS-dependent)
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# Install deps
pip install typer rich pyfiglet questionary
pip install -e ".[dev]"          # After setting up pyproject.toml
```

### Directory Layout

```
my-cli/
├── src/
│   └── my_cli/
│       ├── __init__.py          # Version etc.
│       ├── __main__.py          # python -m my_cli
│       ├── cli.py               # Typer app + command router
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── banner.py        # ASCII art + branding
│       │   ├── theme.py         # Rich style definitions
│       │   └── spinner.py       # Progress wrappers
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── init.py
│       │   ├── build.py
│       │   └── serve.py
│       └── lib/
│           ├── __init__.py
│           ├── config.py        # Config loading
│           └── core.py          # Business logic
├── tests/
│   ├── conftest.py
│   ├── test_cli.py
│   └── test_core.py
├── pyproject.toml
└── README.md
```

---

## Pyproject.toml Configuration

```toml
[project]
name = "my-cli"
version = "1.0.0"
description = "What this CLI does"
requires-python = ">=3.10"
dependencies = [
    "typer>=0.9",
    "rich>=13",
    "pyfiglet>=1.0",
    "questionary>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7",
    "pytest-cov",
]

[project.scripts]
my-cli = "my_cli.cli:app"

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.setuptools.packages.find]
where = ["src"]
```

**__main__.py** (for `python -m my_cli`):

```python
from my_cli.cli import app

app()
```

---

## Command Routing with Typer

### Basic Setup

```python
# cli.py
import typer
from typing import Optional
from rich.console import Console

app = typer.Typer(
    help="What this CLI does",
    no_args_is_help=True,
    rich_markup_mode="rich",
)
console = Console()
```

### Subcommands

```python
@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    template: str = typer.Option("default", "--template", "-t", help="Template"),
    no_install: bool = typer.Option(False, "--no-install", help="Skip deps"),
) -> None:
    """Initialize a new project."""
    from .commands.init import run_init
    run_init(name=name, template=template, install=not no_install)


@app.command()
def build(
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch mode"),
    output: str = typer.Option("dist", "--output", "-o", help="Output dir"),
) -> None:
    """Build the project for production."""
    from .commands.build import run_build
    run_build(watch=watch, output=output)
```

### Command Groups

```python
# Group related commands
db_app = typer.Typer(help="Database operations")
app.add_typer(db_app, name="db")

@db_app.command("migrate")
def db_migrate() -> None:
    """Run database migrations."""
    ...

@db_app.command("seed")
def db_seed() -> None:
    """Seed the database."""
    ...

# Usage: my-cli db migrate
```

### Callback (Banner + Global Options)

```python
@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose"),
    version: bool = typer.Option(False, "--version", "-V", help="Show version"),
) -> None:
    """My CLI - tool description."""
    if version:
        from . import __version__
        console.print(f"my-cli v{__version__}")
        raise typer.Exit()

    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    if ctx.invoked_subcommand is None:
        from .ui.banner import show_banner
        show_banner()
        console.print("Run [bold]my-cli --help[/bold] to see available commands.")
```

---

## Alternative: Click

For more control or complex nested commands, use Click directly:

```python
import click
from rich.console import Console

console = Console()

@click.group()
@click.option("--verbose", "-v", is_flag=True)
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """My CLI tool."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

@cli.command()
@click.argument("name")
@click.option("--template", "-t", default="default")
def init(name: str, template: str) -> None:
    """Initialize a new project."""
    ...

if __name__ == "__main__":
    cli()
```

---

## Rich Output

### Theme Definition

```python
# ui/theme.py
from rich.theme import Theme
from rich.style import Style

CLI_THEME = Theme({
    "primary": Style(color="cyan"),
    "secondary": Style(color="magenta"),
    "success": Style(color="green", bold=True),
    "warning": Style(color="yellow"),
    "error": Style(color="red", bold=True),
    "info": Style(color="blue"),
    "dim": Style(dim=True),
    "heading": Style(color="cyan", bold=True, underline=True),
    "code": Style(color="bright_black", bgcolor="grey11"),
})

# Use in console
from rich.console import Console
console = Console(theme=CLI_THEME)

# Now use named styles:
console.print("Done!", style="success")
console.print("Warning: file exists", style="warning")
```

### Styled Output Patterns

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

# Section heading
console.print("\n[heading]Configuration[/heading]")
console.print(f"  [dim]Output:[/dim] [primary]/dist[/primary]")

# Success box
console.print(Panel(
    "[success]Project created successfully![/success]\n\n"
    "Next steps:\n"
    "  cd my-project\n"
    "  npm install\n"
    "  npm run dev",
    title="Done",
    border_style="green",
    box=box.ROUNDED,
))

# Key-value display
def show_status(items: dict[str, str]) -> None:
    max_key = max(len(k) for k in items)
    for key, value in items.items():
        console.print(f"  [dim]{key:<{max_key}}[/dim]  {value}")
```

---

## ASCII Banners with Pyfiglet

### Banner Module

```python
# ui/banner.py
from pyfiglet import figlet_format
from rich.console import Console
from rich.text import Text

console = Console()

def show_banner(
    name: str = "MY CLI",
    version: str = "1.0.0",
    tagline: str | None = None,
    font: str = "slant",
) -> None:
    """Display the CLI banner."""
    banner = figlet_format(name, font=font)
    console.print(f"[cyan]{banner}[/cyan]", end="")

    if tagline:
        console.print(f"  [dim]{tagline}[/dim]")

    console.print(f"  [dim]v{version}[/dim]\n")


def show_compact_banner(name: str, version: str) -> None:
    """Compact one-line banner for subcommands."""
    console.print(f"[bold cyan]{name}[/bold cyan] [dim]v{version}[/dim]\n")


def show_status_line(items: dict[str, str]) -> None:
    """PPTX VIBE-style status line."""
    for key, value in items.items():
        console.print(f"  [dim]{key}:[/dim] {value}")
    console.print()
```

### Recommended Fonts

| Font | Style | Best For |
|------|-------|----------|
| `slant` | Italic, elegant | Developer tools |
| `standard` | Clean, readable | General purpose |
| `big` | Large, blocky | Impact |
| `small` | Compact | Narrow terminals |
| `cybermedium` | Techy | Dev/hacker tools |
| `banner3` | Very bold | Title screens |

---

## Interactive Prompts

### Questionary (Recommended)

```python
import questionary
from questionary import Style

custom_style = Style([
    ("qmark", "fg:cyan bold"),
    ("question", "bold"),
    ("answer", "fg:cyan"),
    ("pointer", "fg:cyan bold"),
    ("highlighted", "fg:cyan bold"),
    ("selected", "fg:cyan"),
])

# Text input
name = questionary.text(
    "Project name:",
    default="my-project",
    validate=lambda v: len(v) > 0 or "Name is required",
    style=custom_style,
).ask()

# Select one
template = questionary.select(
    "Choose a template:",
    choices=["minimal", "standard", "full"],
    style=custom_style,
).ask()

# Multi-select
features = questionary.checkbox(
    "Select features:",
    choices=[
        questionary.Choice("TypeScript", checked=True),
        questionary.Choice("ESLint"),
        questionary.Choice("Prettier"),
        questionary.Choice("Testing"),
    ],
    style=custom_style,
).ask()

# Confirm
proceed = questionary.confirm(
    "Create project with these settings?",
    default=True,
    style=custom_style,
).ask()
```

### Rich Prompts (Simple Cases)

```python
from rich.prompt import Prompt, Confirm

name = Prompt.ask("Project name", default="my-project")
proceed = Confirm.ask("Continue?", default=True)
```

### Non-Interactive Fallback

```python
@app.command()
def init(
    name: str = typer.Argument(...),
    template: str = typer.Option("default"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip prompts"),
) -> None:
    if not yes:
        template = questionary.select("Template:", choices=[...]).ask()
        if not questionary.confirm("Proceed?").ask():
            raise typer.Abort()
    # Continue with values...
```

---

## Progress Indicators

### Rich Progress Bar

```python
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeElapsedColumn(),
) as progress:
    task = progress.add_task("Processing...", total=100)
    for i in range(100):
        do_work(i)
        progress.update(task, advance=1)
```

### Rich Spinner

```python
from rich.console import Console

console = Console()

with console.status("[bold cyan]Installing dependencies...") as status:
    install_deps()
    status.update("[bold cyan]Configuring project...")
    configure()

console.print("[green]Done![/green]")
```

### Multi-Step Progress

```python
from rich.console import Console
from contextlib import contextmanager

console = Console()

@contextmanager
def step(description: str, total_steps: int, current: int):
    prefix = f"[dim][{current}/{total_steps}][/dim]"
    with console.status(f"{prefix} {description}"):
        yield
    console.print(f"{prefix} [green]{description} ... done[/green]")

steps = [
    "Creating project structure",
    "Installing dependencies",
    "Configuring toolchain",
    "Initializing git",
]

for i, desc in enumerate(steps, 1):
    with step(desc, len(steps), i):
        do_step(i)
```

---

## Tables & Panels

```python
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich import box

console = Console()

# Data table
table = Table(
    title="Available Templates",
    box=box.ROUNDED,
    header_style="bold cyan",
)
table.add_column("Name", style="cyan")
table.add_column("Description")
table.add_column("Status", justify="center")

table.add_row("minimal", "Bare essentials", "[green]stable[/green]")
table.add_row("standard", "Recommended setup", "[green]stable[/green]")
table.add_row("full", "Everything included", "[yellow]beta[/yellow]")

console.print(table)

# Info panel
console.print(Panel(
    "[bold]Next steps:[/bold]\n\n"
    "  1. cd my-project\n"
    "  2. pip install -e .\n"
    "  3. my-cli --help",
    title="Project Created",
    border_style="green",
    box=box.ROUNDED,
))
```

---

## Configuration Management

```python
# lib/config.py
from pathlib import Path
from dataclasses import dataclass, field
import json
import tomllib

@dataclass
class Config:
    output: str = "dist"
    template: str = "default"
    features: list[str] = field(default_factory=list)

CONFIG_FILES = [
    "mytool.toml",
    ".mytoolrc.json",
    ".mytoolrc",
    "pyproject.toml",
]

def load_config(cwd: Path | None = None) -> Config:
    cwd = cwd or Path.cwd()

    for name in CONFIG_FILES:
        path = cwd / name
        if not path.exists():
            continue

        if name.endswith(".toml"):
            with open(path, "rb") as f:
                data = tomllib.load(f)
            # Handle pyproject.toml nesting
            if name == "pyproject.toml":
                data = data.get("tool", {}).get("mytool", {})
            return Config(**{k: v for k, v in data.items() if k in Config.__dataclass_fields__})

        if name.endswith(".json") or name == ".mytoolrc":
            data = json.loads(path.read_text())
            return Config(**{k: v for k, v in data.items() if k in Config.__dataclass_fields__})

    return Config()
```

---

## Error Handling

```python
# lib/errors.py
import typer
from rich.console import Console

console = Console(stderr=True)

class CliError(Exception):
    def __init__(self, message: str, hint: str | None = None, exit_code: int = 1):
        super().__init__(message)
        self.hint = hint
        self.exit_code = exit_code

def handle_error(error: Exception, verbose: bool = False) -> None:
    if isinstance(error, CliError):
        console.print(f"\n  [red bold]Error:[/red bold] {error}")
        if error.hint:
            console.print(f"  [dim]Hint: {error.hint}[/dim]")
        raise typer.Exit(error.exit_code)

    console.print("\n  [red bold]Unexpected error occurred[/red bold]")
    if verbose:
        console.print_exception()
    else:
        console.print("  [dim]Run with --verbose for details[/dim]")
    raise typer.Exit(1)
```

---

## Testing CLIs

### Pytest + Typer Testing

```python
# tests/test_cli.py
from typer.testing import CliRunner
from my_cli.cli import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.stdout

def test_init_creates_project(tmp_path):
    result = runner.invoke(app, ["init", "test-project", "--yes"], cwd=tmp_path)
    assert result.exit_code == 0
    assert (tmp_path / "test-project").exists()

def test_init_validates_name():
    result = runner.invoke(app, ["init", "INVALID NAME!!", "--yes"])
    assert result.exit_code != 0
```

### Click Testing

```python
from click.testing import CliRunner
from my_cli.cli import cli

runner = CliRunner()

def test_help():
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
```

---

## Distribution

### PyPI Publish

```bash
pip install build twine
python -m build
twine upload dist/*

# Users:
pip install my-cli
# or
pipx install my-cli   # Isolated install
```

### Standalone Binary (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --onefile src/my_cli/__main__.py --name my-cli
# Output: dist/my-cli (or dist/my-cli.exe on Windows)
```

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install .
ENTRYPOINT ["my-cli"]
```
