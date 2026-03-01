"""Tests for the CLI entry points using Typer's CliRunner."""

from typer.testing import CliRunner

from projinit import __version__
from projinit.cli import app

runner = CliRunner()


class TestGlobalOptions:
    """Tests for --version and --help flags."""

    def test_version_flag(self) -> None:
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert __version__ in result.stdout

    def test_help_flag(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "projinit" in result.stdout.lower()


class TestTemplatesCommand:
    """Tests for the 'templates' subcommand."""

    def test_templates_lists_all(self) -> None:
        result = runner.invoke(app, ["templates"])
        assert result.exit_code == 0
        assert "Minimal" in result.stdout
        assert "Standard" in result.stdout
        assert "Full" in result.stdout

    def test_templates_shows_table(self) -> None:
        result = runner.invoke(app, ["templates"])
        assert result.exit_code == 0
        # Table header should be present
        assert "Name" in result.stdout or "Available" in result.stdout


class TestInitCommand:
    """Tests for the 'init' subcommand in non-interactive mode."""

    def test_init_unknown_template_exits(self) -> None:
        result = runner.invoke(app, ["init", "--template", "nonexistent", "--name", "demo", "--yes"])
        assert result.exit_code == 1

    def test_init_invalid_name_exits(self) -> None:
        result = runner.invoke(app, ["init", "--template", "minimal", "--name", "INVALID", "--yes"])
        assert result.exit_code == 1
