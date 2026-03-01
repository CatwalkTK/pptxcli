"""Command router — Typer app definition and global options."""

import typer
from rich.console import Console

from projinit import __version__

app = typer.Typer(
    help="Interactive project scaffolding CLI with template selection and polished UX.",
    no_args_is_help=False,
    rich_markup_mode="rich",
)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    version: bool = typer.Option(False, "--version", "-V", help="Show version and exit"),
) -> None:
    """projinit - Scaffold new projects interactively."""
    if version:
        console.print(f"projinit v{__version__}")
        raise typer.Exit()

    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    if ctx.invoked_subcommand is None:
        from projinit.commands.init import run_init_interactive

        run_init_interactive(verbose=verbose)


@app.command()
def init(
    name: str = typer.Option(None, "--name", "-n", help="Project name (skip prompt)"),
    template: str = typer.Option(
        None, "--template", "-t", help="Template: minimal, standard, or full"
    ),
    no_install: bool = typer.Option(False, "--no-install", help="Skip dependency installation"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts"),
) -> None:
    """Initialize a new project from a template."""
    from projinit.commands.init import run_init

    run_init(name=name, template=template, install=not no_install, skip_confirm=yes)


@app.command()
def templates() -> None:
    """List available project templates."""
    from projinit.commands.templates import run_templates

    run_templates()
