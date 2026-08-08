#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadPlaywright } from "../yh-social-visual/scripts/lib/playwright-loader.mjs";
import { browserLaunchOptions } from "../yh-social-visual/scripts/lib/browser-options.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "output", "playwright", "template-representatives");
const cases = [
  ["presentation-4x3", "yh-slides/templates/upstream/ppt-master/layouts/presentation_core_43/templates/01_title_slide.svg", 1024, 768],
  ["formal-report-16x9", "yh-slides/templates/upstream/ppt-master/layouts/report_core/templates/01_cover.svg", 1280, 720],
  ["editorial-full-bleed-16x9", "yh-slides/templates/upstream/ppt-master/layouts/editorial_bleed/templates/01_hero_full.svg", 1280, 720],
  ["xiaohongshu-3x4", "yh-social-visual/assets/upstream/ppt-master/layouts/xiaohongshu_post/templates/01_cover.svg", 1242, 1660],
  ["story-9x16", "yh-social-visual/assets/upstream/ppt-master/layouts/story_vertical/templates/01_cover.svg", 1080, 1920],
  ["moments-1x1", "yh-social-visual/assets/upstream/ppt-master/layouts/moments_square/templates/01_cover.svg", 1080, 1080],
];

await fs.mkdir(output, { recursive: true });
const { chromium } = loadPlaywright();
const browser = await chromium.launch(browserLaunchOptions());
const evidence = [];
try {
  for (const [name, relative, width, height] of cases) {
    const source = path.join(root, relative);
    const svg = await fs.readFile(source, "utf8");
    if (!svg.includes(`width="${width}"`) || !svg.includes(`height="${height}"`)) {
      throw new Error(`${relative}: declared canvas differs from ${width}x${height}`);
    }
    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
    await page.route("http://**", route => route.abort());
    await page.route("https://**", route => route.abort());
    await page.setContent(`<!doctype html><meta charset="utf-8"><style>html,body{margin:0;width:100%;height:100%;overflow:hidden}svg{display:block;width:100%;height:100%}</style>${svg}`, { waitUntil: "load" });
    const target = path.join(output, `${name}.png`);
    await page.screenshot({ path: target, type: "png" });
    evidence.push({ name, source: relative.replaceAll("\\", "/"), width, height, output: path.relative(root, target).replaceAll("\\", "/") });
    await page.close();
  }
} finally {
  await browser.close();
}
await fs.writeFile(path.join(output, "render-manifest.json"), JSON.stringify({ schema: "skill-portfolio.representative-renders.v1", network: false, cases: evidence }, null, 2) + "\n", "utf8");
console.log(`OK: rendered ${evidence.length} representative templates to ${path.relative(root, output)}`);
