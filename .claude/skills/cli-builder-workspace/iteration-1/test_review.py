"""Playwright test: screenshot review page and examine generated CLI code outputs."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

WORKSPACE = Path(r"C:\ai\pptx\.claude\skills\cli-builder-workspace\iteration-1")
REVIEW_HTML = WORKSPACE / "review.html"
SCREENSHOT_DIR = WORKSPACE / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)


def test_review_page():
    """Take screenshots of the review viewer."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        url = REVIEW_HTML.as_uri()
        page.goto(url)
        page.wait_for_load_state("networkidle")

        # Initial view
        page.screenshot(path=str(SCREENSHOT_DIR / "01_review_initial.png"))
        print("[1] Review initial view")

        # Navigate through cases
        for i in range(5):
            page.keyboard.press("ArrowRight")
            page.wait_for_timeout(400)
            page.screenshot(path=str(SCREENSHOT_DIR / f"02_review_case_{i+1}.png"))
            print(f"[{i+2}] Review case {i+1}")

        # Benchmark tab
        tabs = page.query_selector_all("button, [role='tab'], a, div[class*='tab']")
        for tab in tabs:
            text = tab.text_content() or ""
            if "benchmark" in text.lower():
                tab.click()
                page.wait_for_timeout(500)
                break
        page.screenshot(path=str(SCREENSHOT_DIR / "07_benchmark.png"), full_page=True)
        print("[7] Benchmark tab")

        browser.close()


def test_eval_outputs():
    """Examine actual generated code files with screenshots of key files."""
    evals = [
        ("eval-0-nodejs-csv-converter", "Node.js CSV Converter"),
        ("eval-1-python-project-setup", "Python Project Setup"),
        ("eval-2-task-manager", "Task Manager"),
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for eval_dir, label in evals:
            for variant in ["with_skill", "without_skill"]:
                output_path = WORKSPACE / eval_dir / variant / "outputs"
                if not output_path.exists():
                    continue

                # Create an HTML page showing file tree and key file contents
                files = sorted(output_path.rglob("*"), key=lambda x: str(x))
                source_files = [
                    f for f in files
                    if f.is_file() and f.suffix in (".ts", ".js", ".py", ".toml", ".json")
                    and "node_modules" not in str(f)
                ]

                html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
body {{ font-family: 'Cascadia Code', 'Fira Code', monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }}
h1 {{ color: #569cd6; font-size: 18px; }}
h2 {{ color: #4ec9b0; font-size: 14px; margin-top: 20px; }}
.tree {{ color: #9cdcfe; font-size: 12px; background: #252526; padding: 10px; border-radius: 4px; }}
pre {{ background: #1e1e2e; padding: 12px; border-radius: 4px; font-size: 11px; overflow-x: auto; border-left: 3px solid #569cd6; }}
.label {{ color: #ce9178; font-size: 12px; }}
</style></head><body>
<h1>{label} — {variant}</h1>
<div class="tree"><strong>File Tree:</strong><br>"""

                # Build file tree
                for f in files:
                    if f.is_file() and "node_modules" not in str(f):
                        rel = f.relative_to(output_path)
                        indent = "  " * (len(rel.parts) - 1)
                        html += f"{indent}📄 {rel}<br>"

                html += "</div>"

                # Show key source files (first 60 lines each)
                shown = 0
                for f in source_files:
                    if shown >= 6:
                        break
                    try:
                        content = f.read_text(encoding="utf-8", errors="replace")
                        lines = content.split("\n")[:60]
                        truncated = "\n".join(lines)
                        if len(content.split("\n")) > 60:
                            truncated += "\n... (truncated)"
                        # Escape HTML
                        truncated = truncated.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                        rel = f.relative_to(output_path)
                        html += f'<h2>{rel}</h2><pre>{truncated}</pre>'
                        shown += 1
                    except Exception:
                        pass

                html += "</body></html>"

                # Render and screenshot
                tmp_html = SCREENSHOT_DIR / f"_tmp_{eval_dir}_{variant}.html"
                tmp_html.write_text(html, encoding="utf-8")

                page = browser.new_page(viewport={"width": 1400, "height": 2000})
                page.goto(tmp_html.as_uri())
                page.wait_for_load_state("networkidle")
                page.screenshot(
                    path=str(SCREENSHOT_DIR / f"{eval_dir}_{variant}.png"),
                    full_page=True,
                )
                page.close()
                tmp_html.unlink()
                print(f"[+] {eval_dir}/{variant} captured")

        browser.close()


if __name__ == "__main__":
    print("=== Testing Review Page ===")
    test_review_page()
    print("\n=== Examining Generated Outputs ===")
    test_eval_outputs()
    print(f"\nAll screenshots: {SCREENSHOT_DIR}")
