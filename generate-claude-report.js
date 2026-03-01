const globalModules = require("path").join(process.env.APPDATA || "", "npm/node_modules");
const pptxgen = require(require("path").join(globalModules, "pptxgenjs"));
const React = require(require("path").join(globalModules, "react-icons/node_modules/react"));
const ReactDOMServer = require(require("path").join(globalModules, "react-dom/server"));
const sharp = require(require("path").join(globalModules, "sharp"));
const {
  FaRobot, FaBrain, FaCode, FaShieldAlt, FaRocket, FaDollarSign,
  FaUsers, FaLaptopCode, FaChartLine, FaLock, FaEye, FaCog,
  FaDesktop, FaComments, FaDatabase, FaClipboardList, FaHistory,
  FaArrowRight, FaCheckCircle, FaLayerGroup
} = require(require("path").join(globalModules, "react-icons/fa"));

// ─── Icon Renderer ───
function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}
async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// ─── Design Tokens ───
const C = {
  dark:    "0F0F1A",
  primary: "D4956A",   // warm copper
  accent:  "E8B36B",   // golden
  light:   "F7F2ED",   // warm cream
  card:    "FFFFFF",
  text:    "1A1A2E",
  muted:   "6B7280",
  white:   "FFFFFF",
  green:   "10B981",
  blue:    "3B82F6",
  purple:  "8B5CF6",
  rose:    "F43F5E",
  teal:    "14B8A6",
  sky:     "0EA5E9",
  lightMuted: "9CA3AF", // lighter muted for dark bg readability
};
const FONT_H = "Trebuchet MS";
const FONT_B = "Calibri";

const makeShadow = () => ({
  type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.12
});

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "PPTX VIBE";
  pres.title = "2026年 Claude 現状機能レポート";

  // ─── Pre-render icons ───
  const icons = {};
  const iconMap = {
    robot: [FaRobot, C.white],
    brain: [FaBrain, C.white],
    code: [FaCode, C.white],
    shield: [FaShieldAlt, C.white],
    rocket: [FaRocket, C.white],
    dollar: [FaDollarSign, C.white],
    users: [FaUsers, C.white],
    laptop: [FaLaptopCode, C.white],
    chart: [FaChartLine, C.white],
    lock: [FaLock, C.white],
    eye: [FaEye, C.white],
    cog: [FaCog, C.white],
    desktop: [FaDesktop, C.white],
    comments: [FaComments, C.white],
    database: [FaDatabase, C.white],
    clipboard: [FaClipboardList, C.white],
    history: [FaHistory, C.white],
    arrow: [FaArrowRight, C.primary],
    check: [FaCheckCircle, C.green],
    layer: [FaLayerGroup, C.white],
    robotD: [FaRobot, C.primary],
    brainD: [FaBrain, C.accent],
    rocketD: [FaRocket, C.accent],
    codeD: [FaCode, C.primary],
    shieldD: [FaShieldAlt, C.accent],
  };
  for (const [key, [Comp, color]] of Object.entries(iconMap)) {
    icons[key] = await iconToBase64Png(Comp, "#" + color);
  }

  // ================================================================
  // SLIDE 1: TITLE
  // ================================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.dark };

    // Decorative top bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.primary }
    });

    // Decorative circles (pushed further right to avoid content)
    slide.addShape(pres.shapes.OVAL, {
      x: 7.8, y: 0.8, w: 3.0, h: 3.0,
      fill: { color: C.primary, transparency: 92 },
      line: { color: C.primary, width: 1.5, transparency: 60 }
    });
    slide.addShape(pres.shapes.OVAL, {
      x: 8.3, y: 1.3, w: 2.0, h: 2.0,
      fill: { color: C.accent, transparency: 93 },
      line: { color: C.accent, width: 1, transparency: 70 }
    });

    // Icon + Title tighter together
    slide.addImage({ data: icons.brainD, x: 0.7, y: 1.3, w: 0.65, h: 0.65 });

    slide.addText("2026年\nClaude 現状機能レポート", {
      x: 0.7, y: 2.05, w: 7, h: 1.8,
      fontFace: FONT_H, fontSize: 40, bold: true,
      color: C.white, lineSpacingMultiple: 1.15, margin: 0
    });

    // Subtitle - brighter color for contrast
    slide.addText("Anthropic Claude の最新モデル・機能・エコシステム総覧", {
      x: 0.7, y: 3.9, w: 7, h: 0.45,
      fontFace: FONT_B, fontSize: 16, color: C.accent, margin: 0
    });

    // Date - lighter for readability
    slide.addText("February 2026", {
      x: 0.7, y: 4.4, w: 3, h: 0.35,
      fontFace: FONT_B, fontSize: 12, color: C.lightMuted, margin: 0
    });

    // Bottom bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 5.425, w: 10, h: 0.2, fill: { color: C.primary }
    });
  }

  // ================================================================
  // SLIDE 2: AGENDA
  // ================================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.light };

    slide.addText("CONTENTS", {
      x: 0.7, y: 0.45, w: 3, h: 0.3,
      fontFace: FONT_B, fontSize: 11, color: C.primary,
      bold: true, charSpacing: 4, margin: 0
    });
    slide.addText("目次", {
      x: 0.7, y: 0.8, w: 5, h: 0.55,
      fontFace: FONT_H, fontSize: 32, bold: true, color: C.text, margin: 0
    });

    const items = [
      { num: "01", label: "モデルラインナップ", desc: "Opus 4.6 / Sonnet 4.6 / Haiku 4.5", icon: icons.layer },
      { num: "02", label: "進化のタイムライン", desc: "Claude 1 から 4.6 への歩み", icon: icons.history },
      { num: "03", label: "主要プロダクト", desc: "Claude Code / Cowork / Agent Teams", icon: icons.laptop },
      { num: "04", label: "API料金体系", desc: "トークン単価と最適化", icon: icons.dollar },
      { num: "05", label: "安全性とガバナンス", desc: "2026 Constitution / プロンプト注入耐性", icon: icons.shield },
      { num: "06", label: "今後の展望", desc: "Claude 5 と次世代AIの方向性", icon: icons.rocket },
    ];

    items.forEach((item, i) => {
      const yBase = 1.6 + i * 0.6;
      // Icon circle
      slide.addShape(pres.shapes.OVAL, {
        x: 0.7, y: yBase, w: 0.42, h: 0.42,
        fill: { color: C.primary }
      });
      slide.addImage({ data: item.icon, x: 0.78, y: yBase + 0.06, w: 0.26, h: 0.26 });

      // Number
      slide.addText(item.num, {
        x: 1.3, y: yBase - 0.02, w: 0.4, h: 0.3,
        fontFace: FONT_H, fontSize: 14, bold: true, color: C.primary, margin: 0
      });
      slide.addText(item.label, {
        x: 1.7, y: yBase - 0.02, w: 3.5, h: 0.3,
        fontFace: FONT_H, fontSize: 15, bold: true, color: C.text, margin: 0
      });
      slide.addText(item.desc, {
        x: 1.7, y: yBase + 0.26, w: 4.5, h: 0.22,
        fontFace: FONT_B, fontSize: 10, color: C.muted, margin: 0
      });
    });

    // Right side decoration - vertically centered
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 7.2, y: 1.4, w: 2.3, h: 3.5,
      fill: { color: C.dark }, shadow: makeShadow()
    });
    slide.addImage({ data: icons.robotD, x: 7.85, y: 2.4, w: 1.0, h: 1.0 });
    slide.addText("Claude", {
      x: 7.2, y: 3.5, w: 2.3, h: 0.4,
      fontFace: FONT_H, fontSize: 18, bold: true, color: C.primary, align: "center", margin: 0
    });
    slide.addText("by Anthropic", {
      x: 7.2, y: 3.85, w: 2.3, h: 0.3,
      fontFace: FONT_B, fontSize: 11, color: C.lightMuted, align: "center", margin: 0
    });
  }

  // ================================================================
  // SLIDE 3: MODEL LINEUP - 3 cards (tighter, more margin)
  // ================================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.light };

    slide.addText("MODEL LINEUP", {
      x: 0.7, y: 0.45, w: 4, h: 0.3,
      fontFace: FONT_B, fontSize: 11, color: C.primary,
      bold: true, charSpacing: 4, margin: 0
    });
    slide.addText("現行モデルラインナップ", {
      x: 0.7, y: 0.8, w: 8, h: 0.5,
      fontFace: FONT_H, fontSize: 28, bold: true, color: C.text, margin: 0
    });

    const models = [
      {
        name: "Opus 4.6", tier: "FLAGSHIP",
        color: C.primary, tierBg: C.primary,
        stats: [
          { label: "コンテキスト", val: "1M tokens" },
          { label: "入力", val: "$15 / 1M" },
          { label: "出力", val: "$75 / 1M" },
        ],
        features: ["Agent Teams", "最高推論能力", "複雑なタスク"],
      },
      {
        name: "Sonnet 4.6", tier: "BEST VALUE",
        color: C.blue, tierBg: C.blue,
        stats: [
          { label: "コンテキスト", val: "1M tokens" },
          { label: "入力", val: "$3 / 1M" },
          { label: "出力", val: "$15 / 1M" },
        ],
        features: ["コーディング最強", "Opus 4.5超え", "コスパ最良"],
      },
      {
        name: "Haiku 4.5", tier: "SPEED",
        color: C.teal, tierBg: C.teal,
        stats: [
          { label: "コンテキスト", val: "200K tokens" },
          { label: "入力", val: "$1 / 1M" },
          { label: "出力", val: "$5 / 1M" },
        ],
        features: ["最速レスポンス", "低コスト", "軽量タスク"],
      },
    ];

    models.forEach((m, i) => {
      const xBase = 0.6 + i * 3.1;
      const cardW = 2.8;
      const cardY = 1.5;
      const cardH = 3.4;

      // Card bg
      slide.addShape(pres.shapes.RECTANGLE, {
        x: xBase, y: cardY, w: cardW, h: cardH,
        fill: { color: C.card }, shadow: makeShadow()
      });

      // Tier badge
      slide.addShape(pres.shapes.RECTANGLE, {
        x: xBase, y: cardY, w: cardW, h: 0.42,
        fill: { color: m.tierBg }
      });
      slide.addText(m.tier, {
        x: xBase, y: cardY, w: cardW, h: 0.42,
        fontFace: FONT_B, fontSize: 10, bold: true, color: C.white,
        align: "center", valign: "middle", charSpacing: 2, margin: 0
      });

      // Model name
      slide.addText(m.name, {
        x: xBase + 0.25, y: cardY + 0.55, w: cardW - 0.5, h: 0.4,
        fontFace: FONT_H, fontSize: 22, bold: true, color: C.text, margin: 0
      });

      // Stats
      m.stats.forEach((s, si) => {
        const yS = cardY + 1.1 + si * 0.5;
        slide.addText(s.label, {
          x: xBase + 0.25, y: yS, w: cardW - 0.5, h: 0.2,
          fontFace: FONT_B, fontSize: 9, color: C.muted, margin: 0
        });
        slide.addText(s.val, {
          x: xBase + 0.25, y: yS + 0.18, w: cardW - 0.5, h: 0.24,
          fontFace: FONT_H, fontSize: 14, bold: true, color: C.text, margin: 0
        });
      });

      // Divider
      slide.addShape(pres.shapes.LINE, {
        x: xBase + 0.25, y: cardY + 2.65, w: cardW - 0.5, h: 0,
        line: { color: "E5E7EB", width: 1 }
      });

      // Features
      const featureTexts = m.features.map((f, fi) => ({
        text: f,
        options: {
          bullet: true, breakLine: fi < m.features.length - 1,
          fontSize: 12, fontFace: FONT_B, color: C.text,
          paraSpaceAfter: 4
        }
      }));
      slide.addText(featureTexts, {
        x: xBase + 0.25, y: cardY + 2.75, w: cardW - 0.5, h: 0.6, margin: 0
      });
    });
  }

  // ================================================================
  // SLIDE 4: TIMELINE
  // ================================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.light };

    slide.addText("TIMELINE", {
      x: 0.7, y: 0.45, w: 4, h: 0.3,
      fontFace: FONT_B, fontSize: 11, color: C.primary,
      bold: true, charSpacing: 4, margin: 0
    });
    slide.addText("Claude 進化の軌跡", {
      x: 0.7, y: 0.8, w: 8, h: 0.5,
      fontFace: FONT_H, fontSize: 28, bold: true, color: C.text, margin: 0
    });

    // Timeline horizontal line
    const lineY = 2.4;
    slide.addShape(pres.shapes.LINE, {
      x: 0.8, y: lineY, w: 8.4, h: 0,
      line: { color: C.primary, width: 2 }
    });

    const events = [
      { year: "2023", items: ["Claude 1 登場", "Claude 2 一般公開", "200Kコンテキスト"], color: C.muted },
      { year: "2024", items: ["Claude 3 三兄弟", "3.5 Sonnet 衝撃", "Computer Use"], color: C.purple },
      { year: "2025", items: ["Claude 4 発表", "Sonnet 4.5 SWE最高", "Opus 4.5 67%値下げ"], color: C.blue },
      { year: "2026", items: ["Opus 4.6 Agent Teams", "Sonnet 4.6 最強コスパ", "Claude 5 予告"], color: C.primary },
    ];

    events.forEach((ev, i) => {
      const xPos = 1.15 + i * 2.15;

      // Dot on timeline
      slide.addShape(pres.shapes.OVAL, {
        x: xPos + 0.3, y: lineY - 0.1, w: 0.2, h: 0.2,
        fill: { color: ev.color }
      });

      // Year label above
      slide.addText(ev.year, {
        x: xPos - 0.1, y: lineY - 0.6, w: 1.0, h: 0.35,
        fontFace: FONT_H, fontSize: 18, bold: true, color: ev.color,
        align: "center", margin: 0
      });

      // Items below
      const itemTexts = ev.items.map((item, ii) => ({
        text: item,
        options: {
          bullet: true, breakLine: ii < ev.items.length - 1,
          fontSize: 10, fontFace: FONT_B, color: C.text,
          paraSpaceAfter: 3
        }
      }));
      slide.addText(itemTexts, {
        x: xPos - 0.15, y: lineY + 0.25, w: 1.9, h: 1.2, margin: 0
      });
    });

    // Bottom stat callouts - moved up for margin
    const calloutY = 4.15;
    const callouts = [
      { val: "3年", label: "開発期間", color: C.primary },
      { val: "12+", label: "リリースモデル数", color: C.blue },
      { val: "1M", label: "最大コンテキスト", color: C.teal },
      { val: "67%", label: "コスト削減", color: C.green },
    ];
    callouts.forEach((c, i) => {
      const xC = 0.6 + i * 2.3;
      slide.addShape(pres.shapes.RECTANGLE, {
        x: xC, y: calloutY, w: 2.05, h: 0.85,
        fill: { color: C.card }, shadow: makeShadow()
      });
      slide.addShape(pres.shapes.RECTANGLE, {
        x: xC, y: calloutY, w: 0.06, h: 0.85,
        fill: { color: c.color }
      });
      slide.addText(c.val, {
        x: xC + 0.2, y: calloutY + 0.08, w: 1.6, h: 0.38,
        fontFace: FONT_H, fontSize: 22, bold: true, color: c.color, margin: 0
      });
      slide.addText(c.label, {
        x: xC + 0.2, y: calloutY + 0.48, w: 1.6, h: 0.25,
        fontFace: FONT_B, fontSize: 10, color: C.muted, margin: 0
      });
    });
  }

  // ================================================================
  // SLIDE 5: KEY PRODUCTS - 2x2 grid (uniform spacing)
  // ================================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.light };

    slide.addText("KEY PRODUCTS", {
      x: 0.7, y: 0.45, w: 4, h: 0.3,
      fontFace: FONT_B, fontSize: 11, color: C.primary,
      bold: true, charSpacing: 4, margin: 0
    });
    slide.addText("主要プロダクトと機能", {
      x: 0.7, y: 0.8, w: 8, h: 0.5,
      fontFace: FONT_H, fontSize: 28, bold: true, color: C.text, margin: 0
    });

    const products = [
      {
        name: "Claude Code",
        desc: "AIコーディングアシスタントのCLIツール。並列エージェント、チェックポイント、IDE連携でコードの90%以上をAIが記述。",
        icon: icons.code, color: C.blue,
      },
      {
        name: "Claude Cowork",
        desc: "非エンジニア向けGUIエージェント。ローカルVM上で動作し、ファイル操作やMCP連携で知識ワークを自動化。",
        icon: icons.desktop, color: C.purple,
      },
      {
        name: "Agent Teams",
        desc: "Opus 4.6の中核機能。複数エージェントがタスクを分担し並行処理。Cコンパイラの自動構築に成功。",
        icon: icons.users, color: C.primary,
      },
      {
        name: "Claude Code Security",
        desc: "コードベース全体の脆弱性を自動検出。Anthropic社内でも使用される防御的セキュリティレビュー。",
        icon: icons.shield, color: C.teal,
      },
    ];

    const gridGap = 0.3;
    const cardW = 4.25;
    const cardH = 1.65;

    products.forEach((p, i) => {
      const col = i % 2;
      const row = Math.floor(i / 2);
      const xBase = 0.6 + col * (cardW + gridGap);
      const yBase = 1.5 + row * (cardH + gridGap);

      // Card
      slide.addShape(pres.shapes.RECTANGLE, {
        x: xBase, y: yBase, w: cardW, h: cardH,
        fill: { color: C.card }, shadow: makeShadow()
      });

      // Icon circle
      slide.addShape(pres.shapes.OVAL, {
        x: xBase + 0.2, y: yBase + 0.2, w: 0.5, h: 0.5,
        fill: { color: p.color }
      });
      slide.addImage({ data: p.icon, x: xBase + 0.29, y: yBase + 0.29, w: 0.32, h: 0.32 });

      // Name
      slide.addText(p.name, {
        x: xBase + 0.9, y: yBase + 0.2, w: cardW - 1.15, h: 0.38,
        fontFace: FONT_H, fontSize: 16, bold: true, color: C.text, margin: 0
      });

      // Desc
      slide.addText(p.desc, {
        x: xBase + 0.2, y: yBase + 0.82, w: cardW - 0.4, h: 0.7,
        fontFace: FONT_B, fontSize: 11, color: C.muted, margin: 0
      });
    });
  }

  // ================================================================
  // SLIDE 6: PRICING - Bar chart + stats
  // ================================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.light };

    slide.addText("API PRICING", {
      x: 0.7, y: 0.45, w: 4, h: 0.3,
      fontFace: FONT_B, fontSize: 11, color: C.primary,
      bold: true, charSpacing: 4, margin: 0
    });
    slide.addText("API料金体系（per 1M tokens）", {
      x: 0.7, y: 0.8, w: 8, h: 0.5,
      fontFace: FONT_H, fontSize: 28, bold: true, color: C.text, margin: 0
    });

    // Chart
    slide.addChart(pres.charts.BAR, [
      {
        name: "入力 ($/1M)",
        labels: ["Opus 4.6", "Opus 4.5", "Sonnet 4.6", "Sonnet 4.5", "Haiku 4.5"],
        values: [15, 5, 3, 3, 1],
      },
      {
        name: "出力 ($/1M)",
        labels: ["Opus 4.6", "Opus 4.5", "Sonnet 4.6", "Sonnet 4.5", "Haiku 4.5"],
        values: [75, 25, 15, 15, 5],
      },
    ], {
      x: 0.5, y: 1.45, w: 5.3, h: 3.5,
      barDir: "col",
      chartColors: [C.primary, C.blue],
      chartArea: { fill: { color: C.card }, roundedCorners: true },
      catAxisLabelColor: C.text,
      catAxisLabelFontSize: 10,
      valAxisLabelColor: C.muted,
      valAxisLabelFontSize: 10,
      valGridLine: { color: "E2E8F0", size: 0.5 },
      catGridLine: { style: "none" },
      showValue: true,
      dataLabelPosition: "outEnd",
      dataLabelColor: C.text,
      dataLabelFontSize: 9,
      showLegend: true,
      legendPos: "b",
      legendFontSize: 10,
    });

    // Right side - cost optimization tips (with more gap from chart)
    const tipsX = 6.15;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: tipsX, y: 1.45, w: 3.35, h: 3.5,
      fill: { color: C.dark }, shadow: makeShadow()
    });
    slide.addText("コスト最適化", {
      x: tipsX + 0.3, y: 1.65, w: 2.75, h: 0.4,
      fontFace: FONT_H, fontSize: 16, bold: true, color: C.white, margin: 0
    });

    const tips = [
      { val: "-90%", label: "プロンプトキャッシュ" },
      { val: "-50%", label: "Batch API" },
      { val: "-60%", label: "70/20/10 モデル混合" },
      { val: "無制限", label: "Infinite Chats" },
    ];
    tips.forEach((t, i) => {
      const yT = 2.25 + i * 0.68;
      slide.addText(t.val, {
        x: tipsX + 0.3, y: yT, w: 2.75, h: 0.3,
        fontFace: FONT_H, fontSize: 20, bold: true, color: C.accent, margin: 0
      });
      slide.addText(t.label, {
        x: tipsX + 0.3, y: yT + 0.3, w: 2.75, h: 0.22,
        fontFace: FONT_B, fontSize: 11, color: C.lightMuted, margin: 0
      });
    });
  }

  // ================================================================
  // SLIDE 7: SAFETY & GOVERNANCE (tighter cards)
  // ================================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.light };

    slide.addText("SAFETY & GOVERNANCE", {
      x: 0.7, y: 0.45, w: 5, h: 0.3,
      fontFace: FONT_B, fontSize: 11, color: C.primary,
      bold: true, charSpacing: 4, margin: 0
    });
    slide.addText("安全性とガバナンス", {
      x: 0.7, y: 0.8, w: 8, h: 0.5,
      fontFace: FONT_H, fontSize: 28, bold: true, color: C.text, margin: 0
    });

    const cardTop = 1.5;
    const cardH = 3.3;

    // Left column - 2026 Constitution
    const leftX = 0.6;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: leftX, y: cardTop, w: 4.25, h: cardH,
      fill: { color: C.card }, shadow: makeShadow()
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: leftX, y: cardTop, w: 4.25, h: 0.45,
      fill: { color: C.primary }
    });
    slide.addText("2026 Constitution", {
      x: leftX + 0.25, y: cardTop, w: 3.75, h: 0.45,
      fontFace: FONT_H, fontSize: 14, bold: true, color: C.white,
      valign: "middle", margin: 0
    });
    const constItems = [
      "ガイドライン根拠の明示化",
      "民主主義保護の原則を強化",
      "Constitution違反をほぼゼロにする目標",
      "訓練手法と誘導手法の多層的組合せ",
      "透明性レポートの定期公開",
    ];
    const constTexts = constItems.map((c, ci) => ({
      text: c,
      options: {
        bullet: true, breakLine: ci < constItems.length - 1,
        fontSize: 12, fontFace: FONT_B, color: C.text,
        paraSpaceAfter: 8
      }
    }));
    slide.addText(constTexts, {
      x: leftX + 0.25, y: cardTop + 0.6, w: 3.75, h: 2.5,
      valign: "top", margin: 0
    });

    // Right column - Security improvements
    const rightX = 5.15;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: rightX, y: cardTop, w: 4.25, h: cardH,
      fill: { color: C.card }, shadow: makeShadow()
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: rightX, y: cardTop, w: 4.25, h: 0.45,
      fill: { color: C.teal }
    });
    slide.addText("セキュリティ強化", {
      x: rightX + 0.25, y: cardTop, w: 3.75, h: 0.45,
      fontFace: FONT_H, fontSize: 14, bold: true, color: C.white,
      valign: "middle", margin: 0
    });
    const secItems = [
      "プロンプト注入耐性の大幅向上（4.6）",
      "Claude Code Securityで脆弱性検出",
      "コードベース全体の自動レビュー",
      "Anthropic社内での自社コード防御に活用",
      "エンタープライズ向けガバナンス機能",
    ];
    const secTexts = secItems.map((s, si) => ({
      text: s,
      options: {
        bullet: true, breakLine: si < secItems.length - 1,
        fontSize: 12, fontFace: FONT_B, color: C.text,
        paraSpaceAfter: 8
      }
    }));
    slide.addText(secTexts, {
      x: rightX + 0.25, y: cardTop + 0.6, w: 3.75, h: 2.5,
      valign: "top", margin: 0
    });
  }

  // ================================================================
  // SLIDE 8: OUTLOOK - Dark closing slide (no overlapping decor)
  // ================================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.dark };

    // Top bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.primary }
    });

    slide.addText("OUTLOOK", {
      x: 0.7, y: 0.45, w: 4, h: 0.3,
      fontFace: FONT_B, fontSize: 11, color: C.primary,
      bold: true, charSpacing: 4, margin: 0
    });
    slide.addText("今後の展望", {
      x: 0.7, y: 0.8, w: 8, h: 0.5,
      fontFace: FONT_H, fontSize: 28, bold: true, color: C.white, margin: 0
    });

    // Claude 5 callout - solid card
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y: 1.55, w: 4.2, h: 2.2,
      fill: { color: "1A1A30" },
      line: { color: C.primary, width: 1.5 }
    });
    slide.addText("Claude 5", {
      x: 0.85, y: 1.7, w: 3.7, h: 0.5,
      fontFace: FONT_H, fontSize: 30, bold: true, color: C.accent, margin: 0
    });
    slide.addText([
      { text: "2026年 Q2〜Q3 リリース予定", options: { breakLine: true, fontSize: 13, color: C.white } },
      { text: "コードネーム「Fennec」（Sonnet 5）", options: { breakLine: true, fontSize: 13, color: C.white } },
      { text: "Vertex AI エラーログで確認済み", options: { fontSize: 13, color: C.lightMuted } },
    ], {
      x: 0.85, y: 2.3, w: 3.7, h: 1.2,
      fontFace: FONT_B, lineSpacingMultiple: 1.5, margin: 0
    });

    // Key stats for future - evenly spaced
    const futureStats = [
      { val: "50%", label: "米国の全職種がClaude利用", color: C.accent },
      { val: "90%+", label: "AIによるコード記述率", color: C.blue },
      { val: "AGI級", label: "推論能力の目標水準", color: C.green },
    ];
    futureStats.forEach((f, i) => {
      const yF = 1.55 + i * 0.85;
      slide.addText(f.val, {
        x: 5.5, y: yF, w: 4, h: 0.45,
        fontFace: FONT_H, fontSize: 34, bold: true, color: f.color, margin: 0
      });
      slide.addText(f.label, {
        x: 5.5, y: yF + 0.42, w: 4, h: 0.28,
        fontFace: FONT_B, fontSize: 12, color: C.lightMuted, margin: 0
      });
    });

    // Bottom bar with source
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 4.95, w: 10, h: 0.68, fill: { color: C.primary }
    });
    slide.addText("Source: Anthropic, CNBC, TechCrunch, VentureBeat  |  February 2026", {
      x: 0.7, y: 5.0, w: 8.6, h: 0.55,
      fontFace: FONT_B, fontSize: 11, color: C.white, align: "center", valign: "middle", margin: 0
    });
  }

  // ─── Save ───
  const outPath = "C:/ai/pptx/output/claude_2026_report.pptx";
  await pres.writeFile({ fileName: outPath });
  console.log("Saved: " + outPath);
}

main().catch(console.error);
