"""Browser utilities for SciVal automation"""

import asyncio
import nodriver as uc
from pathlib import Path
from config import BROWSER_ARGS, DOWNLOAD_DIR

async def create_browser():
    """Create and configure browser instance"""
    try:
        browser = await uc.start(
            headless=False,
            no_sandbox=True,
            args=BROWSER_ARGS
        )
        print("Browser started successfully")
        return browser
    except Exception as e:
        print(f"Failed to start browser: {e}")
        raise

async def safe_browser_cleanup(browser):
    """Safely cleanup browser to avoid errors"""
    if browser:
        try:
            await browser.stop()
        except Exception as cleanup_error:
            print(f"Error during browser cleanup: {cleanup_error}")
