"""init command — interactive project scaffolding."""

from __future__ import annotations

import typer
import questionary
from questionary import Style as QStyle
from rich.console import Console
from rich.panel import Panel
from rich import box

from projinit.ui.banner import show_banner, show_status_line
from projinit.ui.theme import CLI_THEME, PROMPT_STYLE
from projinit.ui.progress import install_with_progress, step
from projinit.lib.core import (
    TEMPLATES,
    create_project_structure,
    get_template_packages,
    validate_project_name,
)

console = Console(theme=CLI_THEME)
qstyle = QStyle(PROMPT_STYLE)


def _prompt_template() -> str:
    """Interactively select a project template."""
    choices = [
        questionary.Choice(
            title=f"{t.display_name} -- {t.description}",
            value=t.name,
        )
        for t in TEMPLATES.values()
    ]

    result = questionary.select(
        "Choose a project template:",
        choices=choices,
        style=qstyle,
    ).ask()

    if result is None:
        raise typer.Abort()

    return result


def _prompt_project_name() -> str:
    """Interactively ask for the project name with validation."""
    result = questionary.text(
        "Project name:",
        default="my-project",
        validate=lambda v: validate_project_name(v) or "Invalid name. Use lowercase letters, numbers, and hyphens only.",
        style=qstyle,
    ).ask()

    if result is None:
        raise typer.Abort()

    return result


def _confirm_settings(name: str, template: str, install: bool) -> bool:
    """Display summary and ask for confirmation."""
    tpl = TEMPLATES[template]
    packages = get_template_packages(template)

    console.print()
    console.print("[heading]Project Summary[/heading]")
    show_status_line(
        {
            "Name": f"[cyan]{name}[/cyan]",
            "Template": f"[cyan]{tpl.display_name}[/cyan]",
            "Packages": f"[cyan]{len(packages)}[/cyan] dependencies",
            "Install": "[green]yes[/green]" if install else "[yellow]no[/yellow]",
        }
    )

    result = questionary.confirm(
        "Proceed with these settings?",
        default=True,
        style=qstyle,
    ).ask()

    if result is None:
        raise typer.Abort()

    return result


def run_init_interactive(verbose: bool = False) -> None:
    """Full interactive flow — banner, prompts, scaffold, install."""
    show_banner()

    template = _prompt_template()
    name = _prompt_project_name()

    if not _confirm_settings(name, template, install=True):
        console.print("[dim]Aborted.[/dim]")
        raise typer.Exit()

    _execute_scaffold(name=name, template=template, install=True, verbose=verbose)


def run_init(
    name: str | None = None,
    template: str | None = None,
    install: bool = True,
    skip_confirm: bool = False,
) -> None:
    """Init command handler — supports both interactive and non-interactive modes."""
    show_banner()

    if template is None:
        template = _prompt_template()

    if template not in TEMPLATES:
        console.print(f"[error]Unknown template:[/error] {template}")
        console.print(f"[dim]Available: {', '.join(TEMPLATES.keys())}[/dim]")
        raise typer.Exit(1)

    if name is None:
        name = _prompt_project_name()

    if not validate_project_name(name):
        console.print(
            "[error]Invalid project name.[/error] Use lowercase letters, numbers, and hyphens only."
        )
        raise typer.Exit(1)

    if not skip_confirm:
        if not _confirm_settings(name, template, install):
            console.print("[dim]Aborted.[/dim]")
            raise typer.Exit()

    _execute_scaffold(name=name, template=template, install=install, verbose=False)


def _execute_scaffold(
    name: str,
    template: str,
    install: bool,
    verbose: bool,
) -> None:
    """Run the actual scaffolding steps with progress display."""
    total_steps = 4 if install else 3
    current = 0

    console.print()

    # Step 1: Create directory structure
    current += 1
    with step("Creating project structure", total_steps, current):
        create_project_structure(name, template)

    # Step 2: Generate configuration files
    current += 1
    with step("Generating configuration files", total_steps, current):
        from projinit.lib.core import write_config_files

        write_config_files(name, template)

    # Step 3: Initialize git repository
    current += 1
    with step("Initializing git repository", total_steps, current):
        from projinit.lib.core import init_git_repo

        init_git_repo(name)

    # Step 4: Install dependencies
    if install:
        current += 1
        console.print(f"  [dim][{current}/{total_steps}][/dim] Installing dependencies...")
        packages = get_template_packages(template)
        install_with_progress(packages, description="  Installing")

    # Done!
    console.print()
    console.print(
        Panel(
            f"[success]Project [bold]{name}[/bold] created successfully![/success]\n\n"
            f"[bold]Next steps:[/bold]\n"
            f"  [cyan]cd {name}[/cyan]\n"
            f"  [cyan]python -m venv .venv[/cyan]\n"
            f"  [cyan]source .venv/bin/activate[/cyan]  [dim]# or .venv\\Scripts\\activate on Windows[/dim]\n"
            f"  [cyan]pip install -e .[/cyan]",
            title="\u2728 Done",
            border_style="green",
            box=box.ROUNDED,
        )
    )
