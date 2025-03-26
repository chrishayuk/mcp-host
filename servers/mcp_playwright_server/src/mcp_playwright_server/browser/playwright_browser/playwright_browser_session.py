# browser/playwright_browser/playwright_browser_session.py
import logging

# imports
from browser.base.abstract_browser_session import AbstractBrowserSession

# playwright
from playwright.sync_api import sync_playwright, Error as PlaywrightError

# Set up basic logging.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlaywrightBrowserSession(AbstractBrowserSession):
    def __init__(self, browser_channel: str = "msedge", headless: bool = True):
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(channel=browser_channel, headless=headless)
            self.context = self.browser.new_context()
            self.pages = {}  # Optional: track pages by name
            logger.info("Playwright browser session started successfully.")
        except PlaywrightError as e:
            logger.exception("Failed to start Playwright session: %s", e)
            raise

    def new_page(self, url: str = None, name: str = None):
        """Create a new page (or equivalent) and optionally navigate to a URL."""
        try:
            page = self.context.new_page()
            if url:
                page.goto(url)
                logger.info("Navigated to URL: %s", url)
            if name:
                self.pages[name] = page
                logger.info("Stored page with name: %s", name)
            return page
        except PlaywrightError as e:
            logger.exception("Error creating new page: %s", e)
            raise

    def close(self):
        """Close the browser session."""
        try:
            self.browser.close()
         
