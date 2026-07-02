import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";

const require = createRequire(import.meta.url);

function tryRequire(specifier) {
  try {
    return require(specifier);
  } catch (error) {
    if (error?.code !== "MODULE_NOT_FOUND") throw error;
    return null;
  }
}

function tryPnpmStore(root) {
  const store = path.join(root, ".pnpm");
  try {
    const packageDir = fs.readdirSync(store, { withFileTypes: true })
      .find((entry) => entry.isDirectory() && entry.name.startsWith("playwright@"));
    if (!packageDir) return null;
    return tryRequire(path.join(store, packageDir.name, "node_modules", "playwright"));
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
    return null;
  }
}

export function loadPlaywright() {
  const local = tryRequire("playwright");
  if (local) return local;

  const roots = [process.env.CODEX_NODE_MODULES, ...(process.env.NODE_PATH || "").split(path.delimiter)]
    .filter(Boolean);

  for (const root of roots) {
    const candidate = tryRequire(path.join(root, "playwright"));
    if (candidate) return candidate;
    const pnpmCandidate = tryPnpmStore(root);
    if (pnpmCandidate) return pnpmCandidate;
  }

  throw new Error(
    "Playwright was not found. Install it locally or set CODEX_NODE_MODULES to the Node packages path returned by the Codex workspace dependency loader."
  );
}
