"""Tests for the scaffold module."""

from io import StringIO
from pathlib import Path

from rich.console import Console

from projinit.templates.registry import build_template
from projinit.scaffold import generate_files


def _make_console() -> Console:
    return Console(file=StringIO(), force_terminal=True, width=120)


class TestGenerateFiles:
    """Tests for generate_files."""

    def test_creates_project_dir(self, tmp_path: Path):
        template = build_template("minimal", "test-proj")
        console = _make_console()
        result = generate_files("test-proj", template, base_dir=tmp_path, console=console)
        assert result.exists()
        assert result.is_dir()
        assert result.name == "test-proj"

    def test_creates_all_files(self, tmp_path: Path):
        template = build_template("minimal", "test-proj")
        console = _make_console()
        project_dir = generate_files("test-proj", template, base_dir=tmp_path, console=console)

        for tfile in template.files:
            assert (project_dir / tfile.path).exists(), f"Missing: {tfile.path}"

    def test_file_contents_match(self, tmp_path: Path):
        template = build_template("minimal", "test-proj")
        console = _make_console()
        project_dir = generate_files("test-proj", template, base_dir=tmp_path, console=console)

        for tfile in template.files:
            actual = (project_dir / tfile.path).read_text(encoding="utf-8")
            assert actual == tfile.content, f"Content mismatch: {tfile.path}"

    def test_standard_creates_nested_dirs(self, tmp_path: Path):
        template = build_template("standard", "my-app")
        console = _make_console()
        project_dir = generate_files("my-app", template, base_dir=tmp_path, console=console)
        assert (project_dir / "src" / "my_app").is_dir()
        assert (project_dir / "tests").is_dir()

    def test_full_creates_github_workflows(self, tmp_path: Path):
        template = build_template("full", "my-app")
        console = _make_console()
        project_dir = generate_files("my-app", template, base_dir=tmp_path, console=console)
        assert (project_dir / ".github" / "workflows" / "ci.yml").exists()
