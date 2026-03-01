# PPTX VIBE — Presentation AI Studio

[English](README.md) | 日本語

Claude AI を利用して PowerPoint (.pptx) の作成・編集・分析・テーマ適用を行う AI 駆動のプレゼンテーション生成ツールです。

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

## 機能

- **作成** — テンプレートまたはゼロからスライドデッキを生成
- **編集** — 既存プレゼンテーションの修正
- **分析** — .pptx ファイルからのコンテンツ抽出・確認
- **テーマ** — 10種類のプリセット＋カスタムテーマの適用

## クイックスタート

### 必要環境

- Python 3.10 以上
- [Anthropic API キー](https://console.anthropic.com/)

### インストール

```bash
git clone <リポジトリURL>
cd pptx
pip install -r requirements.txt
```

### 設定

プロジェクトルートに `.env` ファイルを作成：

```
ANTHROPIC_API_KEY=あなたのAPIキー
```

### CLI の起動

```bash
python -m cli
```

対話型 CLI で Claude と会話しながらプレゼンテーションを作成・編集できます。生成されたファイルは `output/` に保存されます。

## プロジェクト構成

```
pptx/
├── cli/              # 対話型 CLI アプリケーション
├── output/            # 生成された .pptx ファイル（デフォルト出力先）
├── scripts/           # ユーティリティスクリプト（トランジション、Office ツール等）
├── .claude/skills/    # AI スキル（pptx、theme-factory 等）
├── generate_ai_*.py   # スライド生成のサンプルスクリプト
├── requirements.txt
└── .env               # API キー（コミット対象外）
```

## CLI コマンド

| コマンド | 説明 |
|----------|------|
| `/help` | ヘルプを表示 |
| `/clear` | 会話履歴をクリア |
| `/exit` | アプリケーションを終了 |

## スキル

このプロジェクトでは Claude Agent Skills を利用しています：

- **pptx** — PowerPoint の作成・編集・読み取り・分析
- **theme-factory** — 10種類のプリセットテーマまたはカスタムテーマの適用

## 依存関係

- `python-pptx` — PowerPoint ファイル操作
- `anthropic` — Claude API クライアント
- `rich` — ターミナル表示
- `pyfiglet` — ASCII アートバナー
- `prompt_toolkit` — 対話型プロンプト
- `python-dotenv` — 環境変数の読み込み

## 出力先

生成されたプレゼンテーションは次のディレクトリに保存されます：

```
C:\ai\pptx\output\
```

## ライセンス

詳細は [LICENSE](LICENSE) を参照してください。
