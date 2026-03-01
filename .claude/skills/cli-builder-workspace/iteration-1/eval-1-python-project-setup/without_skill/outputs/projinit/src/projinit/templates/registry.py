"""Template registry: defines the three project templates and their contents."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TemplateFile:
    """A single file to be generated from a template."""

    path: str
    content: str


@dataclass(frozen=True)
class TemplateDef:
    """Full definition of a project template."""

    name: str
    label: str
    description: str
    dependencies: list[str] = field(default_factory=list)
    dev_dependencies: list[str] = field(default_factory=list)
    files: list[TemplateFile] = field(default_factory=list)


def _readme(project_name: str, description: str) -> str:
    return f"# {project_name}\n\n{description}\n"


def _gitignore() -> str:
    return (
        "__pycache__/\n"
        "*.py[cod]\n"
        "*$py.class\n"
        "*.so\n"
        "dist/\n"
        "build/\n"
        "*.egg-info/\n"
        ".eggs/\n"
        "*.egg\n"
        ".env\n"
        ".venv/\n"
        "venv/\n"
        ".mypy_cache/\n"
        ".pytest_cache/\n"
        ".ruff_cache/\n"
        "htmlcov/\n"
        ".coverage\n"
        "coverage.xml\n"
    )


def _main_py(project_name: str) -> str:
    module = project_name.replace("-", "_")
    return (
        f'"""Entry point for {project_name}."""\n'
        "\n"
        "\n"
        "def main() -> None:\n"
        f'    """Run {module}."""\n'
        f'    print("Hello from {project_name}!")\n'
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    main()\n"
    )


def _test_main(project_name: str) -> str:
    module = project_name.replace("-", "_")
    return (
        f'"""Tests for {module}.main."""\n'
        "\n"
        f"from {module}.main import main\n"
        "\n"
        "\n"
        "def test_main(capsys):\n"
        '    """Verify main prints greeting."""\n'
        "    main()\n"
        "    captured = capsys.readouterr()\n"
        f'    assert "{project_name}" in captured.out\n'
    )


def _pyproject_toml(project_name: str, deps: list[str], dev_deps: list[str]) -> str:
    module = project_name.replace("-", "_")
    dep_lines = "\n".join(f'    "{d}",' for d in deps)
    dev_dep_lines = "\n".join(f'    "{d}",' for d in dev_deps)

    sections = [
        "[build-system]",
        'requires = ["setuptools>=68.0", "wheel"]',
        'build-backend = "setuptools.backends._legacy:_Backend"',
        "",
        "[project]",
        f'name = "{project_name}"',
        'version = "0.1.0"',
        f'description = "A new project: {project_name}"',
        'requires-python = ">=3.9"',
        "dependencies = [",
        dep_lines,
        "]",
        "",
        "[project.optional-dependencies]",
        "dev = [",
        dev_dep_lines,
        "]",
        "",
        "[tool.setuptools.packages.find]",
        f'where = ["src"]',
        "",
        "[tool.pytest.ini_options]",
        'testpaths = ["tests"]',
    ]
    return "\n".join(sections) + "\n"


def _dockerfile(project_name: str) -> str:
    module = project_name.replace("-", "_")
    return (
        "FROM python:3.12-slim\n"
        "\n"
        "WORKDIR /app\n"
        "\n"
        "COPY pyproject.toml .\n"
        "COPY src/ src/\n"
        "\n"
        "RUN pip install --no-cache-dir .\n"
        "\n"
        f'CMD ["python", "-m", "{module}.main"]\n'
    )


def _github_ci(project_name: str) -> str:
    return (
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
        "      - name: Set up Python ${{ matrix.python-version }}\n"
        "        uses: actions/setup-python@v5\n"
        "        with:\n"
        "          python-version: ${{ matrix.python-version }}\n"
        "      - name: Install dependencies\n"
        '        run: pip install ".[dev]"\n'
        "      - name: Lint\n"
        "        run: ruff check src/ tests/\n"
        "      - name: Test\n"
        "        run: pytest --cov -q\n"
    )


def _makefile(project_name: str) -> str:
    return (
        ".PHONY: install test lint fmt clean\n"
        "\n"
        "install:\n"
        '\tpip install -e ".[dev]"\n'
        "\n"
        "test:\n"
        "\tpytest --cov -q\n"
        "\n"
        "lint:\n"
        "\truff check src/ tests/\n"
        "\n"
        "fmt:\n"
        "\truff format src/ tests/\n"
        "\n"
        "clean:\n"
        "\trm -rf dist/ build/ *.egg-info .pytest_cache .ruff_cache htmlcov .coverage\n"
    )


def build_template(template_name: str, project_name: str) -> TemplateDef:
    """Build a TemplateDef for the given template name and project name.

    Args:
        template_name: One of 'minimal', 'standard', 'full'.
        project_name: The user-provided project name.

    Returns:
        A fully populated TemplateDef.

    Raises:
        ValueError: If template_name is not recognized.
    """
    module = project_name.replace("-", "_")

    if template_name == "minimal":
        deps: list[str] = []
        dev_deps = ["pytest>=7.0"]
        files = [
            TemplateFile("README.md", _readme(project_name, "A minimal Python project.")),
            TemplateFile(".gitignore", _gitignore()),
            TemplateFile(
                "pyproject.toml",
                _pyproject_toml(project_name, deps, dev_deps),
            ),
            TemplateFile(f"src/{module}/__init__.py", '"""Package root."""\n'),
            TemplateFile(f"src/{module}/main.py", _main_py(project_name)),
        ]
        return TemplateDef(
            name="minimal",
            label="Minimal",
            description="Bare-bones Python package with src layout",
            dependencies=deps,
            dev_dependencies=dev_deps,
            files=files,
        )

    if template_name == "standard":
        deps = []
        dev_deps = ["pytest>=7.0", "pytest-cov>=4.0", "ruff>=0.4.0"]
        files = [
            TemplateFile("README.md", _readme(project_name, "A standard Python project with testing and linting.")),
            TemplateFile(".gitignore", _gitignore()),
            TemplateFile(
                "pyproject.toml",
                _pyproject_toml(project_name, deps, dev_deps),
            ),
            TemplateFile(f"src/{module}/__init__.py", '"""Package root."""\n'),
            TemplateFile(f"src/{module}/main.py", _main_py(project_name)),
            TemplateFile(f"tests/__init__.py", ""),
            TemplateFile(f"tests/test_main.py", _test_main(project_name)),
            TemplateFile("Makefile", _makefile(project_name)),
        ]
        return TemplateDef(
            name="standard",
            label="Standard",
            description="Python package with tests, linting (ruff), and Makefile",
            dependencies=deps,
            dev_dependencies=dev_deps,
            files=files,
        )

    if template_name == "full":
        deps = []
        dev_deps = [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "ruff>=0.4.0",
            "mypy>=1.8.0",
        ]
        files = [
            TemplateFile("README.md", _readme(project_name, "A full-featured Python project with CI, Docker, and more.")),
            TemplateFile(".gitignore", _gitignore()),
            TemplateFile(
                "pyproject.toml",
                _pyproject_toml(project_name, deps, dev_deps),
            ),
            TemplateFile(f"src/{module}/__init__.py", '"""Package root."""\n'),
            TemplateFile(f"src/{module}/main.py", _main_py(project_name)),
            TemplateFile(f"tests/__init__.py", ""),
            TemplateFile(f"tests/test_main.py", _test_main(project_name)),
            TemplateFile("Makefile", _makefile(project_name)),
            TemplateFile("Dockerfile", _dockerfile(project_name)),
            TemplateFile(
                ".github/workflows/ci.yml",
                _github_ci(project_name),
            ),
            TemplateFile(".env.example", "# Environment variables\n# DATABASE_URL=\n"),
        ]
        return TemplateDef(
            name="full",
            label="Full",
            description="Everything: CI/CD, Docker, env config, type checking",
            dependencies=deps,
            dev_dependencies=dev_deps,
            files=files,
        )

    raise ValueError(f"Unknown template: {template_name!r}")
