"""Tests for the CLI entry point."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from projinit.cli import main


class TestCLI:
    """Tests for the main CLI command."""

    def test_version_flag(self) -> None:
        """Test --version flag displays version."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_help_flag(self) -> None:
        """Test --help flag shows usage info."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "projinit" in result.output.lower()
        assert "--name" in result.output
        assert "--template" in result.output

    @patch("projinit.cli.create_project")
    @patch("projinit.cli.print_summary")
    @patch("projinit.cli.display_banner")
    def test_non_interactive_mode(
        self,
        mock_banner: MagicMock,
        mock_summary: MagicMock,
        mock_create: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test non-interactive mode with --name and --template flags."""
        mock_create.return_value = tmp_path / "myapp"
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["--name", "myapp", "--template", "minimal", "--no-confirm", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0
        mock_banner.assert_called_once()
        mock_create.assert_called_once()

    @patch("projinit.cli.create_project")
    @patch("projinit.cli.print_summary")
    @patch("projinit.cli.display_banner")
    def test_file_exists_error_exits_with_1(
        self,
        mock_banner: MagicMock,
        mock_summary: MagicMock,
        mock_create: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test that FileExistsError causes exit code 1."""
        mock_create.side_effect = FileExistsError("Directory already exists")
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["--name", "myapp", "--template", "minimal", "--no-confirm", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 1
        assert "Error" in result.output

    @patch("projinit.cli.create_project")
    @patch("projinit.cli.print_summary")
    @patch("projinit.cli.display_banner")
    def test_validation_error_exits_with_1(
        self,
        mock_banner: MagicMock,
        mock_summary: MagicMock,
        mock_create: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test that ValueError causes exit code 1."""
        mock_create.side_effect = ValueError("Invalid name")
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["--name", "myapp", "--template", "minimal", "--no-confirm", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 1
        assert "Validation Error" in result.output

    @patch("projinit.cli.prompt_confirm_creation")
    @patch("projinit.cli.prompt_template_selection")
    @patch("projinit.cli.prompt_project_name")
    @patch("projinit.cli.create_project")
    @patch("projinit.cli.print_summary")
    @patch("projinit.cli.display_banner")
    def test_user_cancels_confirmation(
        self,
        mock_banner: MagicMock,
        mock_summary: MagicMock,
        mock_create: MagicMock,
        mock_name: MagicMock,
        mock_template: MagicMock,
        mock_confirm: MagicMock,
    ) -> None:
        """Test that declining confirmation aborts gracefully."""
        mock_name.return_value = "myapp"
        mock_template.return_value = "minimal"
        mock_confirm.return_value = False
        runner = CliRunner()
        result = runner.invoke(main, [])
        assert result.exit_code == 0
        assert "Aborted" in result.output
        mock_create.assert_not_called()

    @patch("projinit.cli.prompt_template_selection")
    @patch("projinit.cli.prompt_project_name")
    @patch("projinit.cli.display_banner")
    def test_keyboard_interrupt_handled(
        self,
        mock_banner: MagicMock,
        mock_name: MagicMock,
        mock_template: MagicMock,
    ) -> None:
        """Test that KeyboardInterrupt is handled gracefully."""
        mock_name.side_effect = KeyboardInterrupt()
        runner = CliRunner()
        result = runner.invoke(main, [])
        assert result.exit_code == 130
        assert "Cancelled" in result.output

    def test_invalid_template_choice(self) -> None:
        """Test that invalid template choice is rejected by click."""
        runner = CliRunner()
        result = runner.invoke(main, ["--template", "nonexistent"])
        assert result.exit_code != 0
