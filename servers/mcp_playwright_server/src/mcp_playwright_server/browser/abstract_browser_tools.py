# abstract_browser_tools.py
from abc import ABC, abstractmethod

# Abstract base classes for a browser session and tools

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


class AbstractNavigationTools(ABC):
    """
    Abstract base class for navigation-related actions.
    """
    @abstractmethod
    def navigate_to_url(self, url: str, timeout: int = 30000):
        """Navigate to a URL."""
        pass

    @abstractmethod
    def wait_for_page_load(self, timeout: int = 30000):
        """Wait for the page to load completely."""
        pass

    @abstractmethod
    def refresh_page(self):
        """Refresh the current page."""
        pass

    @abstractmethod
    def go_back(self):
        """Navigate back in browser history."""
        pass


class AbstractInteractionTools(ABC):
    """
    Abstract base class for interaction-related actions.
    """
    @abstractmethod
    def click_element(self, selector: str):
        """Click an element identified by the given selector."""
        pass

    @abstractmethod
    def enter_text(self, selector: str, text: str):
        """Enter text into an element."""
        pass

    @abstractmethod
    def hover_element(self, selector: str):
        """Hover over an element."""
        pass

    @abstractmethod
    def execute_script(self, script: str):
        """Execute a custom script on the page."""
        pass

    @abstractmethod
    def scroll_page(self, x: int = 0, y: int = 0):
        """Scroll the page by the specified offsets."""
        pass

    @abstractmethod
    def take_screenshot(self, filename: str, full_page: bool = False):
        """Take a screenshot of the page."""
        pass


class AbstractTabManagementTools(ABC):
    """
    Abstract base class for tab management actions.
    """
    @abstractmethod
    def open_new_tab(self, url: str, tab_name: str = None):
        """Open a new tab with the given URL."""
        pass

    @abstractmethod
    def switch_to_tab(self, tab_identifier: str):
        """Switch to an existing tab."""
        pass

    @abstractmethod
    def close_tab(self, tab_identifier: str):
        """Close a specified tab."""
        pass

    @abstractmethod
    def get_tab_info(self):
        """Retrieve information about open tabs."""
        pass
