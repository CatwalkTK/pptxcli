# PPTX VIBE — Presentation AI Studio

[日本語](README.ja.md) | English

AI-powered presentation generator that creates, edits, analyzes, and themes PowerPoint (.pptx) files using Claude AI.

```
 ██████  ██████  ████████ ██   ██
 ██   ██ ██   ██    ██     ██ ██
 ██████  ██████     ██      ███
 ██      ██         ██     ██ ██
 ██      ██         ██    ██   ██

 ██    ██ ██ ██████  ███████
 ██    ██ ██ ██   ██ ██
 ██    ██ ██ ██████  █████
  ██  ██  ██ ██   ██ ██
   ████   ██ ██████  ███████
  ░▒▓█ Presentation AI Studio █▓▒░
```

## Features

- **Create** — Generate slide decks from scratch or from templates
- **Edit** — Modify existing presentations
- **Analyze** — Extract and inspect content from .pptx files
- **Theme** — Apply professional themes (10 presets + custom themes)

## Quick Start

### Prerequisites

- Python 3.10+
- [Anthropic API key](https://console.anthropic.com/)

### Installation

```bash
git clone <repository-url>
cd pptx
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your-api-key-here
```

### Run the CLI

```bash
python -m cli
```

The interactive CLI lets you chat with Claude to create and edit presentations. Generated files are saved to `output/`.

## Project Structure

```
pptx/
├── cli/              # Interactive CLI application
├── output/            # Generated .pptx files (default output directory)
├── scripts/           # Utility scripts (transitions, office tools)
├── .claude/skills/    # AI skills (pptx, theme-factory, etc.)
├── generate_ai_*.py   # Example slide generation scripts
├── requirements.txt
└── .env               # API keys (not committed)
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help |
| `/clear` | Clear conversation history |
| `/exit` | Exit the application |

## Skills

This project uses Claude Agent Skills for specialized tasks:

- **pptx** — Create, edit, read, and analyze PowerPoint files
- **theme-factory** — Apply 10 preset themes or generate custom themes

## Dependencies

- `python-pptx` — PowerPoint file manipulation
- `anthropic` — Claude API client
- `rich` — Terminal formatting
- `pyfiglet` — ASCII art banners
- `prompt_toolkit` — Interactive prompts
- `python-dotenv` — Environment variable loading

## Output

All generated presentations are saved to:

```
C:\ai\pptx\output\
```

## License

See [LICENSE](LICENSE) for details.
