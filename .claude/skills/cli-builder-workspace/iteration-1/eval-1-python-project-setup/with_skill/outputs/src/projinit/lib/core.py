"""Core business logic — template definitions, scaffolding, and validation.

This module must NOT import any UI libraries (rich, questionary, pyfiglet).
It handles pure data and file-system operations only.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Template definitions
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Template:
    """Describes a project template."""

    name: str
    display_name: str
    description: str
    packages: list[str] = field(default_factory=list)
    directories: list[str] = field(default_factory=list)
    stable: bool = True


TEMPLATES: dict[str, Template] = {
    "minimal": Template(
        name="minimal",
        display_name="Minimal",
        description="Bare essentials -- a clean starting point with zero bloat",
        packages=["pytest"],
        directories=[
            "src",
            "tests",
        ],
        stable=True,
    ),
    "standard": Template(
        name="standard",
        display_name="Standard",
        description="Recommended setup -- linting, testing, formatting included",
        packages=[
            "pytest",
            "pytest-cov",
            "ruff",
            "mypy",
            "pre-commit",
        ],
        directories=[
            "src",
            "tests",
            "docs",
        ],
        stable=True,
    ),
    "full": Template(
        name="full",
        display_name="Full",
        description="All batteries included -- CI, Docker, docs, and more",
        packages=[
            "pytest",
            "pytest-cov",
            "pytest-asyncio",
            "ruff",
            "mypy",
            "pre-commit",
            "sphinx",
            "sphinx-rtd-theme",
            "docker-compose",
            "httpx",
            "pydantic",
        ],
        directories=[
            "src",
            "tests",
            "docs",
            "scripts",
            ".github/workflows",
            "docker",
        ],
        stable=True,
    ),
}


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

PROJECT_NAME_RE = re.compile(r"^[a-z][a-z0-9\-]{0,62}[a-z0-9]$")


def validate_project_name(name: str) -> bool:
    """Return True if *name* is a valid, hyphen-separated, lowercase project name."""
    if len(name) < 2:
        return False
    return bool(PROJECT_NAME_RE.match(name))


# ---------------------------------------------------------------------------
# Scaffolding helpers
# ---------------------------------------------------------------------------

def get_template_packages(template_name: str) -> list[str]:
    """Return the list of dependency packages for a given template."""
    tpl = TEMPLATES.get(template_name)
    if tpl is None:
        return []
    return list(tpl.packages)


def create_project_structure(name: str, template_name: str) -> Path:
    """Create the directory tree for a new project.

    Returns the root ``Path`` of the created project.
    """
    tpl = TEMPLATES[template_name]
    root = Path.cwd() / name
    root.mkdir(parents=True, exist_ok=True)

    for directory in tpl.directories:
        (root / directory).mkdir(parents=True, exist_ok=True)

    # Create a package inside src/
    pkg_name = name.replace("-", "_")
    pkg_dir = root / "src" / pkg_name
    pkg_dir.mkdir(parents=True, exist_ok=True)
    (pkg_dir / "__init__.py").write_text(
        f'"""Top-level package for {name}."""\n\n__version__ = "0.1.0"\n',
        encoding="utf-8",
    )

    # Always create a tests/__init__.py
    tests_init = root / "tests" / "__init__.py"
    if not tests_init.exists():
        tests_init.write_text("", encoding="utf-8")

    return root


def write_config_files(name: str, template_name: str) -> None:
    """Write pyproject.toml, README, .gitignore, and template-specific configs."""
    tpl = TEMPLATES[template_name]
    root = Path.cwd() / name
    pkg_name = name.replace("-", "_")
    packages_toml = ",\n".join(f'    "{p}"' for p in tpl.packages)

    # pyproject.toml
    pyproject = textwrap.dedent(f"""\
        [project]
        name = "{name}"
        version = "0.1.0"
        description = ""
        requires-python = ">=3.10"
        dependencies = [
        {packages_toml}
        ]

        [project.optional-dependencies]
        dev = [
            "pytest>=7",
            "pytest-cov",
        ]

        [build-system]
        requires = ["setuptools>=68", "wheel"]
        build-backend = "setuptools.backends._legacy:_Backend"

        [tool.setuptools.packages.find]
        where = ["src"]
    """)
    (root / "pyproject.toml").write_text(pyproject, encoding="utf-8")

    # README.md
    readme = textwrap.dedent(f"""\
        # {name}

        > Generated with **projinit** ({template_name} template)

        ## Getting Started

        ```bash
        cd {name}
        python -m venv .venv
        source .venv/bin/activate   # or .venv\\Scripts\\activate on Windows
        pip install -e ".[dev]"
        ```

        ## Running Tests

        ```bash
        pytest
        ```
    """)
    (root / "README.md").write_text(readme, encoding="utf-8")

    # .gitignore
    gitignore = textwrap.dedent("""\
        __pycache__/
        *.py[cod]
        *$py.class
        .venv/
        venv/
        dist/
        build/
        *.egg-info/
        .eggs/
        .mypy_cache/
        .ruff_cache/
        .pytest_cache/
        htmlcov/
        .coverage
        .env
        *.log
    """)
    (root / ".gitignore").write_text(gitignore, encoding="utf-8")

    # Template-specific extras
    if template_name in ("standard", "full"):
        _write_ruff_config(root)

    if template_name == "full":
        _write_dockerfile(root, name)
        _write_github_ci(root, name)


def _write_ruff_config(root: Path) -> None:
    """Write a ruff configuration section into pyproject.toml (appended)."""
    ruff_section = textwrap.dedent("""\

        [tool.ruff]
        line-length = 100
        target-version = "py310"

        [tool.ruff.lint]
        select = ["E", "F", "I", "W", "UP"]
    """)
    with open(root / "pyproject.toml", "a", encoding="utf-8") as f:
        f.write(ruff_section)


def _write_dockerfile(root: Path, name: str) -> None:
    """Write a minimal Dockerfile."""
    dockerfile = textwrap.dedent(f"""\
        FROM python:3.12-slim
        WORKDIR /app
        COPY . .
        RUN pip install --no-cache-dir .
        CMD ["python", "-m", "{name.replace('-', '_')}"]
    """)
    (root / "docker" / "Dockerfile").write_text(dockerfile, encoding="utf-8")


def _write_github_ci(root: Path, name: str) -> None:
    """Write a GitHub Actions CI workflow."""
    ci_yaml = textwrap.dedent(f"""\
        name: CI

        on:
          push:
            branches: [main]
          pull_request:
            branches: [main]

        jobs:
          test:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - uses: actions/setup-python@v5
                with:
                  python-version: "3.12"
              - run: pip install -e ".[dev]"
              - run: pytest --cov=src/{name.replace('-', '_')} --cov-report=term-missing
    """)
    workflows_dir = root / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    (workflows_dir / "ci.yml").write_text(ci_yaml, encoding="utf-8")


def init_git_repo(name: str) -> None:
    """Initialize a git repository in the project directory.

    Uses ``subprocess`` to call ``git init``. Silently ignores failures
    (e.g. git not installed) so the rest of scaffolding completes.
    """
    import subprocess

    root = Path.cwd() / name
    try:
        subprocess.run(
            ["git", "init"],
            cwd=root,
            capture_output=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass  # git not available — skip silently
