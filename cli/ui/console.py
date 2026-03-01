"""Rich console rendering helpers."""

import os

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def print_welcome() -> None:
    """PPTX-VIBE style startup screen."""
    from cli import __version__

    import pyfiglet

    cwd = os.getcwd()
    model = os.environ.get("CLI_MODEL", "claude-sonnet-4-20250514")

    # Block font: VISUAL STUDIO style - two words, clear vertical separation
    try:
        pptx_art = pyfiglet.figlet_format("PPTX", font="block")
        vibe_art = pyfiglet.figlet_format("VIBE", font="block")
    except Exception:
        pptx_art = pyfiglet.figlet_format("PPTX", font="standard")
        vibe_art = pyfiglet.figlet_format("VIBE", font="standard")
    # Strip to content, normalize line lengths
    pptx_lines = [l.rstrip() for l in pptx_art.rstrip().split("\n") if l.strip()]
    vibe_lines = [l.rstrip() for l in vibe_art.rstrip().split("\n") if l.strip()]
    pptx_w = max(len(l) for l in pptx_lines) if pptx_lines else 0
    vibe_w = max(len(l) for l in vibe_lines) if vibe_lines else 0
    # Pad to consistent width, center VIBE under PPTX
    pptx_padded = [l.ljust(pptx_w) for l in pptx_lines]
    indent = max(0, (pptx_w - vibe_w) // 2)
    vibe_padded = [" " * indent + l.ljust(vibe_w) for l in vibe_lines]
    # Significant vertical space between words (VISUAL STUDIO style)
    ascii_lines = pptx_padded + [""] + [""] + vibe_padded
    title = "\n".join(
        f"[bold magenta]{line}[/bold magenta]" for line in ascii_lines
    )
    subtitle = "[white] * MULTI-PROVIDER AI AGENT *[/white]"
    version_line = f"[dim]v{__version__} // Anthropic * Model: {model}[/dim]"

    # Info blocks (ASCII-safe for Windows cp932)
    info_lines = [
        "[red]*[/red] [bold]strong[/bold]  claude-opus-4",
        "[blue]*[/blue] [bold]balanced[/bold]  claude-sonnet-4",
        "[green]*[/green] [bold]fast[/bold]  claude-haiku-4",
        "",
        "[yellow][M][/yellow] [green]Mode +[/green] [white]INTERACTIVE[/white]",
        "[yellow][S][/yellow] [white]Strategy[/white] [dim]auto[/dim]",
        "",
        f"[cyan][>][/cyan] [white]CwD[/white] [dim]{cwd}[/dim]",
    ]

    # Help footer
    help_lines = [
        "[dim]/help \u30b3\u30de\u30f3\u30c9\u4e00\u89a7[/dim]",
        "[dim]ESC/Ctrl+C \u4e2d\u65ad (2\u56de\u3067\u7d42\u4e86)[/dim]",
        '[dim]*""\u3067\u8907\u6570\u884c[/dim]',
        "[dim]IME\u5bfe\u5fdc: \u7a7a\u884c Enter\u3067\u9001\u4fe1[/dim]",
    ]

    content = (
        f"\n{title}\n"
        f"{subtitle}\n"
        f"{version_line}\n\n"
        + "\n".join(info_lines)
        + "\n\n"
        + "  ".join(help_lines)
    )

    console.print(
        Panel(
            content,
            border_style="magenta",
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


def _truncate(s: str, max_len: int) -> str:
    return s if len(s) <= max_len else s[:max_len] + "..."
