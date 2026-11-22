"""A headless Chromium in a sandbox (public template "browser"), driven with Playwright over CDP.
The browser is already running when the sandbox starts; no browser is installed on your machine.

    pip install playwright   # no `playwright install` needed
    python browser_playwright.py https://example.com
"""
import sys

from e2b import Sandbox
from playwright.sync_api import sync_playwright


def title_of(sandbox: Sandbox, url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("https://" + sandbox.get_host(9222))
        page = browser.contexts[0].new_page()
        page.goto(url)
        title = page.title()
        page.screenshot(path="page.png")
        browser.close()
        return title


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    with Sandbox.create("browser", timeout=300) as sandbox:
        print(title_of(sandbox, url), "(screenshot in page.png)")
