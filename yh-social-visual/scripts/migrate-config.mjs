#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const skillDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const skillsDir = path.dirname(skillDir);
const source = path.join(skillsDir, ".yh-skills", "yh-article-visual", "EXTEND.md");
const target = path.join(skillsDir, ".yh-skills", "yh-social-visual", "EXTEND.md");

async function readIfPresent(filePath) {
  try {
    return await fs.readFile(filePath, "utf8");
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    throw error;
  }
}

function migrate(content) {
  const lines = content.split(/\r?\n/)
    .filter((line) => !/^preferred_image_backend\s*:/.test(line));
  const strategyIndex = lines.findIndex((line) => /^render_strategy\s*:/.test(line));
  if (strategyIndex < 0) {
    const versionIndex = lines.findIndex((line) => /^version\s*:/.test(line));
    lines.splice(versionIndex >= 0 ? versionIndex + 1 : 1, 0, "render_strategy: auto");
  }
  return `${lines.join("\n").replace(/\n+$/, "")}\n`;
}

const sourceContent = await readIfPresent(source);
const desired = migrate(sourceContent || "---\nversion: 1\noutput_root: assets\n---\n");
const current = await readIfPresent(target);

await fs.mkdir(path.dirname(target), { recursive: true });
if (current === desired) {
  console.log(`Already up to date: ${target}`);
  process.exit(0);
}

if (current !== null) {
  const backup = `${target}.bak-${new Date().toISOString().replace(/[:.]/g, "-")}`;
  await fs.copyFile(target, backup);
  console.log(`Backed up: ${backup}`);
}

await fs.writeFile(target, desired, "utf8");
console.log(`Migrated: ${sourceContent === null ? "defaults" : source} -> ${target}`);

