"""Project scaffolding engine for projinit."""

from __future__ import annotations

import os
import re
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

from projinit.templates import Template


def validate_project_name(name: str) -> str | None:
    """Validate a project name.

    Args:
        name: The project name to validate.

    Returns:
        Error message if invalid, None if valid.
    """
    if not name:
        return "Project name cannot be empty."
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
        return "Name must start with a letter and contain only letters, numbers, hyphens, or underscores."
    if len(name) > 64:
        return "Project name must be 64 characters or fewer."
    return None


def _render_content(content: str, project_name: str) -> str:
    """Replace template placeholders with actual values.

    Args:
        content: Template string with {{project_name}} placeholders.
        project_name: The actual project name.

    Returns:
        Rendered string.
    """
    return content.replace("{{project_name}}", project_name)


def create_project(
    project_name: str,
    template: Template,
    target_dir: Path | None = None,
    console: Console | None = None,
) -> Path:
    """Scaffold a new project from a template.

    Args:
        project_name: Name of the project to create.
        template: Template configuration to use.
        target_dir: Parent directory for the project. Defaults to cwd.
        console: Rich console for output. Created if not provided.

    Returns:
        Path to the created project directory.

    Raises:
        FileExistsError: If the project directory already exists.
        ValueError: If the project name is invalid.
    """
    if console is None:
        console = Console()

    validation_error = validate_project_name(project_name)
    if validation_error is not None:
        raise ValueError(validation_error)

    if target_dir is None:
        target_dir = Path.cwd()

    project_path = target_dir / project_name
    if project_path.exists():
        raise FileExistsError(f"Directory already exists: {project_path}")

    total_steps = len(template.directories) + len(template.files) + len(template.dev_dependencies)

    with Progress(
        SpinnerColumn(style="bold cyan"),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40, style="cyan", complete_style="bold green", finished_style="bold green"),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Scaffolding project...", total=total_steps)

        # Create project root
        project_path.mkdir(parents=True, exist_ok=True)

        # Create directories
        for directory in template.directories:
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            progress.update(task, advance=1, description=f"Creating {directory}/")
            time.sleep(0.05)

        # Create files
        for file_path_str, content in template.files.items():
            file_path = project_path / file_path_str
            file_path.parent.mkdir(parents=True, exist_ok=True)
            rendered = _render_content(content, project_name)
            file_path.write_text(rendered, encoding="utf-8")
            progress.update(task, advance=1, description=f"Writing {file_path_str}")
            time.sleep(0.08)

        # Simulate dependency installation
        for dep in template.dev_dependencies:
            progress.update(task, advance=1, description=f"Installing {dep}...")
            time.sleep(0.25)

        progress.update(task, description="[bold green]Done!")

    return project_path


def print_summary(
    project_name: str,
    template: Template,
    project_path: Path,
    console: Console | None = None,
) -> None:
    """Display a summary after project creation.

    Args:
        project_name: Name of the created project.
        template: Template that was used.
        project_path: Path to the created project.
        console: Rich console for output.
    """
    if console is None:
        console = Console()

    console.print()
    console.print("[bold green]  Project created successfully![/]")
    console.print()
    console.print(f"  [bold]Project:[/]   {project_name}")
    console.print(f"  [bold]Template:[/]  {template.display_name}")
    console.print(f"  [bold]Location:[/]  {project_path}")
    console.print()
    console.print("[bold]  Next steps:[/]")
    console.print(f"    [cyan]cd {project_name}[/]")

    if template.name == "minimal":
        console.print("    [cyan]python -m venv .venv[/]")
        console.print("    [cyan]pip install -e .[/]")
    elif template.name == "standard":
        console.print("    [cyan]python -m venv .venv[/]")
        console.print("    [cyan]pip install -e '.[dev]'[/]")
        console.print("    [cyan]pytest[/]")
    elif template.name == "full":
        console.print("    [cyan]python -m venv .venv[/]")
        console.print("    [cyan]make install[/]")
        console.print("    [cyan]make test[/]")

    console.print()
    console.print("  [dim]Happy coding![/dim]")
    console.print()
