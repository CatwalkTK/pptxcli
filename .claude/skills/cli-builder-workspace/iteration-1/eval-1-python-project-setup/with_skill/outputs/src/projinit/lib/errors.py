"""Custom error types and global error handler."""

from __future__ import annotations

import typer
from rich.console import Console

console = Console(stderr=True)


class CliError(Exception):
    """A user-facing error with an optional hint and exit code."""

    def __init__(
        self,
        message: str,
        hint: str | None = None,
        exit_code: int = 1,
    ) -> None:
        super().__init__(message)
        self.hint = hint
        self.exit_code = exit_code


def handle_error(error: Exception, verbose: bool = False) -> None:
    """Pretty-print an error to stderr and exit.

    * ``CliError`` instances show a friendly message + optional hint.
    * Unknown errors show a generic message (use ``--verbose`` for traceback).
    """
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
