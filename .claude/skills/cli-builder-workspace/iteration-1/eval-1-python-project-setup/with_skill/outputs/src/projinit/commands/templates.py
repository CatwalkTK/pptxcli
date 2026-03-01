"""templates command — list available project templates."""

from rich.console import Console
from rich.table import Table
from rich import box

from projinit.ui.banner import show_compact_banner
from projinit.ui.theme import CLI_THEME
from projinit.lib.core import TEMPLATES

console = Console(theme=CLI_THEME)


def run_templates() -> None:
    """Display a table of all available project templates."""
    show_compact_banner()

    table = Table(
        title="Available Templates",
        box=box.ROUNDED,
        header_style="bold cyan",
        title_style="bold",
    )
    table.add_column("Name", style="cyan", min_width=12)
    table.add_column("Description", min_width=30)
    table.add_column("Packages", justify="center", min_width=10)
    table.add_column("Status", justify="center", min_width=10)

    for tpl in TEMPLATES.values():
        pkg_count = str(len(tpl.packages))
        status = "[green]stable[/green]" if tpl.stable else "[yellow]beta[/yellow]"
        table.add_row(tpl.display_name, tpl.description, pkg_count, status)

    console.print(table)
    console.print()
    console.print(
        "[dim]Use [bold]projinit init --template <name>[/bold] to scaffold a project.[/dim]"
    )
