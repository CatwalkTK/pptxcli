# PPTX VIBE - Presentation Generator

## ⚠️ 最重要ルール（コードを書く前に必ず読め）

### 1. SKILLファイルの読み込み（絶対必須）

**プレゼンテーションのコードを1行でも書く前に、必ず以下を読み込むこと：**

```
view_file: .claude/skills/pptx/SKILL.md
view_file: .claude/skills/pptx/pptxgenjs.md
```

既存ファイル編集時は追加で：
```
view_file: .claude/skills/pptx/editing.md
```

### 2. 絶対禁止デザイン（違反したら作り直し）

以下のスライドは**ゴミ**。絶対に作るな：
- ❌ 白背景 + 黒テキストだけのスライド
- ❌ 全スライド同じレイアウト
- ❌ テキストだけのスライド（ビジュアル要素なし）
- ❌ フォント未指定（デフォルトのまま）
- ❌ カラーパレット未定義で作成開始
- ❌ python-pptxで直接コードを書く（PptxGenJSを使うこと）

### 3. タイトルスライドの正しい例（このレベルが最低基準）

```javascript
const pptxgen = require("pptxgenjs");
let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

// === カラーパレットを最初に定義する ===
const COLORS = {
  primary: "1E2761",    // ダークネイビー
  secondary: "CADCFC",  // アイスブルー
  accent: "F96167",     // コーラル
  text: "FFFFFF",       // ホワイト
  bodyText: "2D3436",   // ダークグレー
  lightBg: "F8F9FA",    // ライトグレー
};
const FONTS = { header: "Georgia", body: "Calibri" };

// === タイトルスライド（暗い背景 + 白テキスト）===
let titleSlide = pres.addSlide();
titleSlide.background = { color: COLORS.primary };
// 装飾: アクセントの図形
titleSlide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.15, h: 5.625,
  fill: { color: COLORS.accent }
});
titleSlide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 4.2, w: 10, h: 0.08,
  fill: { color: COLORS.secondary, transparency: 50 }
});
titleSlide.addText("プレゼンテーションタイトル", {
  x: 0.8, y: 1.5, w: 8.5, h: 1.5,
  fontSize: 40, fontFace: FONTS.header,
  color: COLORS.text, bold: true
});
titleSlide.addText("サブタイトル — 概要テキスト", {
  x: 0.8, y: 3.2, w: 8.5, h: 0.8,
  fontSize: 20, fontFace: FONTS.body,
  color: COLORS.secondary
});
```

**↑ この品質が最低ライン。白背景に黒テキストだけは論外。**

---

## プロジェクト設定

When greeting the user at the start of a conversation, display this banner:

```
 ██▀▀█  ██▀▀█  ▀▀██▀▀  ▀▄  ▄▀
 ██▄▄▀  ██▄▄▀    ██      ▀██▀
 ██     ██       ██     ▄▀▀▀▄
 ▀▀     ▀▀       ▀▀    ▀▀   ▀▀

 █▌  ▐█  ██  ██▀▀▄  ██▀▀▀
  █▌▐█   ██  ██▀▀█  ██▀▀
   ▀▀    ██  ██▄▄▀  ██▄▄▄

 ═══ Presentation AI Studio ═══
```

After the banner, show a brief status line:
- Output directory: `C:\ai\pptx\output\`
- Available: Create / Edit / Analyze / Theme

### Output Directory (MANDATORY)
- **ALL generated .pptx files MUST be saved to `C:\ai\pptx\output\`**
- NEVER save .pptx files to the project root directory
- Create the output directory if it doesn't exist

### Quality
- スライド生成後、必ずVisual QAを実施する
- `python -m markitdown output.pptx` でコンテンツを確認する
- 画像変換して目視チェックする（`soffice` + `pdftoppm`）
