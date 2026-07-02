#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

const args = process.argv.slice(2);
const values = new Map();
for (let index = 0; index < args.length; index += 1) {
  if (!args[index].startsWith("--")) continue;
  values.set(args[index].slice(2), args[index + 1]);
  index += 1;
}

const taskDir = values.get("dir");
if (!taskDir) {
  console.error("Usage: node scripts/init-task.mjs --dir <task-dir> [--mode package] [--platforms xiaohongshu] [--strategy auto] [--title title]");
  process.exit(2);
}

const allowedModes = new Set(["package", "carousel", "cover", "article", "adapt"]);
const allowedStrategies = new Set(["auto", "native", "html", "hybrid"]);
const mode = values.get("mode") || "package";
const strategy = values.get("strategy") || "auto";
if (!allowedModes.has(mode)) throw new Error(`Unsupported mode: ${mode}`);
if (!allowedStrategies.has(strategy)) throw new Error(`Unsupported strategy: ${strategy}`);

const root = path.resolve(taskDir);
const manifestPath = path.join(root, "manifest.json");
try {
  await fs.access(manifestPath);
  console.error(`Task already exists: ${manifestPath}`);
  process.exit(1);
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
}

for (const name of ["prompts", "html", "sources", "output"]) {
  await fs.mkdir(path.join(root, name), { recursive: true });
}

const now = new Date().toISOString();
const platforms = (values.get("platforms") || "")
  .split(",")
  .map((item) => item.trim())
  .filter(Boolean);
const title = values.get("title") || path.basename(root);
const manifest = {
  schema_version: 1,
  title,
  mode,
  platforms,
  render_strategy: strategy,
  created_at: now,
  updated_at: now,
  assets: [],
};

const illustrationConcepts = mode === "article"
  ? `\n## Illustration Concepts\n\n| ID | Placement | Visual form | Cognitive anchor | Conflict / action | Object / subject | Facts / source | Text policy | Three-second read | Failure signals |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n\nFor each concept, also record the composition archetype, invariants, content-specific relationship, difference from other package images, originality risk, and whether it is core or optional.\n`
  : "";
const brief = `# ${title}\n\n## Goal\n\n## Audience\n\n## Platforms\n${platforms.map((item) => `- ${item}`).join("\n") || "- TBD"}\n\n## Content Breakdown\n${illustrationConcepts}\n## Asset Plan\n\n## Constraints\n`;
await fs.writeFile(path.join(root, "brief.md"), brief, "utf8");
await fs.writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
console.log(root);
