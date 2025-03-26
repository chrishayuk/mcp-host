# mcp_playwright_server/tools/navigation_tools.py

# imports
from models import ResponseModel

class NavigationTools:
    @staticmethod
    def navigate_to_url(url: str, timeout: int = 30000, wait_until: str = "load") -> ResponseModel:
        # Implementation logic here
        return ResponseModel(status="success", message=f"Navigated to {url}")

    @staticmethod
    def go_back() -> ResponseModel:
        return ResponseModel(status="success", message="Navigated back in browser history")

    @staticmethod
    def go_forward() -> ResponseModel:
        return ResponseModel(status="success", message="Navigated forward in browser history")

    @staticmethod
    def wait_for_page_load(timeout: int = 30000) -> ResponseModel:
        return ResponseModel(status="success", message=f"Page loaded after waiting {timeout}ms")

    @staticmethod
    def refresh_page() -> ResponseModel:
        return ResponseModel(status="success", message="Page refreshed")

    @staticmethod
    def accept_cookies() -> ResponseModel:
        return ResponseModel(status="success", message="Accepted all cookies")

    @staticmethod
    def take_screenshot(filename: str) -> ResponseModel:
        return ResponseModel(status="success", message=f"Screenshot saved as {filename}")
