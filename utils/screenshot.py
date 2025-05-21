import asyncio
from pathlib import Path
from playwright.sync_api import sync_playwright

def capture_screenshot(url: str, save_path: Path):
    """
    Captura una imagen de la página renderizada en modo headless.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 800},
                device_scale_factor=1
            )
            page = context.new_page()
            page.goto(url, timeout=30000, wait_until="networkidle")
            page.screenshot(path=str(save_path), full_page=True)
            browser.close()
            print(f"Captura completada para {url}")
    except Exception as e:
        print(f"Error capturando pantalla de {url}: {e}")
