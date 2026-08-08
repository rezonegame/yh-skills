#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { loadPlaywright } from "./lib/playwright-loader.mjs";
import { browserLaunchOptions } from "./lib/browser-options.mjs";
import { restrictContextToLocalRoots } from "./lib/browser-safety.mjs";

const taskDir = process.argv[2];
if (!taskDir) {
  console.error("Usage: node scripts/render-social-deck.mjs <task-dir|index.html>");
  process.exit(2);
}

const target = path.resolve(taskDir);
const stats = await fs.stat(target);
const indexPath = stats.isDirectory() ? path.join(target, "html", "index.html") : target;
const root = stats.isDirectory() ? target : path.dirname(path.dirname(target));
const outputDir = path.join(root, "output");

try {
  await fs.access(indexPath);
} catch {
  console.error(`Missing HTML entry: ${indexPath}`);
  process.exit(2);
}

const { chromium } = loadPlaywright();
await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch(browserLaunchOptions());
const context = await browser.newContext({ viewport: { width: 2400, height: 1920 }, deviceScaleFactor: 1 });
await restrictContextToLocalRoots(context, [root]);
const page = await context.newPage();

try {
  await page.goto(pathToFileURL(indexPath).href, { waitUntil: "networkidle" });
  await page.evaluate(() => (document.fonts ? document.fonts.ready.then(() => true) : true));
  await page.waitForTimeout(500);
  const selector = ".poster, .cover, .wechat-pair-preview";
  await page.locator(selector).evaluateAll((nodes) => nodes.forEach((node, index) => node.setAttribute("data-render-index", String(index))));
  const targets = await page.locator(selector).evaluateAll((nodes) => nodes.map((node, index) => ({
    selector: node.id ? `#${CSS.escape(node.id)}` : `[data-render-index="${index}"]`,
    id: node.id || `frame-${String(index + 1).padStart(2, "0")}`,
  })));

  if (!targets.length) throw new Error("No render targets found. Add .poster, .cover, or .wechat-pair-preview elements.");
  for (const item of targets) {
    const element = page.locator(item.selector).first();
    const outPath = path.join(outputDir, `${item.id}.png`);
    try {
      await fs.access(outPath);
      throw new Error(`Refusing to overwrite existing output: ${outPath}`);
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
    }
    await element.screenshot({ path: outPath });
    const box = await element.boundingBox();
    console.log(`${outPath} ${Math.round(box?.width || 0)}x${Math.round(box?.height || 0)}`);
  }
} finally {
  await browser.close();
}
