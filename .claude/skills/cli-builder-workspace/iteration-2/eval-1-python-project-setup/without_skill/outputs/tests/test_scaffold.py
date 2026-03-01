"""Tests for the scaffold module."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pytest
from rich.console import Console

from projinit.scaffold import (
    create_project,
    print_summary,
    validate_project_name,
)
from projinit.templates import FULL_TEMPLATE, MINIMAL_TEMPLATE, STANDARD_TEMPLATE


class TestValidateProjectName:
    """Tests for the validate_project_name function."""

    def test_valid_name(self) -> None:
        """Test that a valid name returns None."""
        assert validate_project_name("my-project") is None

    def test_valid_name_with_underscore(self) -> None:
        """Test that underscores are allowed."""
        assert validate_project_name("my_project") is None

    def test_valid_name_with_numbers(self) -> None:
        """Test that numbers after first char are allowed."""
        assert validate_project_name("project123") is None

    def test_empty_name(self) -> None:
        """Test that empty name returns error."""
        error = validate_project_name("")
        assert error is not None
        assert "empty" in error.lower()

    def test_starts_with_number(self) -> None:
        """Test that name starting with number is rejected."""
        error = validate_project_name("123project")
        assert error is not None

    def test_starts_with_hyphen(self) -> None:
        """Test that name starting with hyphen is rejected."""
        error = validate_project_name("-project")
        assert error is not None

    def test_special_characters(self) -> None:
        """Test that special characters are rejected."""
        error = validate_project_name("my@project")
        assert error is not None

    def test_spaces_rejected(self) -> None:
        """Test that spaces are rejected."""
        error = validate_project_name("my project")
        assert error is not None

    def test_too_long_name(self) -> None:
        """Test that names over 64 chars are rejected."""
        error = validate_project_name("a" * 65)
        assert error is not None
        assert "64" in error

    def test_exactly_64_chars_valid(self) -> None:
        """Test that exactly 64 chars is acceptable."""
        assert validate_project_name("a" * 64) is None


class TestCreateProject:
    """Tests for the create_project function."""

    def test_creates_project_directory(self, tmp_path: Path) -> None:
        """Test that project directory is created."""
        console = Console(file=StringIO(), force_terminal=True)
        project_path = create_project("testproj", MINIMAL_TEMPLATE, tmp_path, console)
        assert project_path.exists()
        assert project_path.is_dir()

    def test_creates_subdirectories(self, tmp_path: Path) -> None:
        """Test that template directories are created."""
        console = Console(file=StringIO(), force_terminal=True)
        create_project("testproj", MINIMAL_TEMPLATE, tmp_path, console)
        assert (tmp_path / "testproj" / "src").is_dir()

    def test_creates_files(self, tmp_path: Path) -> None:
        """Test that template files are created."""
        console = Console(file=StringIO(), force_terminal=True)
        create_project("testproj", MINIMAL_TEMPLATE, tmp_path, console)
        assert (tmp_path / "testproj" / "pyproject.toml").is_file()
        assert (tmp_path / "testproj" / "README.md").is_file()
        assert (tmp_path / "testproj" / ".gitignore").is_file()

    def test_template_placeholders_replaced(self, tmp_path: Path) -> None:
        """Test that {{project_name}} is replaced in file contents."""
        console = Console(file=StringIO(), force_terminal=True)
        create_project("myapp", MINIMAL_TEMPLATE, tmp_path, console)
        readme = (tmp_path / "myapp" / "README.md").read_text(encoding="utf-8")
        assert "myapp" in readme
        assert "{{project_name}}" not in readme

    def test_pyproject_contains_project_name(self, tmp_path: Path) -> None:
        """Test that pyproject.toml contains the project name."""
        console = Console(file=StringIO(), force_terminal=True)
        create_project("coolproj", MINIMAL_TEMPLATE, tmp_path, console)
        content = (tmp_path / "coolproj" / "pyproject.toml").read_text(encoding="utf-8")
        assert 'name = "coolproj"' in content

    def test_raises_if_directory_exists(self, tmp_path: Path) -> None:
        """Test that FileExistsError is raised for existing directories."""
        (tmp_path / "existing").mkdir()
        console = Console(file=StringIO(), force_terminal=True)
        with pytest.raises(FileExistsError):
            create_project("existing", MINIMAL_TEMPLATE, tmp_path, console)

    def test_raises_for_invalid_name(self, tmp_path: Path) -> None:
        """Test that ValueError is raised for invalid project names."""
        console = Console(file=StringIO(), force_terminal=True)
        with pytest.raises(ValueError):
            create_project("", MINIMAL_TEMPLATE, tmp_path, console)

    def test_standard_template_creates_tests_dir(self, tmp_path: Path) -> None:
        """Test that standard template creates tests directory."""
        console = Console(file=StringIO(), force_terminal=True)
        create_project("stdproj", STANDARD_TEMPLATE, tmp_path, console)
        assert (tmp_path / "stdproj" / "tests").is_dir()
        assert (tmp_path / "stdproj" / "tests" / "test_main.py").is_file()

    def test_full_template_creates_all_dirs(self, tmp_path: Path) -> None:
        """Test that full template creates all expected directories."""
        console = Console(file=StringIO(), force_terminal=True)
        create_project("fullproj", FULL_TEMPLATE, tmp_path, console)
        assert (tmp_path / "fullproj" / "tests" / "unit").is_dir()
        assert (tmp_path / "fullproj" / "tests" / "integration").is_dir()
        assert (tmp_path / "fullproj" / ".github" / "workflows").is_dir()
        assert (tmp_path / "fullproj" / "scripts").is_dir()

    def test_full_template_creates_docker_files(self, tmp_path: Path) -> None:
        """Test that full template creates Docker-related files."""
        console = Console(file=StringIO(), force_terminal=True)
        create_project("fullproj", FULL_TEMPLATE, tmp_path, console)
        assert (tmp_path / "fullproj" / "Dockerfile").is_file()
        assert (tmp_path / "fullproj" / ".dockerignore").is_file()

    def test_full_template_creates_makefile(self, tmp_path: Path) -> None:
        """Test that full template creates a Makefile."""
        console = Console(file=StringIO(), force_terminal=True)
        create_project("fullproj", FULL_TEMPLATE, tmp_path, console)
        assert (tmp_path / "fullproj" / "Makefile").is_file()

    def test_returns_project_path(self, tmp_path: Path) -> None:
        """Test that the function returns the correct project path."""
        console = Console(file=StringIO(), force_terminal=True)
        result = create_project("testproj", MINIMAL_TEMPLATE, tmp_path, console)
        assert result == tmp_path / "testproj"

    def test_defaults_to_cwd_when_no_target(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that target_dir defaults to cwd."""
        monkeypatch.chdir(tmp_path)
        console = Console(file=StringIO(), force_terminal=True)
        result = create_project("testproj", MINIMAL_TEMPLATE, console=console)
        assert result == tmp_path / "testproj"


class TestPrintSummary:
    """Tests for the print_summary function."""

    def test_summary_contains_project_name(self, tmp_path: Path) -> None:
        """Test that summary mentions the project name."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, no_color=True)
        print_summary("myapp", MINIMAL_TEMPLATE, tmp_path / "myapp", console)
        result = output.getvalue()
        assert "myapp" in result

    def test_summary_contains_template_name(self, tmp_path: Path) -> None:
        """Test that summary mentions the template."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, no_color=True)
        print_summary("myapp", STANDARD_TEMPLATE, tmp_path / "myapp", console)
        result = output.getvalue()
        assert "Standard" in result

    def test_summary_contains_next_steps(self, tmp_path: Path) -> None:
        """Test that summary includes next steps guidance."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, no_color=True)
        print_summary("myapp", MINIMAL_TEMPLATE, tmp_path / "myapp", console)
        result = output.getvalue()
        assert "cd myapp" in result

    def test_full_template_summary_mentions_make(self, tmp_path: Path) -> None:
        """Test that full template summary mentions make install."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, no_color=True)
        print_summary("myapp", FULL_TEMPLATE, tmp_path / "myapp", console)
        result = output.getvalue()
        assert "make install" in result

    def test_summary_shows_success_message(self, tmp_path: Path) -> None:
        """Test that summary shows success message."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, no_color=True)
        print_summary("myapp", MINIMAL_TEMPLATE, tmp_path / "myapp", console)
        result = output.getvalue()
        assert "successfully" in result.lower()
