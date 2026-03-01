"""Tests for the project scaffolding business logic."""

from __future__ import annotations

from pathlib import Path

import pytest

from projinit.lib.scaffold import scaffold_project, _to_python_name
from projinit.lib.templates import TEMPLATES


# ---------------------------------------------------------------------------
# _to_python_name
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("input_name", "expected"),
    [
        ("my-project", "my_project"),
        ("MyProject", "myproject"),
        ("hello world", "hello_world"),
        ("foo--bar", "foo_bar"),
        ("123abc", "123abc"),
        ("---", ""),  # edge case: sanitizes to empty -> fallback
    ],
)
def test_to_python_name(input_name: str, expected: str) -> None:
    result = _to_python_name(input_name)
    if expected == "":
        # Falls back to "project" when sanitized to empty
        assert result == "project"
    else:
        assert result == expected


# ---------------------------------------------------------------------------
# scaffold_project
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("template_key", list(TEMPLATES.keys()))
def test_scaffold_creates_directory(
    tmp_path: Path,
    template_key: str,
) -> None:
    """Each template should create the project root directory."""
    project_root = scaffold_project(
        name="test-proj",
        template_key=template_key,
        base_dir=tmp_path,
    )
    assert project_root.exists()
    assert project_root.is_dir()
    assert project_root.name == "test-proj"


@pytest.mark.parametrize("template_key", list(TEMPLATES.keys()))
def test_scaffold_creates_pyproject_toml(
    tmp_path: Path,
    template_key: str,
) -> None:
    """Every template should produce a ``pyproject.toml``."""
    project_root = scaffold_project(
        name="demo",
        template_key=template_key,
        base_dir=tmp_path,
    )
    pyproject = project_root / "pyproject.toml"
    assert pyproject.exists()
    content = pyproject.read_text(encoding="utf-8")
    assert 'name = "demo"' in content


def test_scaffold_minimal_structure(tmp_path: Path) -> None:
    root = scaffold_project(name="mini", template_key="minimal", base_dir=tmp_path)
    assert (root / "src" / "mini" / "__init__.py").exists()
    assert (root / "src" / "mini" / "main.py").exists()
    assert (root / ".gitignore").exists()
    assert (root / "README.md").exists()


def test_scaffold_standard_has_tests(tmp_path: Path) -> None:
    root = scaffold_project(name="std-proj", template_key="standard", base_dir=tmp_path)
    assert (root / "tests" / "test_main.py").exists()


def test_scaffold_full_has_ci_and_docker(tmp_path: Path) -> None:
    root = scaffold_project(name="full-proj", template_key="full", base_dir=tmp_path)
    assert (root / ".github" / "workflows" / "ci.yml").exists()
    assert (root / "Dockerfile").exists()
    assert (root / ".pre-commit-config.yaml").exists()
    assert (root / "docs" / "index.md").exists()
