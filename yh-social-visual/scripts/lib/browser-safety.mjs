import path from "node:path";
import { fileURLToPath } from "node:url";

function isWithin(candidate, root) {
  const relative = path.relative(root, candidate);
  return relative === "" || (!relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative));
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
    try {
      const candidate = path.resolve(fileURLToPath(url));
      return allowedRoots.some((root) => isWithin(candidate, root))
        ? route.continue()
        : route.abort();
    } catch {
      return route.abort();
    }
  });
}
