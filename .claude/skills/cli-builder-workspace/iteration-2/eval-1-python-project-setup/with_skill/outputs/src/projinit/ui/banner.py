"""ASCII art banner for projinit CLI."""

from pyfiglet import figlet_format
from rich.console import Console

from projinit.ui.theme import CLI_THEME

console = Console(theme=CLI_THEME)


def show_banner() -> None:
    """Display the main projinit banner with status line."""
    banner = figlet_format("PROJINIT", font="slant")
    console.print(f"[cyan]{banner}[/cyan]", end="")
    console.print("  [dim]v1.0.0 -- Interactive Project Scaffolding[/dim]")
    console.print("  [dim]-----------------------------------------------[/dim]\n")


def show_status_line() -> None:
    """Display PPTX VIBE-style status line after banner."""
    items = {
        "Templates": "[primary]minimal[/primary] | [primary]standard[/primary] | [primary]full[/primary]",
        "Available": "init | --help | --version",
    }
    for key, value in items.items():
        console.print(f"  [dim]{key}:[/dim]  {value}")
    console.print()


def show_compact_banner() -> None:
    """Compact one-line banner for subcommands."""
    console.print("[bold cyan]projinit[/bold cyan] [dim]v1.0.0[/dim]\n")
