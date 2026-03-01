"""Rich theme definitions for consistent CLI styling."""

from rich.theme import Theme
from rich.style import Style

CLI_THEME = Theme(
    {
        "primary": Style(color="cyan"),
        "secondary": Style(color="magenta"),
        "success": Style(color="green", bold=True),
        "warning": Style(color="yellow"),
        "error": Style(color="red", bold=True),
        "info": Style(color="blue"),
        "dim": Style(dim=True),
        "heading": Style(color="cyan", bold=True, underline=True),
        "accent": Style(color="bright_magenta"),
        "code": Style(color="bright_black", bgcolor="grey11"),
    }
)

PROMPT_STYLE = [
    ("qmark", "fg:cyan bold"),
    ("question", "bold"),
    ("answer", "fg:cyan"),
    ("pointer", "fg:cyan bold"),
    ("highlighted", "fg:cyan bold"),
    ("selected", "fg:cyan"),
]
