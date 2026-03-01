"""Project scaffolding logic -- creates directories and writes files.

This module contains pure business logic with no UI imports.
"""

from __future__ import annotations

import re
from pathlib import Path

from projinit.lib.templates import TEMPLATES


def _to_python_name(name: str) -> str:
    """Convert a project name like ``my-project`` to a Python package
    name like ``my_project``."""
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    sanitized = re.sub(r"_+", "_", sanitized).strip("_").lower()
    return sanitized or "project"


def scaffold_project(
    *,
    name: str,
    template_key: str,
    base_dir: Path | None = None,
) -> Path:
    """Create the full project directory tree on disk.

    Parameters
    ----------
    name:
        Human-readable project name (e.g. ``"my-project"``).
    template_key:
        Key into ``TEMPLATES`` (``"minimal"`` / ``"standard"`` / ``"full"``).
    base_dir:
        Parent directory in which the project folder will be created.
        Defaults to the current working directory.

    Returns
    -------
    Path
        Absolute path of the newly created project root.
    """
    template = TEMPLATES[template_key]
    base_dir = base_dir or Path.cwd()
    project_root = base_dir / name
    name_under = _to_python_name(name)

    # Create directories
    project_root.mkdir(parents=True, exist_ok=True)
    for dir_template in template.directories:
        dir_path = project_root / dir_template.format(
            name=name,
            name_under=name_under,
        )
        dir_path.mkdir(parents=True, exist_ok=True)

    # Write files
    for file_template, content_template in template.files:
        file_path = project_root / file_template.format(
            name=name,
            name_under=name_under,
        )
        file_path.parent.mkdir(parents=True, exist_ok=True)
        rendered = content_template.format(
            name=name,
            name_under=name_under,
        )
        file_path.write_text(rendered, encoding="utf-8")

    return project_root
