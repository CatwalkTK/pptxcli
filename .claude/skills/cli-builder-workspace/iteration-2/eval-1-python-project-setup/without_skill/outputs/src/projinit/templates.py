"""Project template definitions for projinit."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Template:
    """Represents a project template configuration."""

    name: str
    display_name: str
    description: str
    directories: tuple[str, ...]
    files: dict[str, str]
    dependencies: tuple[str, ...]
    dev_dependencies: tuple[str, ...]


MINIMAL_TEMPLATE = Template(
    name="minimal",
    display_name="Minimal",
    description="Bare-bones project with just the essentials",
    directories=(
        "src",
    ),
    files={
        "src/__init__.py": '"""{{project_name}} - A new project."""\n',
        "src/main.py": (
            '"""Main entry point for {{project_name}}."""\n'
            "\n\n"
            "def main() -> None:\n"
            '    """Run the application."""\n'
            '    print("Hello from {{project_name}}!")\n'
            "\n\n"
            'if __name__ == "__main__":\n'
            "    main()\n"
        ),
        "pyproject.toml": (
            "[build-system]\n"
            'requires = ["hatchling"]\n'
            'build-backend = "hatchling.build"\n'
            "\n"
            "[project]\n"
            'name = "{{project_name}}"\n'
            'version = "0.1.0"\n'
            'description = ""\n'
            'requires-python = ">=3.10"\n'
            "dependencies = []\n"
        ),
        ".gitignore": (
            "__pycache__/\n"
            "*.py[cod]\n"
            "*$py.class\n"
            "*.egg-info/\n"
            "dist/\n"
            "build/\n"
            ".venv/\n"
            ".env\n"
        ),
        "README.md": "# {{project_name}}\n\nA new project.\n",
    },
    dependencies=(),
    dev_dependencies=("pytest",),
)

STANDARD_TEMPLATE = Template(
    name="standard",
    display_name="Standard",
    description="Well-structured project with testing and linting",
    directories=(
        "src",
        "tests",
        "docs",
    ),
    files={
        "src/__init__.py": '"""{{project_name}} - A new project."""\n\n__version__ = "0.1.0"\n',
        "src/main.py": (
            '"""Main entry point for {{project_name}}."""\n'
            "\n"
            "import logging\n"
            "\n"
            "logger = logging.getLogger(__name__)\n"
            "\n\n"
            "def main() -> None:\n"
            '    """Run the application."""\n'
            "    logging.basicConfig(level=logging.INFO)\n"
            '    logger.info("Starting {{project_name}}")\n'
            '    print("Hello from {{project_name}}!")\n'
            "\n\n"
            'if __name__ == "__main__":\n'
            "    main()\n"
        ),
        "tests/__init__.py": "",
        "tests/test_main.py": (
            '"""Tests for main module."""\n'
            "\n"
            "from src.main import main\n"
            "\n\n"
            "def test_main(capsys):\n"
            '    """Test main function output."""\n'
            "    main()\n"
            "    captured = capsys.readouterr()\n"
            '    assert "Hello from {{project_name}}" in captured.out\n'
        ),
        "pyproject.toml": (
            "[build-system]\n"
            'requires = ["hatchling"]\n'
            'build-backend = "hatchling.build"\n'
            "\n"
            "[project]\n"
            'name = "{{project_name}}"\n'
            'version = "0.1.0"\n'
            'description = ""\n'
            'requires-python = ">=3.10"\n'
            "dependencies = []\n"
            "\n"
            "[project.optional-dependencies]\n"
            "dev = [\n"
            '    "pytest>=7.0.0",\n'
            '    "pytest-cov>=4.0.0",\n'
            '    "ruff>=0.1.0",\n'
            "]\n"
            "\n"
            "[tool.pytest.ini_options]\n"
            'testpaths = ["tests"]\n'
            'addopts = "--tb=short -q"\n'
            "\n"
            "[tool.ruff]\n"
            "line-length = 88\n"
            'target-version = "py310"\n'
            "\n"
            "[tool.ruff.lint]\n"
            'select = ["E", "F", "I", "N", "W"]\n'
        ),
        ".gitignore": (
            "__pycache__/\n"
            "*.py[cod]\n"
            "*$py.class\n"
            "*.egg-info/\n"
            "dist/\n"
            "build/\n"
            ".venv/\n"
            ".env\n"
            "htmlcov/\n"
            ".coverage\n"
            "coverage.xml\n"
            ".pytest_cache/\n"
            ".ruff_cache/\n"
        ),
        "README.md": (
            "# {{project_name}}\n"
            "\n"
            "A new project.\n"
            "\n"
            "## Getting Started\n"
            "\n"
            "```bash\n"
            "pip install -e '.[dev]'\n"
            "```\n"
            "\n"
            "## Testing\n"
            "\n"
            "```bash\n"
            "pytest\n"
            "```\n"
        ),
    },
    dependencies=(),
    dev_dependencies=("pytest", "pytest-cov", "ruff"),
)

FULL_TEMPLATE = Template(
    name="full",
    display_name="Full",
    description="Production-ready project with CI/CD, Docker, and docs",
    directories=(
        "src",
        "tests",
        "tests/unit",
        "tests/integration",
        "docs",
        "scripts",
        ".github/workflows",
    ),
    files={
        "src/__init__.py": '"""{{project_name}} - A new project."""\n\n__version__ = "0.1.0"\n',
        "src/main.py": (
            '"""Main entry point for {{project_name}}."""\n'
            "\n"
            "import logging\n"
            "import sys\n"
            "\n"
            "logger = logging.getLogger(__name__)\n"
            "\n\n"
            "def setup_logging(level: str = \"INFO\") -> None:\n"
            '    """Configure application logging."""\n'
            "    logging.basicConfig(\n"
            "        level=getattr(logging, level.upper()),\n"
            '        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",\n'
            '        datefmt="%Y-%m-%d %H:%M:%S",\n'
            "    )\n"
            "\n\n"
            "def main() -> int:\n"
            '    """Run the application."""\n'
            "    setup_logging()\n"
            '    logger.info("Starting {{project_name}}")\n'
            '    print("Hello from {{project_name}}!")\n'
            "    return 0\n"
            "\n\n"
            'if __name__ == "__main__":\n'
            "    sys.exit(main())\n"
        ),
        "src/config.py": (
            '"""Configuration management for {{project_name}}."""\n'
            "\n"
            "from __future__ import annotations\n"
            "\n"
            "import os\n"
            "from dataclasses import dataclass\n"
            "\n\n"
            "@dataclass(frozen=True)\n"
            "class Config:\n"
            '    """Application configuration."""\n'
            "\n"
            '    app_name: str = "{{project_name}}"\n'
            '    debug: bool = False\n'
            '    log_level: str = "INFO"\n'
            "\n"
            "    @classmethod\n"
            "    def from_env(cls) -> Config:\n"
            '        """Create config from environment variables."""\n'
            "        return cls(\n"
            '            app_name=os.getenv("APP_NAME", "{{project_name}}"),\n'
            '            debug=os.getenv("DEBUG", "false").lower() == "true",\n'
            '            log_level=os.getenv("LOG_LEVEL", "INFO"),\n'
            "        )\n"
        ),
        "tests/__init__.py": "",
        "tests/unit/__init__.py": "",
        "tests/integration/__init__.py": "",
        "tests/unit/test_main.py": (
            '"""Unit tests for main module."""\n'
            "\n"
            "from src.main import main\n"
            "\n\n"
            "def test_main_returns_zero():\n"
            '    """Test main returns success code."""\n'
            "    assert main() == 0\n"
            "\n\n"
            "def test_main_output(capsys):\n"
            '    """Test main function output."""\n'
            "    main()\n"
            "    captured = capsys.readouterr()\n"
            '    assert "Hello from {{project_name}}" in captured.out\n'
        ),
        "tests/unit/test_config.py": (
            '"""Unit tests for config module."""\n'
            "\n"
            "from src.config import Config\n"
            "\n\n"
            "def test_default_config():\n"
            '    """Test default configuration values."""\n'
            "    config = Config()\n"
            '    assert config.app_name == "{{project_name}}"\n'
            "    assert config.debug is False\n"
            '    assert config.log_level == "INFO"\n'
            "\n\n"
            "def test_config_from_env(monkeypatch):\n"
            '    """Test config from environment variables."""\n'
            '    monkeypatch.setenv("DEBUG", "true")\n'
            '    monkeypatch.setenv("LOG_LEVEL", "DEBUG")\n'
            "    config = Config.from_env()\n"
            "    assert config.debug is True\n"
            '    assert config.log_level == "DEBUG"\n'
        ),
        "pyproject.toml": (
            "[build-system]\n"
            'requires = ["hatchling"]\n'
            'build-backend = "hatchling.build"\n'
            "\n"
            "[project]\n"
            'name = "{{project_name}}"\n'
            'version = "0.1.0"\n'
            'description = ""\n'
            'requires-python = ">=3.10"\n'
            "dependencies = []\n"
            "\n"
            "[project.scripts]\n"
            '{{project_name}} = "src.main:main"\n'
            "\n"
            "[project.optional-dependencies]\n"
            "dev = [\n"
            '    "pytest>=7.0.0",\n'
            '    "pytest-cov>=4.0.0",\n'
            '    "pytest-mock>=3.10.0",\n'
            '    "ruff>=0.1.0",\n'
            '    "mypy>=1.0.0",\n'
            '    "pre-commit>=3.0.0",\n'
            "]\n"
            "\n"
            "[tool.pytest.ini_options]\n"
            'testpaths = ["tests"]\n'
            'addopts = "--tb=short -q --cov=src --cov-report=term-missing"\n'
            "\n"
            "[tool.ruff]\n"
            "line-length = 88\n"
            'target-version = "py310"\n'
            "\n"
            "[tool.ruff.lint]\n"
            'select = ["E", "F", "I", "N", "W", "UP", "B", "SIM", "RUF"]\n'
            "\n"
            "[tool.mypy]\n"
            "python_version = \"3.10\"\n"
            "strict = true\n"
            "warn_return_any = true\n"
            "warn_unused_configs = true\n"
            "\n"
            "[tool.coverage.run]\n"
            'source = ["src"]\n'
            "branch = true\n"
            "\n"
            "[tool.coverage.report]\n"
            "show_missing = true\n"
            "fail_under = 80\n"
        ),
        ".gitignore": (
            "# Python\n"
            "__pycache__/\n"
            "*.py[cod]\n"
            "*$py.class\n"
            "*.egg-info/\n"
            "dist/\n"
            "build/\n"
            "\n"
            "# Virtual environments\n"
            ".venv/\n"
            "venv/\n"
            ".env\n"
            "\n"
            "# Testing\n"
            "htmlcov/\n"
            ".coverage\n"
            "coverage.xml\n"
            ".pytest_cache/\n"
            "\n"
            "# Tools\n"
            ".ruff_cache/\n"
            ".mypy_cache/\n"
            "\n"
            "# IDE\n"
            ".vscode/\n"
            ".idea/\n"
            "*.swp\n"
            "*.swo\n"
            "\n"
            "# Docker\n"
            "*.log\n"
        ),
        "Dockerfile": (
            "FROM python:3.12-slim AS base\n"
            "\n"
            "WORKDIR /app\n"
            "\n"
            "COPY pyproject.toml .\n"
            "RUN pip install --no-cache-dir .\n"
            "\n"
            "COPY src/ src/\n"
            "\n"
            'CMD ["python", "-m", "src.main"]\n'
        ),
        ".dockerignore": (
            "__pycache__\n"
            "*.py[cod]\n"
            ".venv\n"
            ".git\n"
            ".github\n"
            "tests\n"
            "docs\n"
            "htmlcov\n"
            ".coverage\n"
            "*.egg-info\n"
        ),
        ".github/workflows/ci.yml": (
            "name: CI\n"
            "\n"
            "on:\n"
            "  push:\n"
            "    branches: [main]\n"
            "  pull_request:\n"
            "    branches: [main]\n"
            "\n"
            "jobs:\n"
            "  test:\n"
            "    runs-on: ubuntu-latest\n"
            "    strategy:\n"
            "      matrix:\n"
            '        python-version: ["3.10", "3.11", "3.12"]\n'
            "    steps:\n"
            "      - uses: actions/checkout@v4\n"
            "      - uses: actions/setup-python@v5\n"
            "        with:\n"
            "          python-version: ${{ matrix.python-version }}\n"
            "      - run: pip install -e '.[dev]'\n"
            "      - run: ruff check src/ tests/\n"
            "      - run: mypy src/\n"
            "      - run: pytest --cov --cov-report=xml\n"
        ),
        ".pre-commit-config.yaml": (
            "repos:\n"
            "  - repo: https://github.com/astral-sh/ruff-pre-commit\n"
            "    rev: v0.3.0\n"
            "    hooks:\n"
            "      - id: ruff\n"
            "        args: [--fix]\n"
            "      - id: ruff-format\n"
        ),
        "Makefile": (
            ".PHONY: install test lint format clean\n"
            "\n"
            "install:\n"
            "\tpip install -e '.[dev]'\n"
            "\tpre-commit install\n"
            "\n"
            "test:\n"
            "\tpytest\n"
            "\n"
            "lint:\n"
            "\truff check src/ tests/\n"
            "\tmypy src/\n"
            "\n"
            "format:\n"
            "\truff format src/ tests/\n"
            "\truff check --fix src/ tests/\n"
            "\n"
            "clean:\n"
            "\trm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache .mypy_cache htmlcov\n"
            "\tfind . -type d -name __pycache__ -exec rm -rf {} +\n"
        ),
        "README.md": (
            "# {{project_name}}\n"
            "\n"
            "A new project.\n"
            "\n"
            "## Getting Started\n"
            "\n"
            "```bash\n"
            "# Install with dev dependencies\n"
            "make install\n"
            "\n"
            "# Or manually\n"
            "pip install -e '.[dev]'\n"
            "```\n"
            "\n"
            "## Development\n"
            "\n"
            "```bash\n"
            "# Run tests\n"
            "make test\n"
            "\n"
            "# Run linters\n"
            "make lint\n"
            "\n"
            "# Format code\n"
            "make format\n"
            "```\n"
            "\n"
            "## Docker\n"
            "\n"
            "```bash\n"
            "docker build -t {{project_name}} .\n"
            "docker run {{project_name}}\n"
            "```\n"
        ),
    },
    dependencies=(),
    dev_dependencies=("pytest", "pytest-cov", "pytest-mock", "ruff", "mypy", "pre-commit"),
)

TEMPLATES: dict[str, Template] = {
    "minimal": MINIMAL_TEMPLATE,
    "standard": STANDARD_TEMPLATE,
    "full": FULL_TEMPLATE,
}


def get_template(name: str) -> Template:
    """Retrieve a template by name.

    Args:
        name: Template identifier ('minimal', 'standard', or 'full').

    Returns:
        The requested Template.

    Raises:
        KeyError: If the template name is not found.
    """
    if name not in TEMPLATES:
        raise KeyError(f"Unknown template: {name}. Available: {', '.join(TEMPLATES)}")
    return TEMPLATES[name]


def get_template_choices() -> list[dict[str, str]]:
    """Return template choices formatted for questionary.

    Returns:
        List of choice dicts with 'name' and 'value' keys.
    """
    return [
        {
            "name": f"{t.display_name:10s} - {t.description}",
            "value": t.name,
        }
        for t in TEMPLATES.values()
    ]
