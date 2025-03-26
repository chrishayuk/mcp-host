# browser/json_browser_session.py
import json

# imports
from browser.base.abstract_browser_session import AbstractBrowserSession

class JsonBrowserSession(AbstractBrowserSession):
    def __init__(self):
        # Simulate an internal store for "pages"
        self.pages = {}
        self.session_active = True

    def new_page(self, url: str = None, name: str = None):
        """Simulate creating a new page and optionally navigating to a URL."""
        if not self.session_active:
            return json.dumps({
                "status": "error",
                "message": "Session is closed."
            })
        # Here, a "page" is simulated by a dict.
        page = {"url": url or "", "name": name or "Unnamed"}
        if name:
            self.pages[name] = page
        return json.dumps({
            "status": "success",
            "message": f"New page created{' and navigated to ' + url if url else ''}.",
            "page": page
        })

    def close(self):
        """Simulate closing the browser session."""
        if not self.session_active:
            return json.dumps({
                "status": "error",
                "message": "Session already closed."
            })
        self.session_active = False
        self.pages = {}
        return json.dumps({
            "status": "success",
            "message": "Browser session closed."
        })
