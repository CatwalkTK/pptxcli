"""Template definitions for project scaffolding.

Each template describes a preset level of project complexity, including
which files to generate and which packages to install.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TemplateConfig:
    """Immutable configuration for a single project template."""

    label: str
    description: str
    packages: tuple[str, ...]
    directories: tuple[str, ...]
    files: tuple[tuple[str, str], ...]  # (relative_path, content)


# ---------------------------------------------------------------------------
# Shared snippets
# ---------------------------------------------------------------------------

_GITIGNORE = """\
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
.env
.eggs/
*.egg
.mypy_cache/
.pytest_cache/
"""

_README_TEMPLATE = """\
# {name}

A new project scaffolded with **projinit**.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\\Scripts\\activate on Windows
pip install -e .
```
"""

_INIT_PY = '"""Package root."""\n'

_MAIN_PY = """\
def main() -> None:
    print("Hello from {name}!")


if __name__ == "__main__":
    main()
"""

# ---------------------------------------------------------------------------
# Template catalogue
# ---------------------------------------------------------------------------

TEMPLATES: dict[str, TemplateConfig] = {
    "minimal": TemplateConfig(
        label="Minimal",
        description="Bare essentials - single module, no tests",
        packages=("setuptools", "wheel"),
        directories=(
            "src/{name_under}",
        ),
        files=(
            ("src/{name_under}/__init__.py", _INIT_PY),
            ("src/{name_under}/main.py", _MAIN_PY),
            (".gitignore", _GITIGNORE),
            ("README.md", _README_TEMPLATE),
            ("pyproject.toml", """\
[project]
name = "{name}"
version = "0.1.0"
requires-python = ">=3.10"

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.setuptools.packages.find]
where = ["src"]
"""),
        ),
    ),
    "standard": TemplateConfig(
        label="Standard",
        description="Recommended - src layout, tests, linting",
        packages=("setuptools", "wheel", "pytest", "ruff", "mypy"),
        directories=(
            "src/{name_under}",
            "tests",
        ),
        files=(
            ("src/{name_under}/__init__.py", _INIT_PY),
            ("src/{name_under}/main.py", _MAIN_PY),
            ("tests/__init__.py", ""),
            ("tests/test_main.py", """\
from {name_under}.main import main


def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "{name}" in captured.out
"""),
            (".gitignore", _GITIGNORE),
            ("README.md", _README_TEMPLATE),
            ("pyproject.toml", """\
[project]
name = "{name}"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7",
    "pytest-cov",
    "ruff",
    "mypy",
]

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.mypy]
python_version = "3.10"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
"""),
        ),
    ),
    "full": TemplateConfig(
        label="Full",
        description="Everything included - CI, Docker, docs, pre-commit",
        packages=(
            "setuptools",
            "wheel",
            "pytest",
            "pytest-cov",
            "ruff",
            "mypy",
            "pre-commit",
            "mkdocs",
        ),
        directories=(
            "src/{name_under}",
            "tests",
            "docs",
            ".github/workflows",
        ),
        files=(
            ("src/{name_under}/__init__.py", _INIT_PY),
            ("src/{name_under}/main.py", _MAIN_PY),
            ("tests/__init__.py", ""),
            ("tests/test_main.py", """\
from {name_under}.main import main


def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "{name}" in captured.out
"""),
            (".gitignore", _GITIGNORE),
            ("README.md", _README_TEMPLATE),
            ("Dockerfile", """\
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .
CMD ["python", "-m", "{name_under}"]
"""),
            (".github/workflows/ci.yml", """\
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{{{ matrix.python-version }}}}
      - run: pip install -e ".[dev]"
      - run: pytest --cov
      - run: ruff check src/
      - run: mypy src/
"""),
            (".pre-commit-config.yaml", """\
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
"""),
            ("docs/index.md", "# {name}\n\nWelcome to the {name} documentation.\n"),
            ("pyproject.toml", """\
[project]
name = "{name}"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7",
    "pytest-cov",
    "ruff",
    "mypy",
    "pre-commit",
    "mkdocs",
]

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.mypy]
python_version = "3.10"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing"
"""),
        ),
    ),
}
