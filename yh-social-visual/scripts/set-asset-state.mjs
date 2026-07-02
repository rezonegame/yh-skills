#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

const [taskDir, assetId, nextState, ...pairs] = process.argv.slice(2);
const states = new Set(["planned", "awaiting-generation", "generated", "awaiting-composition", "rendered", "validated", "failed"]);
if (!taskDir || !assetId || !states.has(nextState)) {
  console.error("Usage: node scripts/set-asset-state.mjs <task-dir> <asset-id> <state> [field=value ...]");
  process.exit(2);
}

const manifestPath = path.resolve(taskDir, "manifest.json");
const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));
const asset = manifest.assets.find((item) => item.id === assetId);
if (!asset) throw new Error(`Unknown asset: ${assetId}`);

asset.state = nextState;
for (const pair of pairs) {
  const separator = pair.indexOf("=");
  if (separator < 1) throw new Error(`Expected field=value, received: ${pair}`);
  asset[pair.slice(0, separator)] = pair.slice(separator + 1) || null;
}
manifest.updated_at = new Date().toISOString();

const temporary = `${manifestPath}.tmp`;
await fs.writeFile(temporary, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
await fs.rename(temporary, manifestPath);
console.log(`${assetId}: ${nextState}`);

