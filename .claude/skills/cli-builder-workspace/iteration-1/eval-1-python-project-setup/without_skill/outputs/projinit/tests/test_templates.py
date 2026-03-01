"""Tests for the template registry."""

import pytest

from projinit.templates.registry import build_template


class TestBuildTemplateMinimal:
    """Tests for the 'minimal' template."""

    def test_minimal_has_readme(self):
        t = build_template("minimal", "my-app")
        paths = [f.path for f in t.files]
        assert "README.md" in paths

    def test_minimal_has_gitignore(self):
        t = build_template("minimal", "my-app")
        paths = [f.path for f in t.files]
        assert ".gitignore" in paths

    def test_minimal_has_main(self):
        t = build_template("minimal", "my-app")
        paths = [f.path for f in t.files]
        assert "src/my_app/main.py" in paths

    def test_minimal_has_init(self):
        t = build_template("minimal", "my-app")
        paths = [f.path for f in t.files]
        assert "src/my_app/__init__.py" in paths

    def test_minimal_has_pyproject(self):
        t = build_template("minimal", "my-app")
        paths = [f.path for f in t.files]
        assert "pyproject.toml" in paths

    def test_minimal_dev_deps(self):
        t = build_template("minimal", "my-app")
        assert len(t.dev_dependencies) >= 1
        assert any("pytest" in d for d in t.dev_dependencies)


class TestBuildTemplateStandard:
    """Tests for the 'standard' template."""

    def test_standard_has_tests(self):
        t = build_template("standard", "my-app")
        paths = [f.path for f in t.files]
        assert "tests/test_main.py" in paths

    def test_standard_has_makefile(self):
        t = build_template("standard", "my-app")
        paths = [f.path for f in t.files]
        assert "Makefile" in paths

    def test_standard_dev_deps_include_ruff(self):
        t = build_template("standard", "my-app")
        assert any("ruff" in d for d in t.dev_dependencies)


class TestBuildTemplateFull:
    """Tests for the 'full' template."""

    def test_full_has_dockerfile(self):
        t = build_template("full", "my-app")
        paths = [f.path for f in t.files]
        assert "Dockerfile" in paths

    def test_full_has_ci(self):
        t = build_template("full", "my-app")
        paths = [f.path for f in t.files]
        assert ".github/workflows/ci.yml" in paths

    def test_full_has_env_example(self):
        t = build_template("full", "my-app")
        paths = [f.path for f in t.files]
        assert ".env.example" in paths

    def test_full_dev_deps_include_mypy(self):
        t = build_template("full", "my-app")
        assert any("mypy" in d for d in t.dev_dependencies)


class TestBuildTemplateEdgeCases:
    """Edge case tests."""

    def test_unknown_template_raises(self):
        with pytest.raises(ValueError, match="Unknown template"):
            build_template("nonexistent", "my-app")

    def test_hyphen_to_underscore_in_paths(self):
        t = build_template("minimal", "my-cool-project")
        paths = [f.path for f in t.files]
        assert "src/my_cool_project/__init__.py" in paths
        assert "src/my_cool_project/main.py" in paths

    def test_template_label_not_empty(self):
        for name in ("minimal", "standard", "full"):
            t = build_template(name, "x")
            assert t.label
            assert t.description
