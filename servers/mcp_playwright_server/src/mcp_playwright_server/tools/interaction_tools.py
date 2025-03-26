# mcp_playwright_server/tools/interaction_tools.py
from models import ResponseModel, AlertAction

class InteractionTools:
    @staticmethod
    def click_element(selector: str) -> ResponseModel:
        return ResponseModel(status="success", message=f"Clicked element with selector '{selector}'")
    
    @staticmethod
    def scroll_page(x: int = 0, y: int = 0) -> ResponseModel:
        return ResponseModel(status="success", message=f"Scrolled page by x: {x}, y: {y}")

    @staticmethod
    def enter_text(selector: str, text: str) -> ResponseModel:
        return ResponseModel(status="success", message=f"Entered text into element with selector '{selector}'")

    @staticmethod
    def hover_element(selector: str) -> ResponseModel:
        return ResponseModel(status="success", message=f"Hovered over element with selector '{selector}'")

    @staticmethod
    def execute_script(script: str) -> ResponseModel:
        return ResponseModel(status="success", message="Executed custom script on the page")

    @staticmethod
    def handle_alert(alert_data: AlertAction) -> ResponseModel:
        msg = f"Alert {alert_data.action}ed"
        if alert_data.prompt_text:
            msg += f" with prompt text '{alert_data.prompt_text}'"
        return ResponseModel(status="success", message=msg)

    @staticmethod
    def wait_for_selector(selector: str, timeout: int = 30000) -> ResponseModel:
        return ResponseModel(status="success", message=f"Element '{selector}' appeared within {timeout}ms")

    @staticmethod
    def clear_cookies() -> ResponseModel:
        return ResponseModel(status="success", message="Cleared all cookies")

    @staticmethod
    def clear_cache() -> ResponseModel:
        return ResponseModel(status="success", message="Cleared browser cache")

