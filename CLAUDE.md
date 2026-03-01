# PPTX VIBE - Presentation Generator

When greeting the user at the start of a conversation, display this banner:

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

After the banner, show a brief status line:
- Output directory: `C:\ai\pptx\output\`
- Available: Create / Edit / Analyze / Theme

## Project Rules

- Save all generated .pptx files to `C:\ai\pptx\output/`
- Use the `pptx` skill for all PPTX operations
- Use the `theme-factory` skill when applying themes
- Run Visual QA after generating slides
