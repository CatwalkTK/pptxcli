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

### Output Directory (MANDATORY)
- **ALL generated .pptx files MUST be saved to `C:\ai\pptx\output\`**
- NEVER save .pptx files to the project root directory
- Create the output directory if it doesn't exist

### Skill Usage (MANDATORY)
- **ALWAYS invoke the `pptx` Skill tool BEFORE writing any PPTX generation code**
- The `pptx` skill provides design templates, layouts, and formatting that are essential for professional output
- **ALWAYS invoke the `theme-factory` Skill tool when applying themes or styling**
- Without these skills, slides will lack proper design and formatting
- Do NOT generate plain python-pptx code without first loading the skill

### Quality
- Run Visual QA after generating slides
