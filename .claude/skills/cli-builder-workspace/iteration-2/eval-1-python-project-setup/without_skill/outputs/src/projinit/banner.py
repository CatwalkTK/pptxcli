"""ASCII banner display for projinit."""

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align

BANNER_ART = r"""
[bold cyan]  ██████╗ ██████╗  ██████╗      ██╗██╗███╗   ██╗██╗████████╗[/]
[bold cyan]  ██╔══██╗██╔══██╗██╔═══██╗     ██║██║████╗  ██║██║╚══██╔══╝[/]
[bold blue]  ██████╔╝██████╔╝██║   ██║     ██║██║██╔██╗ ██║██║   ██║[/]
[bold blue]  ██╔═══╝ ██╔══██╗██║   ██║██   ██║██║██║╚██╗██║██║   ██║[/]
[bold magenta]  ██║     ██║  ██║╚██████╔╝╚█████╔╝██║██║ ╚████║██║   ██║[/]
[bold magenta]  ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝[/]
"""

TAGLINE = "[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]"
SUBTITLE = "[bold white]  Project Scaffolding CLI[/bold white]  [dim]v1.0.0[/dim]"
DECORATIVE = "[dim]  Kickstart your next project in seconds.[/dim]"


def display_banner(console: Console | None = None) -> None:
    """Display the startup banner with styling."""
    if console is None:
        console = Console()

    console.print()
    console.print(BANNER_ART)
    console.print(TAGLINE)
    console.print(SUBTITLE)
    console.print(DECORATIVE)
    console.print(TAGLINE)
    console.print()
