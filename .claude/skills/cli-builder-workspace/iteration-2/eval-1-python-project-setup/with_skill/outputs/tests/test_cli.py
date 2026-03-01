"""Tests for the projinit CLI entry-points."""

from __future__ import annotations

from typer.testing import CliRunner

from projinit.cli import app

runner = CliRunner()


def test_version_flag() -> None:
    """``--version`` should print the version string and exit cleanly."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "projinit v" in result.stdout
    assert "1.0.0" in result.stdout


def test_help_flag() -> None:
    """``--help`` should include the tool description."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "projinit" in result.stdout


def test_init_help() -> None:
    """``init --help`` should describe template options."""
    result = runner.invoke(app, ["init", "--help"])
    assert result.exit_code == 0
    assert "template" in result.stdout.lower()


def test_init_noninteractive(tmp_path) -> None:
    """``init`` with all args + ``--yes`` should scaffold without prompts."""
    result = runner.invoke(
        app,
        [
            "init",
            "test-project",
            "--template", "minimal",
            "--yes",
        ],
        catch_exceptions=False,
    )
    # The command should succeed (exit 0).
    assert result.exit_code == 0
    assert "test-project" in result.stdout
