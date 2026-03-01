"""Main REPL application loop."""

import asyncio

from .agent import Agent
from .config import ANTHROPIC_API_KEY
from .ui.console import console, print_assistant, print_error, print_welcome
from .ui.input import create_prompt_session, get_prompt_text

SLASH_COMMANDS = {
    "/clear": "\u4f1a\u8a71\u5c65\u6b74\u3092\u30af\u30ea\u30a2",
    "/help": "\u30d8\u30eb\u30d7\u3092\u8868\u793a",
    "/exit": "\u7d42\u4e86",
}


async def run() -> None:
    """Main REPL entry point."""
    if not ANTHROPIC_API_KEY:
        print_error(
            "ANTHROPIC_API_KEY \u304c\u8a2d\u5b9a\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002\n"
            ".env \u30d5\u30a1\u30a4\u30eb\u307e\u305f\u306f\u74b0\u5883\u5909\u6570\u306b\u8a2d\u5b9a\u3057\u3066\u304f\u3060\u3055\u3044\u3002"
        )
        return

    print_welcome()
    session = create_prompt_session()
    agent = Agent()

    loop = asyncio.get_event_loop()

    while True:
        try:
            user_input = await loop.run_in_executor(
                None, lambda: session.prompt(get_prompt_text())
            )
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye![/dim]")
            break

        user_input = user_input.strip()
        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "/exit", "/quit"):
            console.print("[dim]Goodbye![/dim]")
            break
        if user_input == "/clear":
            agent.clear_history()
            console.print("[dim]\u4f1a\u8a71\u5c65\u6b74\u3092\u30af\u30ea\u30a2\u3057\u307e\u3057\u305f[/dim]")
            continue
        if user_input == "/help":
            _print_help()
            continue

        try:
            response = await agent.send(user_input)
            if response:
                print_assistant(response)
        except Exception as e:
            print_error(f"{type(e).__name__}: {e}")


def _print_help() -> None:
    console.print("\n[bold]Commands:[/bold]")
    for cmd, desc in SLASH_COMMANDS.items():
        console.print(f"  [cyan]{cmd}[/cyan] - {desc}")
    console.print()
    console.print("[bold]Capabilities:[/bold]")
    console.print("  - \u30d5\u30a1\u30a4\u30eb\u306e\u8aad\u307f\u66f8\u304d\u30fb\u691c\u7d22")
    console.print("  - \u30b7\u30a7\u30eb\u30b3\u30de\u30f3\u30c9\u306e\u5b9f\u884c")
    console.print("  - PowerPoint\u30d7\u30ec\u30bc\u30f3\u30c6\u30fc\u30b7\u30e7\u30f3\u306e\u751f\u6210")
    console.print("  - \u4e00\u822c\u7684\u306a\u8cea\u554f\u3078\u306e\u56de\u7b54")
    console.print()
