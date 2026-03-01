"""Interactive prompts for gathering user input via questionary."""

from __future__ import annotations

import re

import questionary
from questionary import Style

from projinit.templates.registry import build_template, TemplateDef


PROMPT_STYLE = Style(
    [
        ("qmark", "fg:#feca57 bold"),
        ("question", "fg:#48dbfb bold"),
        ("answer", "fg:#0abde3 bold"),
        ("pointer", "fg:#ff6b6b bold"),
        ("highlighted", "fg:#ff6b6b bold"),
        ("selected", "fg:#0abde3"),
        ("separator", "fg:#a29bfe"),
        ("instruction", "fg:#888888"),
    ]
)

TEMPLATE_CHOICES = [
    questionary.Choice(
        title="minimal  -  Bare-bones src-layout package",
        value="minimal",
    ),
    questionary.Choice(
        title="standard -  Tests + Linting + Makefile",
        value="standard",
    ),
    questionary.Choice(
        title="full     -  CI/CD + Docker + Type checking + Everything",
        value="full",
    ),
]

PROJECT_NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]{0,63}$")


def _validate_project_name(name: str) -> bool | str:
    """Return True if valid, or an error message string."""
    if not name.strip():
        return "Project name cannot be empty."
    if not PROJECT_NAME_PATTERN.match(name.strip()):
        return (
            "Must start with a letter, contain only letters/digits/hyphens/underscores, "
            "and be at most 64 characters."
        )
    return True


def ask_template() -> str:
    """Prompt the user to select a project template.

    Returns:
        The selected template name ('minimal', 'standard', or 'full').
    """
    answer = questionary.select(
        "Select a project template:",
        choices=TEMPLATE_CHOICES,
        style=PROMPT_STYLE,
        instruction="(use arrow keys)",
    ).ask()

    if answer is None:
        raise KeyboardInterrupt
    return answer


def ask_project_name() -> str:
    """Prompt the user for a project name with validation.

    Returns:
        The validated, stripped project name.
    """
    answer = questionary.text(
        "Project name:",
        style=PROMPT_STYLE,
        validate=_validate_project_name,
        instruction="(letters, digits, hyphens, underscores)",
    ).ask()

    if answer is None:
        raise KeyboardInterrupt
    return answer.strip()


def ask_install_deps() -> bool:
    """Ask whether to install dependencies now.

    Returns:
        True if the user wants to install dependencies.
    """
    answer = questionary.confirm(
        "Install dependencies now?",
        default=True,
        style=PROMPT_STYLE,
    ).ask()

    if answer is None:
        raise KeyboardInterrupt
    return answer


def gather_inputs() -> tuple[str, TemplateDef, bool]:
    """Run the full interactive prompt sequence.

    Returns:
        A tuple of (project_name, template_def, should_install).
    """
    template_name = ask_template()
    project_name = ask_project_name()
    should_install = ask_install_deps()

    template_def = build_template(template_name, project_name)
    return project_name, template_def, should_install
