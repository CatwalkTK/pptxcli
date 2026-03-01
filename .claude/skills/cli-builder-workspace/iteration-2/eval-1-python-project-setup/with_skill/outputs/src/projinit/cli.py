"""Command router for projinit CLI.

This is the thin entry-point layer that wires Typer commands to the
appropriate command handlers.  Business logic lives in ``lib/`` and
presentation helpers live in ``ui/``.
"""

from __future__ import annotations

import typer
from rich.console import Console

from projinit.ui.theme import CLI_THEME

app = typer.Typer(
    help="Interactive project scaffolding CLI",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

console = Console(theme=CLI_THEME)


# ---------------------------------------------------------------------------
# Global callback -- banner, --version, --verbose
# ---------------------------------------------------------------------------

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    version: bool = typer.Option(False, "--version", "-V", help="Show version and exit"),
) -> None:
    """projinit -- Interactive Project Scaffolding CLI."""
    if version:
        from projinit import __version__
        console.print(f"projinit v{__version__}")
        raise typer.Exit()

    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    if ctx.invoked_subcommand is None:
        from projinit.ui.banner import show_banner, show_status_line
        show_banner()
        show_status_line()
        console.print("  Run [bold]projinit --help[/bold] to see available commands.\n")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

@app.command()
def init(
    name: str | None = typer.Argument(
        None,
        help="Project name (prompted if omitted)",
    ),
    template: str | None = typer.Option(
        None,
        "--template",
        "-t",
        help="Template to use: minimal, standard, or full",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation prompt (non-interactive / CI mode)",
    ),
) -> None:
    """Initialize a new project interactively.

    Choose a template ([cyan]minimal[/cyan] / [cyan]standard[/cyan] /
    [cyan]full[/cyan]), enter a project name, and watch dependencies
    install with a progress bar.
    """
    from projinit.commands.init_project import run_init
    from projinit.lib.errors import handle_error

    try:
        run_init(template=template, name=name, yes=yes)
    except Exception as exc:
        handle_error(exc, verbose=False)
