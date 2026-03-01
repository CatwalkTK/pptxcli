"""Progress indicators — bars, spinners, and multi-step displays."""

from __future__ import annotations

import time
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


def create_progress() -> Progress:
    """Create a rich Progress bar with spinner, bar, percentage, and elapsed time."""
    return Progress(
        SpinnerColumn("dots"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    )


def install_with_progress(packages: list[str], description: str = "Installing") -> None:
    """Simulate dependency installation with a progress bar.

    In a real-world scenario this would shell out to pip/npm.
    Here we simulate the work to demonstrate the progress UX.
    """
    with create_progress() as progress:
        task = progress.add_task(f"{description}...", total=len(packages))
        for pkg in packages:
            progress.update(task, description=f"{description} [cyan]{pkg}[/cyan]")
            # Simulate install latency (would be real I/O in production)
            time.sleep(0.35)
            progress.update(task, advance=1)

        progress.update(task, description=f"[green]{description} complete[/green]")


@contextmanager
def step(description: str, total_steps: int, current: int) -> Generator[None, None, None]:
    """Context manager for multi-step progress display.

    Usage::

        with step("Creating structure", 4, 1):
            create_dirs()
    """
    prefix = f"[dim][{current}/{total_steps}][/dim]"
    with console.status(f"{prefix} {description}"):
        yield
    console.print(f"  {prefix} [green]\u2714[/green] {description}")
