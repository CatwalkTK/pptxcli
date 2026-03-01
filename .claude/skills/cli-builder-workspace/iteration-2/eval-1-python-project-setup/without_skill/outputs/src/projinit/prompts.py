"""Interactive prompts for projinit using questionary."""

from __future__ import annotations

import questionary
from questionary import Style

from projinit.templates import get_template_choices

CUSTOM_STYLE = Style(
    [
        ("qmark", "fg:cyan bold"),
        ("question", "fg:white bold"),
        ("answer", "fg:green bold"),
        ("pointer", "fg:cyan bold"),
        ("highlighted", "fg:cyan bold"),
        ("selected", "fg:green"),
        ("separator", "fg:magenta"),
        ("instruction", "fg:white dim"),
        ("text", "fg:white"),
    ]
)


def prompt_project_name(default: str = "") -> str:
    """Prompt the user for a project name.

    Args:
        default: Default value to pre-fill.

    Returns:
        The entered project name.

    Raises:
        KeyboardInterrupt: If the user cancels.
    """
    name = questionary.text(
        "Project name:",
        default=default,
        style=CUSTOM_STYLE,
        validate=lambda val: (
            True
            if val and len(val) <= 64
            else "Please enter a valid project name (1-64 characters)."
        ),
    ).ask()

    if name is None:
        raise KeyboardInterrupt("User cancelled project name input.")

    return name.strip()


def prompt_template_selection() -> str:
    """Prompt the user to select a project template.

    Returns:
        The selected template name.

    Raises:
        KeyboardInterrupt: If the user cancels.
    """
    choices = get_template_choices()
    selection = questionary.select(
        "Select a template:",
        choices=[
            questionary.Choice(title=c["name"], value=c["value"])
            for c in choices
        ],
        style=CUSTOM_STYLE,
        instruction="(Use arrow keys to navigate, Enter to select)",
    ).ask()

    if selection is None:
        raise KeyboardInterrupt("User cancelled template selection.")

    return selection


def prompt_confirm_creation(project_name: str, template_name: str) -> bool:
    """Ask the user to confirm project creation.

    Args:
        project_name: The project name to display.
        template_name: The template name to display.

    Returns:
        True if confirmed, False otherwise.
    """
    confirmed = questionary.confirm(
        f"Create project '{project_name}' with '{template_name}' template?",
        default=True,
        style=CUSTOM_STYLE,
    ).ask()

    if confirmed is None:
        return False

    return confirmed
