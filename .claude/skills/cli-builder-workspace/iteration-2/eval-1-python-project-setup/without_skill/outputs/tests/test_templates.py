"""Tests for the templates module."""

import pytest

from projinit.templates import (
    FULL_TEMPLATE,
    MINIMAL_TEMPLATE,
    STANDARD_TEMPLATE,
    TEMPLATES,
    get_template,
    get_template_choices,
)


class TestTemplateDefinitions:
    """Tests for template data integrity."""

    def test_three_templates_available(self) -> None:
        """Test that exactly three templates are defined."""
        assert len(TEMPLATES) == 3

    def test_template_names(self) -> None:
        """Test that expected template names exist."""
        assert set(TEMPLATES.keys()) == {"minimal", "standard", "full"}

    def test_minimal_template_has_required_fields(self) -> None:
        """Test minimal template has all required attributes."""
        t = MINIMAL_TEMPLATE
        assert t.name == "minimal"
        assert t.display_name == "Minimal"
        assert len(t.description) > 0
        assert len(t.directories) > 0
        assert len(t.files) > 0

    def test_standard_template_has_tests_directory(self) -> None:
        """Test standard template includes tests."""
        assert "tests" in STANDARD_TEMPLATE.directories

    def test_full_template_has_ci_config(self) -> None:
        """Test full template includes CI configuration."""
        assert ".github/workflows/ci.yml" in FULL_TEMPLATE.files

    def test_full_template_has_dockerfile(self) -> None:
        """Test full template includes Docker configuration."""
        assert "Dockerfile" in FULL_TEMPLATE.files

    def test_all_templates_have_gitignore(self) -> None:
        """Test all templates include a .gitignore."""
        for name, template in TEMPLATES.items():
            assert ".gitignore" in template.files, f"{name} missing .gitignore"

    def test_all_templates_have_readme(self) -> None:
        """Test all templates include a README."""
        for name, template in TEMPLATES.items():
            assert "README.md" in template.files, f"{name} missing README.md"

    def test_all_templates_have_pyproject(self) -> None:
        """Test all templates include pyproject.toml."""
        for name, template in TEMPLATES.items():
            assert "pyproject.toml" in template.files, f"{name} missing pyproject.toml"

    def test_templates_are_frozen(self) -> None:
        """Test that templates are immutable."""
        with pytest.raises(AttributeError):
            MINIMAL_TEMPLATE.name = "hacked"  # type: ignore[misc]

    def test_full_template_dev_deps_include_all_tools(self) -> None:
        """Test full template has comprehensive dev dependencies."""
        deps = FULL_TEMPLATE.dev_dependencies
        assert "pytest" in deps
        assert "ruff" in deps
        assert "mypy" in deps


class TestGetTemplate:
    """Tests for the get_template function."""

    def test_get_existing_template(self) -> None:
        """Test retrieving a valid template."""
        template = get_template("minimal")
        assert template.name == "minimal"

    def test_get_standard_template(self) -> None:
        """Test retrieving the standard template."""
        template = get_template("standard")
        assert template.name == "standard"

    def test_get_full_template(self) -> None:
        """Test retrieving the full template."""
        template = get_template("full")
        assert template.name == "full"

    def test_get_unknown_template_raises(self) -> None:
        """Test that requesting unknown template raises KeyError."""
        with pytest.raises(KeyError, match="Unknown template"):
            get_template("nonexistent")


class TestGetTemplateChoices:
    """Tests for the get_template_choices function."""

    def test_returns_list_of_dicts(self) -> None:
        """Test return format is a list of dicts."""
        choices = get_template_choices()
        assert isinstance(choices, list)
        assert len(choices) == 3

    def test_choices_have_required_keys(self) -> None:
        """Test each choice has 'name' and 'value' keys."""
        for choice in get_template_choices():
            assert "name" in choice
            assert "value" in choice

    def test_choices_values_match_template_names(self) -> None:
        """Test choice values are valid template names."""
        values = {c["value"] for c in get_template_choices()}
        assert values == {"minimal", "standard", "full"}

    def test_choices_names_contain_descriptions(self) -> None:
        """Test choice display names contain descriptive text."""
        for choice in get_template_choices():
            assert "-" in choice["name"]  # "Name - description" format
