"""Tests for the banner module."""

from io import StringIO

from rich.console import Console

from projinit.banner import display_banner


def test_display_banner_contains_projinit():
    """The banner output should include the tool name."""
    buf = StringIO()
    console = Console(file=buf, force_terminal=True, width=120)
    display_banner(console)
    output = buf.getvalue()
    assert "PROJINIT" in output.upper() or "projinit" in output.lower()


def test_display_banner_contains_version():
    """The banner output should include the version string."""
    buf = StringIO()
    console = Console(file=buf, force_terminal=True, width=120)
    display_banner(console)
    output = buf.getvalue()
    assert "1.0.0" in output
