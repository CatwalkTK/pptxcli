"""Tests for the CLI entry point."""

from unittest.mock import patch, MagicMock
from pathlib import Path

from click.testing import CliRunner

from projinit.cli import main
from projinit.templates.registry import build_template


class TestCLI:
    """Integration-level tests for the CLI command."""

    def test_aborted_on_keyboard_interrupt(self):
        runner = CliRunner()
        with patch("projinit.cli.gather_inputs", side_effect=KeyboardInterrupt):
            result = runner.invoke(main, ["--no-banner"])
        assert result.exit_code != 0

    def test_error_when_directory_exists(self, tmp_path: Path):
        existing = tmp_path / "my-proj"
        existing.mkdir()

        template = build_template("minimal", "my-proj")

        with patch("projinit.cli.gather_inputs", return_value=("my-proj", template, False)):
            runner = CliRunner()
            result = runner.invoke(main, ["--no-banner", "-o", str(tmp_path)])

        assert result.exit_code != 0
        assert "already exists" in result.output

    def test_successful_scaffold_no_install(self, tmp_path: Path):
        template = build_template("minimal", "new-proj")

        with patch("projinit.cli.gather_inputs", return_value=("new-proj", template, False)):
            runner = CliRunner()
            result = runner.invoke(main, ["--no-banner", "-o", str(tmp_path)])

        assert result.exit_code == 0
        assert (tmp_path / "new-proj").exists()
        assert (tmp_path / "new-proj" / "README.md").exists()

    def test_successful_scaffold_with_install(self, tmp_path: Path):
        template = build_template("standard", "new-proj")

        with (
            patch("projinit.cli.gather_inputs", return_value=("new-proj", template, True)),
            patch("projinit.cli.install_dependencies", return_value=True) as mock_install,
        ):
            runner = CliRunner()
            result = runner.invoke(main, ["--no-banner", "-o", str(tmp_path)])

        assert result.exit_code == 0
        mock_install.assert_called_once()
