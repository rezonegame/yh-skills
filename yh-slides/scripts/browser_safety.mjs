import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

function isWithin(candidate, root) {
  const relative = path.relative(root, candidate);
  return relative === "" || (!relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative));
}

export function localFileUrl(filePath) {
  return pathToFileURL(path.resolve(filePath)).href;
}

export async function restrictContextToLocalRoots(context, roots) {
  const allowedRoots = [...new Set(roots.map((root) => path.resolve(root)))];
  await context.route("**/*", (route) => {
    const requestUrl = route.request().url();
    let url;
    try {
      url = new URL(requestUrl);
    } catch {
      return route.abort();
    }
    if (url.protocol === "data:" || url.protocol === "blob:" || url.protocol === "about:") {
      return route.continue();
    }
    if (url.protocol !== "file:") return route.abort();
    let candidate;
    try {
      candidate = path.resolve(fileURLToPath(url));
    } catch {
      return route.abort();
    }
    return allowedRoots.some((root) => isWithin(candidate, root))
      ? route.continue()
      : route.abort();
  });
}
