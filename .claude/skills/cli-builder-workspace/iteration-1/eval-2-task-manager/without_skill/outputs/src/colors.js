// ============================================================
// colors.js - ANSI color utilities (zero dependencies)
// ============================================================

const ESC = '\x1b[';
const RESET = `${ESC}0m`;

const codes = {
  // Styles
  bold:       [1, 22],
  dim:        [2, 22],
  italic:     [3, 23],
  underline:  [4, 24],
  blink:      [5, 25],
  inverse:    [7, 27],
  strikethrough: [9, 29],

  // Foreground colors
  black:      [30, 39],
  red:        [31, 39],
  green:      [32, 39],
  yellow:     [33, 39],
  blue:       [34, 39],
  magenta:    [35, 39],
  cyan:       [36, 39],
  white:      [37, 39],
  gray:       [90, 39],

  // Bright foreground
  brightRed:     [91, 39],
  brightGreen:   [92, 39],
  brightYellow:  [93, 39],
  brightBlue:    [94, 39],
  brightMagenta: [95, 39],
  brightCyan:    [96, 39],
  brightWhite:   [97, 39],

  // Background colors
  bgBlack:    [40, 49],
  bgRed:      [41, 49],
  bgGreen:    [42, 49],
  bgYellow:   [43, 49],
  bgBlue:     [44, 49],
  bgMagenta:  [45, 49],
  bgCyan:     [46, 49],
  bgWhite:    [47, 49],
};

const c = {};

for (const [name, [open, close]] of Object.entries(codes)) {
  c[name] = (text) => `${ESC}${open}m${text}${ESC}${close}m`;
}

// Composite helpers
c.success = (text) => c.bold(c.green(text));
c.error   = (text) => c.bold(c.red(text));
c.warn    = (text) => c.bold(c.yellow(text));
c.info    = (text) => c.bold(c.cyan(text));
c.muted   = (text) => c.dim(c.gray(text));
c.accent  = (text) => c.bold(c.magenta(text));
c.highlight = (text) => c.bold(c.brightWhite(text));

// 256-color support
c.fg256 = (code, text) => `${ESC}38;5;${code}m${text}${RESET}`;
c.bg256 = (code, text) => `${ESC}48;5;${code}m${text}${RESET}`;

// RGB support
c.rgb = (r, g, b, text) => `${ESC}38;2;${r};${g};${b}m${text}${RESET}`;
c.bgRgb = (r, g, b, text) => `${ESC}48;2;${r};${g};${b}m${text}${RESET}`;

// Strip ANSI codes (for length calculations)
c.strip = (text) => text.replace(/\x1b\[[0-9;]*m/g, '');

module.exports = c;
