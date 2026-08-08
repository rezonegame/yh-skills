import fs from "node:fs";
import os from "node:os";
import path from "node:path";

export function browserLaunchOptions() {
  const home = os.homedir();
  const candidates = [
    process.env.PLAYWRIGHT_CHROME_EXECUTABLE,
    process.platform === "win32" ? path.join(process.env.PROGRAMFILES || "", "Google", "Chrome", "Application", "chrome.exe") : null,
    process.platform === "win32" ? path.join(process.env["PROGRAMFILES(X86)"] || "", "Google", "Chrome", "Application", "chrome.exe") : null,
    process.platform === "win32" ? path.join(process.env.LOCALAPPDATA || "", "Google", "Chrome", "Application", "chrome.exe") : null,
    process.platform === "win32" ? path.join(process.env.PROGRAMFILES || "", "Microsoft", "Edge", "Application", "msedge.exe") : null,
    process.platform === "darwin" ? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" : null,
    process.platform === "linux" ? "/usr/bin/google-chrome" : null,
    process.platform === "linux" ? "/usr/bin/chromium" : null,
    process.platform === "linux" ? "/usr/bin/chromium-browser" : null,
    process.platform === "linux" ? path.join(home, ".local", "bin", "google-chrome") : null,
  ].filter(Boolean);

  const executablePath = candidates.find((candidate) => fs.existsSync(candidate));
  return {
    headless: true,
    ...(executablePath ? { executablePath } : {}),
    args: [],
  };
}
