"""ASCII banner display for projinit CLI."""

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align

from projinit import __version__


BANNER_ART = r"""
  ██████╗ ██████╗  ██████╗      ██╗██╗███╗   ██╗██╗████████╗
  ██╔══██╗██╔══██╗██╔═══██╗     ██║██║████╗  ██║██║╚══██╔══╝
  ██████╔╝██████╔╝██║   ██║     ██║██║██╔██╗ ██║██║   ██║
  ██╔═══╝ ██╔══██╗██║   ██║██   ██║██║██║╚██╗██║██║   ██║
  ██║     ██║  ██║╚██████╔╝╚█████╔╝██║██║ ╚████║██║   ██║
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝
"""

TAGLINE = ">> Project Scaffolding, Supercharged <<"


def display_banner(console: Console | None = None) -> None:
    """Display the startup banner with gradient colors and version info."""
    if console is None:
        console = Console()

    gradient_colors = [
        "#ff6b6b",
        "#ff8e53",
        "#feca57",
        "#48dbfb",
        "#0abde3",
        "#a29bfe",
    ]

    banner_lines = BANNER_ART.strip("\n").split("\n")

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = gradient_colors[i % len(gradient_colors)]
        styled_banner.append(line, style=f"bold {color}")
        if i < len(banner_lines) - 1:
            styled_banner.append("\n")

    styled_banner.append("\n\n")
    styled_banner.append(TAGLINE, style="bold italic #feca57")

    panel = Panel(
        Align.center(styled_banner),
        border_style="bright_cyan",
        padding=(1, 2),
        subtitle=f"[dim]v{__version__}[/dim]",
        subtitle_align="right",
    )

    console.print()
    console.print(panel)
    console.print()
