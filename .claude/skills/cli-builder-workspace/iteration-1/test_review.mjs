import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const WORKSPACE = 'C:/ai/pptx/.claude/skills/cli-builder-workspace/iteration-1';
const REVIEW_HTML = path.join(WORKSPACE, 'review.html');
const SCREENSHOT_DIR = path.join(WORKSPACE, 'screenshots');

fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });

  const url = `file:///${REVIEW_HTML.replace(/\\/g, '/')}`;
  await page.goto(url);
  await page.waitForLoadState('networkidle');

  // 1. Initial view
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '01_initial_view.png') });
  console.log('[1] Initial view captured');

  // 2. Navigate through test cases with arrow keys
  for (let i = 0; i < 5; i++) {
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, `02_case_${i + 1}.png`) });
    console.log(`[${i + 2}] Test case ${i + 1} captured`);
  }

  // 3. Try to switch to Benchmark tab
  const tabs = await page.locator('button, [role="tab"], a').all();
  for (const tab of tabs) {
    const text = await tab.textContent().catch(() => '');
    if (text && text.toLowerCase().includes('benchmark')) {
      await tab.click();
      await page.waitForTimeout(500);
      break;
    }
  }
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '07_benchmark.png'), fullPage: true });
  console.log('[7] Benchmark tab captured');

  // 4. Full page screenshot
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '08_full_page.png'), fullPage: true });
  console.log('[8] Full page captured');

  await browser.close();
  console.log(`\nAll screenshots saved to: ${SCREENSHOT_DIR}`);
}

main().catch(console.error);
