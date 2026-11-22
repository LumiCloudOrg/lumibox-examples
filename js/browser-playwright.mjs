// A headless Chromium in a sandbox (public template "browser"), driven with Playwright over CDP.
// The browser is already running when the sandbox starts; nothing to install but playwright-core.
//   node browser-playwright.mjs https://example.com
import { Sandbox } from "e2b"
import { chromium } from "playwright-core"

export async function titleOf(sandbox, url) {
  const browser = await chromium.connectOverCDP(`https://${sandbox.getHost(9222)}`)
  try {
    const page = await browser.contexts()[0].newPage()
    await page.goto(url)
    await page.screenshot({ path: "page.png" })
    return await page.title()
  } finally {
    await browser.close()
  }
}

if (import.meta.main) {
  const sandbox = await Sandbox.create("browser", { timeoutMs: 300_000 })
  try {
    console.log(await titleOf(sandbox, process.argv[2] ?? "https://example.com"), "(screenshot in page.png)")
  } finally {
    await sandbox.kill()
  }
}
