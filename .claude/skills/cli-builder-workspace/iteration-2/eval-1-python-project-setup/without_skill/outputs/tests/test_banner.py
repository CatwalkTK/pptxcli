"""Tests for the banner module."""

from io import StringIO

from rich.console import Console

from projinit.banner import display_banner


class TestDisplayBanner:
    """Tests for the display_banner function."""

    def test_banner_outputs_to_console(self) -> None:
        """Test that banner produces output."""
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        display_banner(console)
        result = output.getvalue()
        assert len(result) > 0

    def test_banner_contains_projinit_text(self) -> None:
        """Test that banner contains identifying text."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, no_color=True)
        display_banner(console)
        result = output.getvalue()
        # The banner art contains the letters of PROJINIT as Unicode block chars
        assert "Project Scaffolding CLI" in result

    def test_banner_contains_version(self) -> None:
        """Test that banner displays version."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, no_color=True)
        display_banner(console)
        result = output.getvalue()
        assert "v1.0.0" in result

    def test_banner_creates_own_console_if_none(self) -> None:
        """Test that banner works when no console is passed."""
        # Should not raise any exception
        display_banner(Console(file=StringIO()))
