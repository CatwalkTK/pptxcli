"""Progress indicators and spinners for projinit CLI."""

from __future__ import annotations

import time
from collections.abc import Sequence
from contextlib import contextmanager
from typing import Generator

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from projinit.ui.theme import CLI_THEME

console = Console(theme=CLI_THEME)


def install_with_progress(packages: Sequence[str]) -> None:
    """Simulate installing dependency packages with a rich progress bar.

    In a real-world scenario this would call ``pip install`` or a similar
    package manager.  Here we simulate per-package work so the progress
    bar visibly advances.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("Installing dependencies...", total=len(packages))
        for pkg in packages:
            progress.update(task, description=f"Installing [cyan]{pkg}[/cyan]...")
            # Simulate work per package
            time.sleep(0.35)
            progress.update(task, advance=1)
        progress.update(task, description="[green]Dependencies installed[/green]")


@contextmanager
def step_context(
    description: str,
    total_steps: int,
    current: int,
) -> Generator[None, None, None]:
    """Context manager that shows a spinner while a step is running,
    then prints a success line when done."""
    prefix = f"[dim][{current}/{total_steps}][/dim]"
    with console.status(f"{prefix} {description}"):
        yield
    console.print(f"  {prefix} [green]{description} ... done[/green]")
