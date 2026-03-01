"""Handler for the `projinit init` command.

This module orchestrates the full interactive project initialization flow:
  1. Display the banner
  2. Prompt for template selection
  3. Prompt for project name
  4. Show a summary and confirm
  5. Create the project directory structure
  6. Install dependencies with a progress bar
  7. Show a success panel with next steps
"""

from __future__ import annotations

import questionary
from questionary import Style as QStyle
from rich.console import Console
from rich.panel import Panel
from rich import box

from projinit.ui.theme import CLI_THEME
from projinit.ui.banner import show_compact_banner
from projinit.ui.progress import install_with_progress, step_context
from projinit.lib.templates import TEMPLATES, TemplateConfig
from projinit.lib.scaffold import scaffold_project

console = Console(theme=CLI_THEME)

PROMPT_STYLE = QStyle([
    ("qmark", "fg:cyan bold"),
    ("question", "bold"),
    ("answer", "fg:cyan"),
    ("pointer", "fg:cyan bold"),
    ("highlighted", "fg:cyan bold"),
    ("selected", "fg:cyan"),
])


def run_init(
    *,
    template: str | None = None,
    name: str | None = None,
    yes: bool = False,
) -> None:
    """Execute the interactive project initialization flow.

    Parameters
    ----------
    template:
        Pre-selected template name.  If ``None``, the user will be
        prompted to choose interactively.
    name:
        Pre-supplied project name.  If ``None``, the user will be
        prompted for input.
    yes:
        If ``True``, skip the confirmation prompt (non-interactive /
        CI mode).
    """
    show_compact_banner()

    # --- Step 1: Template selection ---
    if template is None:
        choices = [
            questionary.Choice(
                title=f"{cfg.label}  ({cfg.description})",
                value=key,
            )
            for key, cfg in TEMPLATES.items()
        ]
        template = questionary.select(
            "Choose a project template:",
            choices=choices,
            style=PROMPT_STYLE,
        ).ask()
        if template is None:
            # User pressed Ctrl-C
            console.print("\n[warning]Aborted.[/warning]")
            return

    selected: TemplateConfig = TEMPLATES[template]

    # --- Step 2: Project name ---
    if name is None:
        name = questionary.text(
            "Project name:",
            default="my-project",
            validate=lambda v: True if len(v.strip()) > 0 else "Name is required",
            style=PROMPT_STYLE,
        ).ask()
        if name is None:
            console.print("\n[warning]Aborted.[/warning]")
            return

    name = name.strip()

    # --- Step 3: Summary & confirmation ---
    console.print()
    console.print("  [heading]Project Summary[/heading]")
    console.print(f"  [dim]Name:[/dim]      [primary]{name}[/primary]")
    console.print(f"  [dim]Template:[/dim]  [primary]{selected.label}[/primary]")
    console.print(f"  [dim]Packages:[/dim]  {', '.join(selected.packages)}")
    console.print()

    if not yes:
        proceed = questionary.confirm(
            "Create project with these settings?",
            default=True,
            style=PROMPT_STYLE,
        ).ask()
        if not proceed:
            console.print("\n[warning]Aborted.[/warning]")
            return

    # --- Step 4: Scaffold project ---
    console.print()
    total_steps = 3
    current = 0

    current += 1
    with step_context("Creating project structure", total_steps, current):
        scaffold_project(name=name, template_key=template)

    # --- Step 5: Install dependencies ---
    current += 1
    console.print(f"  [dim][{current}/{total_steps}][/dim] Installing dependencies...")
    install_with_progress(selected.packages)
    console.print(f"  [dim][{current}/{total_steps}][/dim] [green]Installing dependencies ... done[/green]")

    current += 1
    with step_context("Finalizing project", total_steps, current):
        # Placeholder for git init, post-hooks, etc.
        pass

    # --- Step 6: Success panel ---
    console.print()
    console.print(Panel(
        f"[success]Project '{name}' created successfully![/success]\n\n"
        f"Next steps:\n"
        f"  [dim]$[/dim] cd {name}\n"
        f"  [dim]$[/dim] python -m venv .venv && source .venv/bin/activate\n"
        f"  [dim]$[/dim] pip install -e .\n"
        f"  [dim]$[/dim] projinit --help",
        title="[success]Done[/success]",
        border_style="green",
        box=box.ROUNDED,
    ))
