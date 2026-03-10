"""Rich console rendering helpers."""

import os
from contextlib import contextmanager

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.style import Style

console = Console()


def print_welcome() -> None:
    """PPTX-VIBE style startup screen."""
    from cli import __version__

    cwd = os.getcwd()
    model = os.environ.get("CLI_MODEL", "claude-sonnet-4-20250514")

    # Block-style ASCII art
    ascii_art = [
        " ██▀▀█  ██▀▀█  ▀▀██▀▀  █▄  ▄█",
        " ██▄▄▀  ██▄▄▀    ██      ▀██▀ ",
        " ██     ██       ██      ▄██▄ ",
        " ▀▀     ▀▀       ▀▀    █▀  ▀█",
        "",
        " █▌  ▐█  ██  ██▀▀▄  ██▀▀▀",
        "  █▌▐█   ██  ██▀▀█  ██▀▀ ",
        "   ▀▀    ██  ██▄▄▀  ██▄▄▄",
        "",
        " ═══ Presentation AI Studio ═══",
    ]

    title = "\n".join(
        f"[bold cyan]{line}[/bold cyan]" for line in ascii_art
    )
    version_line = f"[dim]v{__version__} // Model: {model}[/dim]"

    # Info blocks
    info_lines = [
        "[red]●[/red] [bold]strong[/bold]  claude-opus-4",
        "[blue]●[/blue] [bold]balanced[/bold]  claude-sonnet-4",
        "[green]●[/green] [bold]fast[/bold]  claude-haiku-4",
        "",
        f"[cyan]▸[/cyan] [white]CwD[/white] [dim]{cwd}[/dim]",
    ]

    # Help footer
    help_lines = [
        "[dim]/help コマンド一覧[/dim]",
        "[dim]ESC/Ctrl+C 中断[/dim]",
    ]

    content = (
        f"\n{title}\n"
        f"{version_line}\n\n"
        + "\n".join(info_lines)
        + "\n\n"
        + "  ".join(help_lines)
    )

    console.print(
        Panel(
            content,
            border_style="cyan",
            padding=(1, 2),
        )
    )


def print_assistant(text: str) -> None:
    """Render assistant response as markdown."""
    console.print()
    console.print(Markdown(text))
    console.print()


def print_tool_call(tool_name: str, tool_input: dict) -> None:
    """Display a tool invocation."""
    input_summary = ", ".join(
        f"{k}={_truncate(str(v), 80)}" for k, v in tool_input.items()
    )
    console.print(
        f"  [bold yellow]\u2192 {tool_name}[/bold yellow]"
        f" [dim]({input_summary})[/dim]"
    )


def print_tool_result(tool_name: str, result: str) -> None:
    """Display tool result in a compact panel."""
    display = _truncate(result, 500)
    console.print(
        Panel(
            display,
            title=f"[green]{tool_name}[/green]",
            border_style="green",
            padding=(0, 1),
        )
    )


def print_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")


@contextmanager
def ai_spinner(message: str = "Thinking"):
    """Show a spinning / animation while AI is processing."""
    spinner = Spinner(
        "line",
        text=f"[bold cyan]{message}[/bold cyan]",
        style=Style(color="cyan"),
    )
    with console.status(spinner, spinner_style="cyan"):
        yield


def _truncate(s: str, max_len: int) -> str:
    return s if len(s) <= max_len else s[:max_len] + "..."
