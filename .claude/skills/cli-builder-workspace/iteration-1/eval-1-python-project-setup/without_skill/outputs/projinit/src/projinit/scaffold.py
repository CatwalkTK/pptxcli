"""Project scaffolding: file generation and dependency installation."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.panel import Panel
from rich.tree import Tree
from rich import print as rprint

from projinit.templates.registry import TemplateDef


def _file_progress() -> Progress:
    """Create a Progress instance for file generation."""
    return Progress(
        SpinnerColumn("dots"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=40, style="bright_black", complete_style="bright_cyan", finished_style="green"),
        TaskProgressColumn(),
        TimeElapsedColumn(),
    )


def _install_progress() -> Progress:
    """Create a Progress instance for dependency installation."""
    return Progress(
        SpinnerColumn("dots"),
        TextColumn("[bold magenta]{task.description}"),
        BarColumn(bar_width=40, style="bright_black", complete_style="magenta", finished_style="green"),
        TaskProgressColumn(),
        TimeElapsedColumn(),
    )


def generate_files(
    project_name: str,
    template: TemplateDef,
    base_dir: Path | None = None,
    console: Console | None = None,
) -> Path:
    """Write all template files to disk with a progress bar.

    Args:
        project_name: Name of the project (used as directory name).
        template: The template definition containing files to create.
        base_dir: Parent directory in which to create the project folder.
                  Defaults to the current working directory.
        console: Optional Rich console for output.

    Returns:
        The Path to the created project directory.
    """
    if console is None:
        console = Console()
    if base_dir is None:
        base_dir = Path.cwd()

    project_dir = base_dir / project_name
    total_files = len(template.files)

    console.print()
    console.print(f"[bold bright_cyan]  Scaffolding [bright_white]{project_name}[/] "
                  f"with [bright_white]{template.label}[/] template...[/]")
    console.print()

    with _file_progress() as progress:
        task = progress.add_task("Creating files", total=total_files)

        for tfile in template.files:
            file_path = project_dir / tfile.path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(tfile.content, encoding="utf-8")

            progress.update(task, advance=1, description=f"[dim]{tfile.path}[/dim]")
            time.sleep(0.05)  # small delay so the user sees the progress

        progress.update(task, description="[green bold]Files created[/]")

    _print_tree(project_dir, template, console)
    return project_dir


def _print_tree(project_dir: Path, template: TemplateDef, console: Console) -> None:
    """Display a tree view of the generated project structure."""
    tree = Tree(
        f"[bold bright_cyan]{project_dir.name}/[/]",
        guide_style="bright_black",
    )

    dirs_added: dict[str, Tree] = {}

    for tfile in sorted(template.files, key=lambda f: f.path):
        parts = tfile.path.split("/")
        parent = tree
        for i, part in enumerate(parts[:-1]):
            key = "/".join(parts[: i + 1])
            if key not in dirs_added:
                dirs_added[key] = parent.add(f"[bold blue]{part}/[/]")
            parent = dirs_added[key]

        filename = parts[-1]
        parent.add(f"[green]{filename}[/]")

    console.print()
    console.print(tree)
    console.print()


def install_dependencies(
    project_dir: Path,
    template: TemplateDef,
    console: Console | None = None,
) -> bool:
    """Install project dependencies with a progress bar.

    Args:
        project_dir: Path to the generated project directory.
        template: The template definition with dependency lists.
        console: Optional Rich console for output.

    Returns:
        True if installation succeeded, False otherwise.
    """
    if console is None:
        console = Console()

    all_deps = [*template.dependencies, *template.dev_dependencies]
    if not all_deps:
        console.print("[dim]No dependencies to install.[/dim]")
        return True

    console.print()
    console.print("[bold magenta]  Installing dependencies...[/]")
    console.print()

    total = len(all_deps)

    with _install_progress() as progress:
        task = progress.add_task("Installing packages", total=total)

        for dep in all_deps:
            progress.update(task, description=f"[dim]pip install {dep}[/dim]")

            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep, "--quiet"],
                    cwd=str(project_dir),
                    capture_output=True,
                    text=True,
                    check=True,
                )
            except subprocess.CalledProcessError as exc:
                progress.update(task, description=f"[red bold]Failed: {dep}[/]")
                console.print(f"\n[red]Error installing {dep}:[/red]\n{exc.stderr}")
                return False

            progress.update(task, advance=1)

        progress.update(task, description="[green bold]All packages installed[/]")

    console.print()
    return True


def print_summary(
    project_name: str,
    project_dir: Path,
    template: TemplateDef,
    installed: bool,
    console: Console | None = None,
) -> None:
    """Print the final success summary."""
    if console is None:
        console = Console()

    lines = [
        f"[bold bright_white]{project_name}[/] created successfully!",
        "",
        f"  [dim]Template:[/]  {template.label}",
        f"  [dim]Location:[/] {project_dir}",
    ]

    if installed:
        lines.append("  [dim]Deps:[/]     Installed")
    else:
        lines.append("  [dim]Deps:[/]     Skipped (run [bold]pip install -e \".[dev]\"[/] later)")

    lines.extend([
        "",
        "[bold bright_cyan]Next steps:[/]",
        f"  cd {project_name}",
    ])

    if not installed:
        lines.append('  pip install -e ".[dev]"')

    if template.name in ("standard", "full"):
        lines.append("  make test")

    panel = Panel(
        "\n".join(lines),
        title="[bold green]  Done!  [/]",
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)
    console.print()
