#!/usr/bin/env python3
"""
2026年AI事情スライドのビルドスクリプト
animations.md の手順: 生成 -> ZIP直接編集でトランジション追加（OOXML構造を維持）
"""
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_PPTX = os.path.join(SCRIPT_DIR, "ai_2026_static.pptx")
OUTPUT_PPTX = os.path.join(SCRIPT_DIR, "2026年のAI事情.pptx")


def main():
    # 1. 静的PPTXを生成（python-pptx）
    subprocess.run(
        [sys.executable, os.path.join(SCRIPT_DIR, "generate_ai_2026.py")],
        check=True,
        cwd=SCRIPT_DIR,
    )

    if not os.path.exists(STATIC_PPTX):
        print("Error: generate_ai_2026.py did not create output")
        sys.exit(1)

    # 2. ZIP直接編集でトランジション追加（アンパック/リパックなし）
    add_transitions = os.path.join(SCRIPT_DIR, "scripts", "add_transitions_inplace.py")
    subprocess.run(
        [sys.executable, add_transitions, STATIC_PPTX, OUTPUT_PPTX],
        check=True,
    )

    # 3. 一時ファイル削除
    os.remove(STATIC_PPTX)

    print(f"\nDone: {OUTPUT_PPTX}")


if __name__ == "__main__":
    main()
