"""Shared fixtures for projinit tests."""

from __future__ import annotations

import pytest


@pytest.fixture()
def tmp_project_dir(tmp_path):
    """Return a temporary directory suitable for scaffolding tests."""
    return tmp_path
