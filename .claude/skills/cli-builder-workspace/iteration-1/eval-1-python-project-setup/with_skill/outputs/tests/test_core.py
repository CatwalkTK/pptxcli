"""Tests for projinit.lib.core — business logic layer."""

import pytest
from pathlib import Path

from projinit.lib.core import (
    TEMPLATES,
    validate_project_name,
    get_template_packages,
    create_project_structure,
    write_config_files,
)


# ---------------------------------------------------------------------------
# validate_project_name
# ---------------------------------------------------------------------------

class TestValidateProjectName:
    """Project name validation tests."""

    @pytest.mark.parametrize(
        "name",
        [
            "my-project",
            "hello",
            "web-app-2024",
            "ab",
        ],
    )
    def test_valid_names(self, name: str) -> None:
        assert validate_project_name(name) is True

    @pytest.mark.parametrize(
        "name",
        [
            "",
            "a",
            "My-Project",
            "my_project",
            "my project",
            "-leading-hyphen",
            "trailing-hyphen-",
            "123numbers",
            "ALLCAPS",
        ],
    )
    def test_invalid_names(self, name: str) -> None:
        assert validate_project_name(name) is False


# ---------------------------------------------------------------------------
# get_template_packages
# ---------------------------------------------------------------------------

class TestGetTemplatePackages:
    """Template package retrieval tests."""

    def test_minimal_has_pytest(self) -> None:
        pkgs = get_template_packages("minimal")
        assert "pytest" in pkgs

    def test_standard_has_ruff(self) -> None:
        pkgs = get_template_packages("standard")
        assert "ruff" in pkgs

    def test_full_has_many_packages(self) -> None:
        pkgs = get_template_packages("full")
        assert len(pkgs) > 5

    def test_unknown_template_returns_empty(self) -> None:
        assert get_template_packages("nonexistent") == []


# ---------------------------------------------------------------------------
# create_project_structure
# ---------------------------------------------------------------------------

class TestCreateProjectStructure:
    """Tests for directory scaffolding."""

    def test_minimal_creates_src_and_tests(self, tmp_project_dir: Path) -> None:
        root = create_project_structure("my-app", "minimal")
        assert root.exists()
        assert (root / "src").is_dir()
        assert (root / "tests").is_dir()
        assert (root / "src" / "my_app" / "__init__.py").is_file()

    def test_full_creates_extra_dirs(self, tmp_project_dir: Path) -> None:
        root = create_project_structure("my-app", "full")
        assert (root / "docs").is_dir()
        assert (root / "scripts").is_dir()
        assert (root / "docker").is_dir()
        assert (root / ".github" / "workflows").is_dir()


# ---------------------------------------------------------------------------
# write_config_files
# ---------------------------------------------------------------------------

class TestWriteConfigFiles:
    """Tests for generated config files."""

    def test_pyproject_created(self, tmp_project_dir: Path) -> None:
        create_project_structure("demo", "minimal")
        write_config_files("demo", "minimal")
        pyproject = tmp_project_dir / "demo" / "pyproject.toml"
        assert pyproject.is_file()
        content = pyproject.read_text(encoding="utf-8")
        assert 'name = "demo"' in content

    def test_readme_created(self, tmp_project_dir: Path) -> None:
        create_project_structure("demo", "standard")
        write_config_files("demo", "standard")
        readme = tmp_project_dir / "demo" / "README.md"
        assert readme.is_file()
        assert "demo" in readme.read_text(encoding="utf-8")

    def test_gitignore_created(self, tmp_project_dir: Path) -> None:
        create_project_structure("demo", "minimal")
        write_config_files("demo", "minimal")
        gitignore = tmp_project_dir / "demo" / ".gitignore"
        assert gitignore.is_file()
        assert "__pycache__/" in gitignore.read_text(encoding="utf-8")

    def test_full_has_dockerfile(self, tmp_project_dir: Path) -> None:
        create_project_structure("demo", "full")
        write_config_files("demo", "full")
        dockerfile = tmp_project_dir / "demo" / "docker" / "Dockerfile"
        assert dockerfile.is_file()

    def test_full_has_ci_workflow(self, tmp_project_dir: Path) -> None:
        create_project_structure("demo", "full")
        write_config_files("demo", "full")
        ci = tmp_project_dir / "demo" / ".github" / "workflows" / "ci.yml"
        assert ci.is_file()


# ---------------------------------------------------------------------------
# TEMPLATES registry
# ---------------------------------------------------------------------------

class TestTemplates:
    """Sanity checks on the template registry."""

    def test_three_templates_exist(self) -> None:
        assert set(TEMPLATES.keys()) == {"minimal", "standard", "full"}

    def test_all_templates_have_names(self) -> None:
        for tpl in TEMPLATES.values():
            assert tpl.name
            assert tpl.display_name
            assert tpl.description
