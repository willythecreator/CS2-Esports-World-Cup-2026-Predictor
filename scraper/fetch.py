import os
import time
import hashlib
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

CACHE_DIR = os.path.join("data", "raw")
REQUEST_DELAY = 3  # seconds between live requests, be polite to HLTV


def _cache_path(url: str) -> str:
    """Turn a URL into a safe local filename for caching."""
    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, f"{url_hash}.html")


def fetch_page(url: str, force_refresh: bool = False) -> str:
    """
    Fetch a page's HTML using a real headless browser (Playwright + stealth patches),
    with local caching. Set force_refresh=True to bypass the cache.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = _cache_path(url)

    if not force_refresh and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    print(f"Fetching: {url}")

    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        )

        page.goto(url, timeout=45000, wait_until="domcontentloaded")

        # Cloudflare's challenge page auto-resolves after a few seconds - give it time
        for _ in range(4):
            if "Just a moment" in page.title():
                page.wait_for_timeout(5000)
            else:
                break

        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass  # some pages have ongoing background activity that never goes idle - fine to proceed

        html = page.content()
        browser.close()

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    time.sleep(REQUEST_DELAY)
    return html