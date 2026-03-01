# projinit

Interactive CLI tool for scaffolding new Python projects.

## Features

- **Three templates**: `minimal`, `standard`, `full` -- pick the right level of structure
- **Interactive prompts**: arrow-key template selection, validated project name input
- **Progress bars**: visual feedback during file generation and dependency installation
- **Startup banner**: colourful ASCII art greeting

## Installation

```bash
pip install -e ".[dev]"
```

## Usage

```bash
# Interactive mode (default)
projinit

# Specify an output directory
projinit -o ~/projects

# Skip the banner
projinit --no-banner
```

## Templates

| Template | Includes |
|----------|----------|
| **minimal** | `src/` layout, `pyproject.toml`, README, `.gitignore` |
| **standard** | Everything in minimal + tests, ruff linting, Makefile |
| **full** | Everything in standard + Dockerfile, GitHub Actions CI, `.env.example`, mypy |

## Development

```bash
pip install -e ".[dev]"
pytest --cov -q
```

## License

MIT
