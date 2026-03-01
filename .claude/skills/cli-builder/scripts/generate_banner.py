#!/usr/bin/env python3
"""Preview ASCII art fonts for CLI banners.

Usage:
    python generate_banner.py "MY CLI"
    python generate_banner.py "MY CLI" --fonts slant,standard,big
    python generate_banner.py "MY CLI" --all
"""

import sys

try:
    from pyfiglet import Figlet, FigletFont
except ImportError:
    print("pyfiglet not installed. Run: pip install pyfiglet")
    sys.exit(1)


RECOMMENDED_FONTS = [
    "slant",
    "standard",
    "big",
    "small",
    "banner3",
    "cybermedium",
    "digital",
    "doom",
    "epic",
    "larry3d",
    "lean",
    "ogre",
    "rectangles",
    "shadow",
    "speed",
    "starwars",
    "stop",
    "thick",
]


def preview_font(text: str, font: str) -> str | None:
    """Render text in a figlet font, returning None if it fails."""
    try:
        f = Figlet(font=font)
        rendered = f.renderText(text)
        if rendered.strip():
            return rendered
    except Exception:
        pass
    return None


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python generate_banner.py <text> [--fonts font1,font2] [--all]")
        sys.exit(1)

    text = sys.argv[1]
    show_all = "--all" in sys.argv

    if show_all:
        fonts = sorted(FigletFont.getFonts())
    elif "--fonts" in sys.argv:
        idx = sys.argv.index("--fonts")
        if idx + 1 < len(sys.argv):
            fonts = sys.argv[idx + 1].split(",")
        else:
            fonts = RECOMMENDED_FONTS
    else:
        fonts = RECOMMENDED_FONTS

    print(f"\n  Previewing '{text}' in {len(fonts)} fonts:\n")
    print("=" * 60)

    for font in fonts:
        rendered = preview_font(text, font)
        if rendered:
            print(f"\n  Font: {font}")
            print("-" * 40)
            for line in rendered.splitlines():
                print(f"  {line}")
            print()

    print("=" * 60)
    print(f"\n  Total fonts shown: {len(fonts)}")
    print("  Use --all to see all available fonts")
    print()


if __name__ == "__main__":
    main()
