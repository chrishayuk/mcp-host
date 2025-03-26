# browser/base/abstract_browser_session.py
from abc import ABC, abstractmethod

class AbstractBrowserSession(ABC):
    """
    Abstract base class for a browser session.
    This can be implemented by a Playwright session, an HTTP client session, etc.
    """
    @abstractmethod
    def new_page(self, url: str = None, name: str = None):
        """Create a new page (or equivalent) and optionally navigate to a URL."""
        pass

    @abstractmethod
    def close(self):
        """Close the browser session."""
        pass