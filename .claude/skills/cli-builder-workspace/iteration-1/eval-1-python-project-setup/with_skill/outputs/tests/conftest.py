"""Shared test fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def tmp_project_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Change CWD to a temporary directory and return it."""
    monkeypatch.chdir(tmp_path)
    return tmp_path
