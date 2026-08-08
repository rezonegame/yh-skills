#!/usr/bin/env node
/** Validate both legacy package manifests and geometry-aware platform fixtures. */

import { existsSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const STYLE_PRESETS = new Set(['ink', 'paper', 'editorial', 'warm', 'cool', 'mono', 'forest', 'sunset', 'night', 'signal']);
const PLATFORM_PRESETS = {
  'xhs-carousel': { ratio: '3:4', safe: .05, text: .08 },
  'xhs-cover': { ratio: '3:4', safe: .05, text: .08 },
  'wechat-cover-21-9': { ratio: '21:9', safe: .03, text: .06 },
  'wechat-cover-1-1': { ratio: '1:1', safe: .04, text: .08 },
  'weibo-card': { ratio: '2:3', safe: .04, text: .06 },
  'zhihu-card': { ratio: '16:9', safe: .03, text: .05 },
  'douyin-cover': { ratio: '9:16', safe: .08, text: .10 },
  'article-cover': { ratio: '16:9', safe: .03, text: .05 },
  'article-inline': { ratio: '16:9', safe: .02, text: .04 },
  'portrait-generic': { ratio: '9:16', safe: .08, text: .10 },
  'square-generic': { ratio: '1:1', safe: .04, text: .08 },
  'landscape-generic': { ratio: '16:9', safe: .03, text: .05 },
};

function result(check, status, message = '') { return { check, status, ...(message ? { message } : {}) }; }
function validBounds(value) {
  return value && ['top', 'right', 'bottom', 'left'].every(k => Number.isFinite(value[k]) && value[k] >= 0 && value[k] <= 1);
}
function rgb(hex) {
  let h = String(hex).replace('#', '');
  if (h.length === 3) h = [...h].map(c => c + c).join('');
  if (!/^[0-9a-f]{6}$/i.test(h)) return null;
  return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16));
}
function luminance(hex) {
  const value = rgb(hex);
  if (!value) return null;
  const channels = value.map(c => (c /= 255) <= .03928 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4);
  return .2126 * channels[0] + .7152 * channels[1] + .0722 * channels[2];
}
function contrast(a, b) {
  const x = luminance(a), y = luminance(b);
  if (x === null || y === null) return null;
  return (Math.max(x, y) + .05) / (Math.min(x, y) + .05);
}
function blockMargins(block) {
  const left = block.x ?? 0, top = block.y ?? 0;
  return { left, top, right: 1 - left - (block.w ?? 0), bottom: 1 - top - (block.h ?? 0) };
}

function validatePlatformAsset(asset, baseDir, label) {
  const checks = [];
  const name = asset.platform_preset || (PLATFORM_PRESETS[asset.preset] ? asset.preset : null);
  const spec = name ? PLATFORM_PRESETS[name] : null;
  checks.push(spec ? result(`${label}.platform-preset`, 'pass') : result(`${label}.platform-preset`, 'fail', `Unknown or missing platform preset: ${name || '(missing)'}`));
  if (!spec) return checks;
  const ratio = asset.target_ratio || asset.aspect_ratio;
  checks.push(ratio === spec.ratio ? result(`${label}.ratio`, 'pass') : result(`${label}.ratio`, 'fail', `Expected ${spec.ratio}, got ${ratio || '(missing)'}`));
  const colors = asset.colors || [];
  const nonAchromatic = colors.filter(c => !['#000', '#fff', '#000000', '#ffffff'].includes(String(c).toLowerCase()));
  checks.push(nonAchromatic.length <= 3 ? result(`${label}.colors`, 'pass') : result(`${label}.colors`, 'warn', `${nonAchromatic.length} non-achromatic colors (max 3)`));
  for (const block of asset.text_blocks || []) {
    const margins = blockMargins(block);
    if (Object.values(margins).some(v => v < spec.text)) checks.push(result(`${label}.text-bounds`, 'fail', `Text block ${block.id || '(unnamed)'} exceeds text bounds`));
    if (Object.values(margins).some(v => v < spec.safe)) checks.push(result(`${label}.safe-bounds`, 'fail', `Text block ${block.id || '(unnamed)'} enters crop zone`));
    if (block.color && block.background) {
      const ratioValue = contrast(block.color, block.background);
      if (ratioValue === null || ratioValue < 4.5) checks.push(result(`${label}.contrast`, 'fail', `Text block ${block.id || '(unnamed)'} is below WCAG AA`));
    }
  }
  for (const media of asset.media_refs || []) {
    if (!existsSync(resolve(baseDir, media))) checks.push(result(`${label}.media`, 'fail', `Missing local media: ${media}`));
  }
  if (!checks.some(c => c.check === `${label}.text-bounds`)) checks.push(result(`${label}.text-bounds`, 'pass'));
  if (!checks.some(c => c.check === `${label}.safe-bounds`)) checks.push(result(`${label}.safe-bounds`, 'pass'));
  if (!checks.some(c => c.check === `${label}.contrast`)) checks.push(result(`${label}.contrast`, 'pass'));
  if (!checks.some(c => c.check === `${label}.media`)) checks.push(result(`${label}.media`, 'pass'));
  return checks;
}

function validateManifest(data, baseDir) {
  if (!Array.isArray(data.assets) || data.assets.length === 0) return [result('assets', 'fail', 'assets must be a non-empty array')];
  const checks = [];
  data.assets.forEach((asset, index) => {
    const label = `assets[${index}]`;
    const style = asset.style_preset || (STYLE_PRESETS.has(asset.preset) ? asset.preset : null);
    checks.push(STYLE_PRESETS.has(style) ? result(`${label}.style-preset`, 'pass') : result(`${label}.style-preset`, 'fail', `Unknown style preset: ${style || '(missing)'}`));
    checks.push(/^\d+:\d+$/.test(asset.aspect_ratio || '') ? result(`${label}.aspect-ratio`, 'pass') : result(`${label}.aspect-ratio`, 'fail', 'Invalid aspect_ratio'));
    checks.push(validBounds(asset.safe_text_bounds) ? result(`${label}.safe-text-bounds`, 'pass') : result(`${label}.safe-text-bounds`, 'fail', 'Invalid safe_text_bounds'));
    if (asset.color_override) checks.push(result(`${label}.color-override`, 'fail', 'Arbitrary color_override is not allowed'));
    if (asset.platform_preset) checks.push(...validatePlatformAsset(asset, baseDir, label));
  });
  return checks;
}

const input = process.argv[2];
if (!input) { console.error('Usage: node scripts/validate_social_preset.mjs <manifest-or-fixture.json>'); process.exit(2); }
const fullPath = resolve(input);
let data;
try { data = JSON.parse(readFileSync(fullPath, 'utf8')); }
catch (error) { console.error(JSON.stringify({ error: error.message })); process.exit(2); }

const checks = Array.isArray(data.assets)
  ? validateManifest(data, dirname(fullPath))
  : validatePlatformAsset(data, dirname(fullPath), 'asset');
const summary = Object.fromEntries(['pass', 'fail', 'warn'].map(status => [status, checks.filter(c => c.status === status).length]));
const verdict = summary.fail ? 'FAIL' : summary.warn ? 'WARN' : 'PASS';
console.log(JSON.stringify({ input, checks, summary, verdict }, null, 2));
process.exit(summary.fail ? 1 : 0);
