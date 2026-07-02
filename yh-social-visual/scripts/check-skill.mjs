#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const failures = [];

async function read(relative) {
  try {
    return await fs.readFile(path.join(root, relative), "utf8");
  } catch (error) {
    failures.push(`missing ${relative}: ${error.message}`);
    return "";
  }
}

const skill = await read("SKILL.md");
if (!/^---[\s\S]*?name:\s*yh-social-visual\s*$/m.test(skill)) failures.push("invalid skill frontmatter name");
if (!skill.includes("description:")) failures.push("missing frontmatter description");
if (skill.split(/\r?\n/).length > 500) failures.push("SKILL.md exceeds 500 lines");

const requiredFiles = [
  "references/illustrations/visual-conception.md",
  "references/illustrations/story-scroll.md",
  "assets/social-card/template-story-scroll.html",
  "LICENSE.ian-xiaohei-methods",
];
for (const relative of requiredFiles) await read(relative);

for (const match of skill.matchAll(/`((?:references|assets)\/[^`]+)`/g)) {
  const reference = match[1].replace(/\/$/, "");
  try {
    await fs.access(path.join(root, reference));
  } catch {
    failures.push(`broken SKILL.md reference: ${reference}`);
  }
}

for (const forbidden of ["../yh-image", "preferred_image_backend", "references/social-cards/guizang-social-card-skill", "scripts/main.ts"]) {
  if (skill.includes(forbidden)) failures.push(`forbidden runtime reference in SKILL.md: ${forbidden}`);
}

const conception = await read("references/illustrations/visual-conception.md");
for (const marker of ["concept-metaphor", "object-scene", "story-scroll", "semantic-subject", "Critical QA"]) {
  if (!conception.includes(marker)) failures.push(`missing conception marker: ${marker}`);
}

const story = await read("references/illustrations/story-scroll.md");
for (const marker of ["2400×900", "5–8", "data-story-node", "data-story-base-reviewed", "normalized"]) {
  if (!story.includes(marker)) failures.push(`missing story-scroll marker: ${marker}`);
}

const storyTemplate = await read("assets/social-card/template-story-scroll.html");
if (!storyTemplate.includes('class="poster story-scroll"')) failures.push("story-scroll seed lacks poster root");
if ((storyTemplate.match(/data-story-node/g) || []).length < 5) failures.push("story-scroll seed lacks five nodes");
if ((storyTemplate.match(/data-story-anchor/g) || []).length < 5) failures.push("story-scroll seed lacks five object anchors");

const attribution = await read("references/source-attribution.md");
for (const commit of ["91b560849e8f883922cc2fa8a358a668caa94105", "3555bcb9ecaba284aec77ee492fdfd21c52faae3"]) {
  if (!attribution.includes(commit)) failures.push(`missing source commit: ${commit}`);
}

try {
  const evals = JSON.parse(await read("evals/evals.json"));
  if (evals.skill_name !== "yh-social-visual") failures.push("eval skill_name mismatch");
  if (!Array.isArray(evals.evals) || evals.evals.length < 5) failures.push("insufficient eval coverage");
} catch (error) {
  failures.push(`invalid eval JSON: ${error.message}`);
}

if (failures.length) {
  failures.forEach((failure) => console.error(`FAIL ${failure}`));
  process.exit(1);
}
console.log("PASS yh-social-visual static checks");
