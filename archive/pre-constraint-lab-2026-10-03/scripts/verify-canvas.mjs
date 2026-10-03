import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const url = process.env.SANDBOX_URL || 'http://localhost:5174/';
const shotsDir = new URL('../verification/', import.meta.url);

const viewports = [
  { name: 'desktop', width: 1366, height: 900 },
  { name: 'mobile', width: 390, height: 844 },
];

await mkdir(shotsDir, { recursive: true });

const browser = await chromium.launch({ headless: true });

for (const viewport of viewports) {
  const page = await browser.newPage({ viewport });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForSelector('#scene');
  await page.waitForTimeout(800);

  const result = await page.evaluate(() => {
    const canvas = document.querySelector('#scene');
    const context = canvas.getContext('webgl2') || canvas.getContext('webgl');
    if (!context) {
      return { ok: false, reason: 'No WebGL context' };
    }

    const width = canvas.width;
    const height = canvas.height;
    const pixels = new Uint8Array(width * height * 4);
    context.readPixels(0, 0, width, height, context.RGBA, context.UNSIGNED_BYTE, pixels);

    let active = 0;
    for (let i = 0; i < pixels.length; i += 4) {
      const r = pixels[i];
      const g = pixels[i + 1];
      const b = pixels[i + 2];
      const contrastFromPaper = Math.abs(r - 247) + Math.abs(g - 246) + Math.abs(b - 239);
      if (contrastFromPaper > 55) {
        active += 1;
      }
    }

    const ratio = active / (width * height);
    return { ok: ratio > 0.015, ratio, width, height };
  });

  if (!result.ok) {
    console.error(`${viewport.name} verification failed`, result);
    await browser.close();
    process.exit(1);
  }

  await page.screenshot({ path: fileURLToPath(new URL(`${viewport.name}.png`, shotsDir)), fullPage: true });
  console.log(`${viewport.name}: nonblank ratio ${result.ratio.toFixed(4)} at ${result.width}x${result.height}`);
  await page.close();
}

await browser.close();
