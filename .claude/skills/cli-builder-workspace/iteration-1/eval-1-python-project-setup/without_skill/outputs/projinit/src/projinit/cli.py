"""CLI entry point for projinit."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console

from projinit.banner import display_banner
from projinit.prompts import gather_inputs
from projinit.scaffold import generate_files, install_dependencies, print_summary


@click.command()
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(file_okay=False, resolve_path=True),
    default=".",
    help="Parent directory for the new project (default: current directory).",
)
@click.option(
    "--no-banner",
    is_flag=True,
    default=False,
    help="Skip the startup banner.",
)
def main(output_dir: str, no_banner: bool) -> None:
    """projinit -- Interactive project scaffolding CLI.

    Guides you through template selection, project naming, and optional
    dependency installation to bootstrap a new Python project in seconds.
    """
    console = Console()

    if not no_banner:
        display_banner(console)

    try:
        project_name, template, should_install = gather_inputs()
    except KeyboardInterrupt:
        console.print("\n[yellow]Aborted.[/yellow]")
        sys.exit(1)

    base_dir = Path(output_dir)
    target = base_dir / project_name

    if target.exists():
        console.print(f"\n[red bold]Error:[/] Directory [bright_white]{target}[/] already exists.")
        sys.exit(1)

    project_dir = generate_files(project_name, template, base_dir=base_dir, console=console)

    installed = False
    if should_install:
        installed = install_dependencies(project_dir, template, console=console)

    print_summary(project_name, project_dir, template, installed, console=console)


if __name__ == "__main__":
    main()
