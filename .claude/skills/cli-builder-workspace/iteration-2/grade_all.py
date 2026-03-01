#!/usr/bin/env python3
"""Grade all eval runs with strengthened discriminating assertions."""

import json
import os
import re
from pathlib import Path

WORKSPACE = Path(__file__).parent

EVALS = [
    {
        "eval_dir": "eval-0-nodejs-csv-converter",
        "assertions": [
            ("uses-typescript", r"\.ts$", "TypeScript (.ts) ファイルで実装", "file_ext"),
            ("uses-figlet-library", r"import.*figlet|require.*figlet|from 'figlet'", "figletライブラリ使用", "content"),
            ("uses-chalk-library", r"import.*chalk|require.*chalk|from 'chalk'", "chalkライブラリ使用", "content"),
            ("has-commander-setup", r"import.*commander|from 'commander'|Command\(", "commanderルーティング", "content"),
            ("has-progress-indicator", r"import.*ora|require.*ora|cli-progress|import.*progress", "プログレス表示", "content"),
            ("has-output-option", r"--output|output.*option|'-o'|\"--output\"", "--outputオプション", "content"),
            ("has-4-layer-architecture", None, "ui/ + commands/ + lib/ ディレクトリ分離", "structure"),
            ("has-theme-file", r"theme\.", "theme.ts テーマファイル", "file_name"),
            ("has-banner-file", r"banner\.", "banner.ts バナーモジュール", "file_name"),
        ],
    },
    {
        "eval_dir": "eval-1-python-project-setup",
        "assertions": [
            ("uses-typer", r"import typer|from typer", "typer（推奨）使用", "content"),
            ("uses-pyfiglet", r"import pyfiglet|from pyfiglet|figlet_format", "pyfigletバナー生成", "content"),
            ("uses-rich", r"from rich|import rich", "richライブラリ使用", "content"),
            ("uses-questionary", r"import questionary|from questionary", "questionary対話プロンプト", "content"),
            ("has-progress-bar", r"rich\.progress|track\(|Status\(|Progress\(|progress", "プログレスバー/スピナー", "content"),
            ("has-template-choices", r"minimal.*standard.*full|\"minimal\"|'minimal'", "テンプレート選択肢", "content"),
            ("has-4-layer-architecture", None, "ui/ + commands/ + lib/ 分離", "structure"),
            ("has-pyproject-toml", r"pyproject\.toml", "pyproject.toml設定", "file_name"),
            ("has-theme-file", r"theme\.", "theme.py テーマファイル", "file_name"),
        ],
    },
    {
        "eval_dir": "eval-2-task-manager",
        "assertions": [
            ("uses-figlet-or-pyfiglet", r"import.*figlet|require.*figlet|from pyfiglet|pyfiglet", "figlet/pyfigletバナー", "content"),
            ("uses-established-color-lib", r"import.*chalk|require.*chalk|from 'chalk'|from rich|import rich", "chalk/rich使用", "content"),
            ("has-add-command", r"['\"]add['\"]|command.*add|\.command\(['\"]add", "addコマンド", "content"),
            ("has-list-command", r"['\"]list['\"]|command.*list|\.command\(['\"]list", "listコマンド", "content"),
            ("has-done-command", r"['\"]done['\"]|command.*done|\.command\(['\"]done|complete", "doneコマンド", "content"),
            ("has-json-storage", r"\.json|JSON\.parse|JSON\.stringify|json\.load|json\.dump", "JSONストレージ", "content"),
            ("has-4-layer-architecture", None, "ui/ + commands/ + lib/ 分離", "structure"),
            ("has-theme-file", r"theme\.", "theme.ts/theme.py テーマ", "file_name"),
            ("uses-typescript-or-typed", r"\.ts$|import typer", "TypeScript or typer使用", "file_ext_or_content"),
        ],
    },
]


def collect_all_content(directory: Path) -> str:
    content = ""
    if not directory.exists():
        return content
    for root, dirs, files in os.walk(directory):
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


def collect_file_names(directory: Path) -> list[str]:
    names = []
    if not directory.exists():
        return names
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d != "node_modules"]
        for f in files:
            fpath = Path(root) / f
            names.append(fpath.relative_to(directory).as_posix())
    return names


def collect_file_extensions(directory: Path) -> set[str]:
    exts = set()
    if not directory.exists():
        return exts
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d != "node_modules"]
        for f in files:
            exts.add(Path(f).suffix)
    return exts


def check_directory_separation(directory: Path) -> tuple[bool, str]:
    has_ui = False
    has_commands = False
    has_lib = False
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d != "node_modules"]
        rel = Path(root).relative_to(directory).as_posix().lower()
        parts = rel.split("/")
        for part in parts:
            if part in ("ui",):
                has_ui = True
            if part in ("commands", "command"):
                has_commands = True
            if part in ("lib", "core", "service", "services"):
                has_lib = True

    passed = has_ui and has_commands and has_lib
    found = []
    if has_ui: found.append("ui/")
    if has_commands: found.append("commands/")
    if has_lib: found.append("lib/")
    evidence = f"Found: {', '.join(found)}" if found else "No layer directories found"
    return passed, evidence


def grade_run(eval_info: dict, variant: str) -> dict:
    eval_dir = WORKSPACE / eval_info["eval_dir"] / variant
    outputs_dir = eval_dir / "outputs"

    if not outputs_dir.exists():
        return {"variant": variant, "expectations": [], "pass_rate": 0}

    content = collect_all_content(outputs_dir)
    file_names = collect_file_names(outputs_dir)
    file_exts = collect_file_extensions(outputs_dir)
    results = []

    for name, pattern, description, check_type in eval_info["assertions"]:
        passed = False
        evidence = "No matches found"

        if check_type == "content" and pattern:
            matches = re.findall(pattern, content, re.IGNORECASE)
            passed = len(matches) > 0
            evidence = f"Found {len(matches)} matches" if passed else "No matches in source code"

        elif check_type == "file_name" and pattern:
            matching = [f for f in file_names if re.search(pattern, f, re.IGNORECASE)]
            passed = len(matching) > 0
            evidence = f"Found: {', '.join(matching[:3])}" if passed else "No matching files"

        elif check_type == "file_ext" and pattern:
            matching = [f for f in file_names if re.search(pattern, f)]
            passed = len(matching) > 0
            evidence = f"Found {len(matching)} {pattern} files" if passed else f"No {pattern} files found"

        elif check_type == "file_ext_or_content" and pattern:
            # Check both file extension and content
            ts_files = [f for f in file_names if f.endswith(".ts")]
            content_matches = re.findall(pattern, content, re.IGNORECASE)
            passed = len(ts_files) > 0 or len(content_matches) > 0
            evidence_parts = []
            if ts_files:
                evidence_parts.append(f"{len(ts_files)} .ts files")
            if content_matches:
                evidence_parts.append(f"{len(content_matches)} content matches")
            evidence = f"Found: {', '.join(evidence_parts)}" if passed else "No TypeScript files or typer imports"

        elif check_type == "structure":
            passed, evidence = check_directory_separation(outputs_dir)

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

            grading_path = WORKSPACE / eval_name / variant / "grading.json"
            grading_path.parent.mkdir(parents=True, exist_ok=True)
            with open(grading_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            status = "PASS" if result["pass_rate"] == 1.0 else "PARTIAL" if result["pass_rate"] > 0 else "FAIL"
            print(f"\n  [{variant}] {status} ({result['pass_count']}/{result['total']})")
            for exp in result["expectations"]:
                icon = "+" if exp["passed"] else "-"
                print(f"    [{icon}] {exp['text']}: {exp['evidence']}")

    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")

    for key, result in all_results.items():
        rate_pct = int(result["pass_rate"] * 100)
        print(f"  {key}: {result['pass_count']}/{result['total']} ({rate_pct}%)")

    with open(WORKSPACE / "grading_summary.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n  Results saved to grading_summary.json")


if __name__ == "__main__":
    main()
