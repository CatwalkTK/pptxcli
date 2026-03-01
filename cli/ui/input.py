"""Interactive input using prompt_toolkit."""

import os

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style


def create_prompt_session() -> PromptSession:
    """Create a prompt session with history."""
    history_dir = os.path.expanduser("~/.cli_agent")
    os.makedirs(history_dir, exist_ok=True)
    history_file = os.path.join(history_dir, "history.txt")

    style = Style.from_dict({
        "prompt": "bold cyan",
    })

    session: PromptSession = PromptSession(
        history=FileHistory(history_file),
        style=style,
        multiline=False,
    )
    return session


def get_prompt_text() -> FormattedText:
    return FormattedText([("class:prompt", "You> ")])
