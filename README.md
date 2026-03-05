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

## Design Prompts — How to Get Great Slides

Just describe what you want in natural language. Here are prompt examples from simple to advanced:

### Basic

```
Claude最新情報のプレゼンを作って
```

```
Create a 10-slide pitch deck for a SaaS startup
```

### With Design Direction

```
ダークテーマでAI戦略の資料を作って。アクセントカラーはティール。
```

```
Make a product launch deck with a coral & navy color scheme, large stat callouts, and icon grids.
```

### With Theme

```
セールス報告書を作って。theme-factoryでMinimal Darkテーマを適用して。
```

```
Create a quarterly report and apply the "Ocean Gradient" theme.
```

### Editing Existing Files

```
output/my_deck.pptx のスライド3のグラフを更新して
```

```
Add speaker notes to all slides in output/presentation.pptx
```

### Advanced — Full Control

```
16:9 ワイドで、2カラムレイアウト中心の資料を作成。
背景はダークネイビー(#0F172A)、アクセントはアンバー(#D4A574)。
フォントはCalibri、タイトル36pt、本文14pt。
スライド末尾にページ番号とフッターラインを入れて。
```

### Tips

| Tip | Example |
|-----|---------|
| Specify slide count | `10枚で` / `in 8 slides` |
| Request layout types | `2カラム` / `grid layout` / `stat callouts` |
| Set color palette | `ティール＆ゴールド` / `dark theme with coral accent` |
| Add charts | `売上推移の棒グラフを含めて` / `include a bar chart` |
| Apply theme | `theme-factoryでテーマ適用` / `apply Midnight Executive theme` |

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
