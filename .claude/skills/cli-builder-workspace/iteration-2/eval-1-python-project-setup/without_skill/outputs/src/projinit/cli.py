"""CLI entry point for projinit."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console

from projinit.banner import display_banner
from projinit.prompts import (
    prompt_confirm_creation,
    prompt_project_name,
    prompt_template_selection,
)
from projinit.scaffold import create_project, print_summary
from projinit.templates import get_template


@click.command()
@click.option(
    "--name",
    "-n",
    type=str,
    default=None,
    help="Project name (skips interactive prompt).",
)
@click.option(
    "--template",
    "-t",
    type=click.Choice(["minimal", "standard", "full"]),
    default=None,
    help="Template to use (skips interactive prompt).",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(exists=True, file_okay=False, writable=True),
    default=None,
    help="Parent directory for the new project.",
)
@click.option(
    "--no-confirm",
    is_flag=True,
    default=False,
    help="Skip confirmation prompt.",
)
@click.version_option(version="1.0.0", prog_name="projinit")
def main(
    name: str | None,
    template: str | None,
    output_dir: str | None,
    no_confirm: bool,
) -> None:
    """projinit - Scaffold a new project interactively.

    Create a new project from a template with an interactive wizard,
    or pass --name and --template for non-interactive mode.
    """
    console = Console()

    display_banner(console)

    try:
        # Get project name (interactive or from flag)
        if name is None:
            project_name = prompt_project_name()
        else:
            project_name = name

        # Get template (interactive or from flag)
        if template is None:
            template_name = prompt_template_selection()
        else:
            template_name = template

        selected_template = get_template(template_name)

        # Confirm creation
        if not no_confirm:
            if not prompt_confirm_creation(project_name, selected_template.display_name):
                console.print("\n  [yellow]Aborted.[/yellow]\n")
                sys.exit(0)

        # Determine output directory
        target_dir = Path(output_dir) if output_dir else Path.cwd()

        # Scaffold the project
        console.print()
        project_path = create_project(
            project_name=project_name,
            template=selected_template,
            target_dir=target_dir,
            console=console,
        )

        print_summary(project_name, selected_template, project_path, console)

    except KeyboardInterrupt:
        console.print("\n  [yellow]Cancelled by user.[/yellow]\n")
        sys.exit(130)
    except FileExistsError as exc:
        console.print(f"\n  [bold red]Error:[/] {exc}\n")
        sys.exit(1)
    except ValueError as exc:
        console.print(f"\n  [bold red]Validation Error:[/] {exc}\n")
        sys.exit(1)
    except KeyError as exc:
        console.print(f"\n  [bold red]Error:[/] {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
