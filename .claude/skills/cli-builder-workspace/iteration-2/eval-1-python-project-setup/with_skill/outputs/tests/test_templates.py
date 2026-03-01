"""Tests for template definitions."""

from __future__ import annotations

import pytest

from projinit.lib.templates import TEMPLATES, TemplateConfig


def test_all_three_templates_defined() -> None:
    """The catalogue should contain minimal, standard, and full."""
    assert "minimal" in TEMPLATES
    assert "standard" in TEMPLATES
    assert "full" in TEMPLATES


@pytest.mark.parametrize("key", list(TEMPLATES.keys()))
def test_template_is_frozen_dataclass(key: str) -> None:
    cfg = TEMPLATES[key]
    assert isinstance(cfg, TemplateConfig)
    # TemplateConfig is frozen -- mutation should raise
    with pytest.raises(AttributeError):
        cfg.label = "hacked"  # type: ignore[misc]


@pytest.mark.parametrize("key", list(TEMPLATES.keys()))
def test_template_has_packages(key: str) -> None:
    assert len(TEMPLATES[key].packages) > 0


@pytest.mark.parametrize("key", list(TEMPLATES.keys()))
def test_template_has_pyproject_file(key: str) -> None:
    """Every template should include a pyproject.toml."""
    file_names = [path for path, _ in TEMPLATES[key].files]
    assert any("pyproject.toml" in f for f in file_names)
