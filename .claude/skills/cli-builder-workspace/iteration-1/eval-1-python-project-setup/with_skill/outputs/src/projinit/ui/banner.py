"""ASCII art banner and status line display."""

from pyfiglet import figlet_format
from rich.console import Console

from projinit import __version__
from projinit.ui.theme import CLI_THEME

console = Console(theme=CLI_THEME)

BANNER_FONT = "slant"

TAGLINE = "Scaffold projects in seconds"


def show_banner() -> None:
    """Display the full CLI banner with gradient-style decoration."""
    banner_text = figlet_format("PROJINIT", font=BANNER_FONT)

    console.print()
    console.print(f"[cyan]{banner_text}[/cyan]", end="")
    console.print("  [dim bright_magenta]\u2591\u2592\u2593\u2588[/dim bright_magenta] [bold cyan]Project Initializer[/bold cyan] [dim bright_magenta]\u2588\u2593\u2592\u2591[/dim bright_magenta]")
    console.print(f"  [dim]v{__version__} \u2014 {TAGLINE}[/dim]")
    console.print()


def show_compact_banner() -> None:
    """One-line banner for subcommands."""
    console.print(
        f"[bold cyan]projinit[/bold cyan] [dim]v{__version__}[/dim]\n"
    )


def show_status_line(items: dict[str, str]) -> None:
    """PPTX VIBE-style status line showing current context."""
    max_key_len = max(len(k) for k in items) if items else 0
    for key, value in items.items():
        console.print(f"  [dim]{key + ':':<{max_key_len + 1}}[/dim] {value}")
    console.print()
