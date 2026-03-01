#!/usr/bin/env python3
"""Grade all eval runs by checking assertions against output files."""

import json
import os
import re
from pathlib import Path

WORKSPACE = Path(__file__).parent

EVALS = [
    {
        "eval_dir": "eval-0-nodejs-csv-converter",
        "assertions": [
            ("has-banner-module", r"figlet|banner", "figletでバナー表示がある"),
            ("has-color-theme", r"chalk|theme|color.*=.*chalk", "カラーテーマが定義されている"),
            ("has-commander-setup", r"commander|Command\(|yargs", "commanderでコマンドルーティング"),
            ("has-progress-indicator", r"ora|spinner|progress|cli-progress", "プログレス表示がある"),
            ("has-output-option", r"--output|output.*option|'-o'|\"--output\"", "--outputオプション定義"),
            ("separation-of-concerns", None, "UI/ビジネスロジック分離（ディレクトリ構造）"),
        ],
    },
    {
        "eval_dir": "eval-1-python-project-setup",
        "assertions": [
            ("has-banner-module", r"pyfiglet|figlet_format|BANNER|banner", "pyfigletバナー表示"),
            ("has-rich-output", r"rich|Console|rich\.console", "richライブラリ使用"),
            ("has-typer-or-click", r"typer|click", "typerまたはclick使用"),
            ("has-interactive-prompts", r"questionary|Prompt\.ask|prompt|select|input", "対話プロンプト"),
            ("has-progress-bar", r"progress|track|status|spinner|Progress", "プログレスバー/スピナー"),
            ("has-template-choices", r"minimal|standard|full", "テンプレート選択肢"),
        ],
    },
    {
        "eval_dir": "eval-2-task-manager",
        "assertions": [
            ("has-banner", r"figlet|pyfiglet|BANNER|banner|ASCII", "ASCIIバナー表示"),
            ("has-add-command", r"['\"]add['\"]|command.*add|\.command\(['\"]add", "addコマンド実装"),
            ("has-list-command", r"['\"]list['\"]|command.*list|\.command\(['\"]list", "listコマンド実装"),
            ("has-done-command", r"['\"]done['\"]|command.*done|\.command\(['\"]done|complete", "doneコマンド実装"),
            ("has-json-storage", r"\.json|JSON\.parse|JSON\.stringify|json\.load|json\.dump|readFile|writeFile", "JSONストレージ"),
            ("has-styled-output", r"chalk|rich|color|style|theme|ansi", "スタイル付き出力"),
        ],
    },
]


def collect_all_content(directory: Path) -> str:
    """Read all text files in directory tree into one string."""
    content = ""
    if not directory.exists():
        return content
    for root, dirs, files in os.walk(directory):
        # Skip node_modules
        dirs[:] = [d for d in dirs if d != "node_modules"]
        for f in files:
            fpath = Path(root) / f
            if fpath.suffix in (".ts", ".js", ".py", ".json", ".toml", ".md", ".txt", ".cfg"):
                try:
                    content += f"\n--- {fpath.relative_to(directory)} ---\n"
                    content += fpath.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    pass
    return content


def check_directory_separation(directory: Path) -> bool:
    """Check if the project has separate directories for UI and logic."""
    has_ui = False
    has_logic = False
    for root, dirs, files in os.walk(directory):
        rel = Path(root).relative_to(directory).as_posix().lower()
        if "ui" in rel or "banner" in rel:
            has_ui = True
        if "lib" in rel or "service" in rel or "core" in rel or "commands" in rel:
            has_logic = True
    return has_ui and has_logic


def grade_run(eval_info: dict, variant: str) -> dict:
    """Grade a single run (with_skill or without_skill)."""
    eval_dir = WORKSPACE / eval_info["eval_dir"] / variant
    outputs_dir = eval_dir / "outputs"

    # Find the actual project root (might be nested)
    if not outputs_dir.exists():
        return {"variant": variant, "expectations": [], "pass_rate": 0}

    content = collect_all_content(outputs_dir)
    results = []

    for name, pattern, description in eval_info["assertions"]:
        if name == "separation-of-concerns":
            passed = check_directory_separation(outputs_dir)
            evidence = "Found ui/ + lib/commands/ directories" if passed else "No directory separation found"
        elif pattern:
            matches = re.findall(pattern, content, re.IGNORECASE)
            passed = len(matches) > 0
            evidence = f"Found {len(matches)} matches" if passed else "No matches found"
        else:
            passed = False
            evidence = "No pattern defined"

        results.append({
            "text": description,
            "passed": passed,
            "evidence": evidence,
        })

    pass_count = sum(1 for r in results if r["passed"])
    pass_rate = pass_count / len(results) if results else 0

    return {
        "variant": variant,
        "expectations": results,
        "pass_rate": round(pass_rate, 3),
        "pass_count": pass_count,
        "total": len(results),
    }


def main():
    all_results = {}

    for eval_info in EVALS:
        eval_name = eval_info["eval_dir"]
        print(f"\n{'='*60}")
        print(f"  Grading: {eval_name}")
        print(f"{'='*60}")

        for variant in ["with_skill", "without_skill"]:
            result = grade_run(eval_info, variant)
            key = f"{eval_name}/{variant}"
            all_results[key] = result

            # Save grading.json
            grading_path = WORKSPACE / eval_name / variant / "grading.json"
            grading_path.parent.mkdir(parents=True, exist_ok=True)
            with open(grading_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            status = "PASS" if result["pass_rate"] == 1.0 else "PARTIAL" if result["pass_rate"] > 0 else "FAIL"
            print(f"\n  [{variant}] {status} ({result['pass_count']}/{result['total']})")
            for exp in result["expectations"]:
                icon = "+" if exp["passed"] else "-"
                print(f"    [{icon}] {exp['text']}: {exp['evidence']}")

    # Summary
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")

    for key, result in all_results.items():
        rate_pct = int(result["pass_rate"] * 100)
        print(f"  {key}: {result['pass_count']}/{result['total']} ({rate_pct}%)")

    # Save aggregate
    with open(WORKSPACE / "grading_summary.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n  Results saved to grading_summary.json")


if __name__ == "__main__":
    main()
