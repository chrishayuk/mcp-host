# mcp_playwright_server/tools/tab_management_tools.py
from typing import Union, Optional

# imports
from models import ResponseModel, TabResponse, TabInfo

class TabManagementTools:
    @staticmethod
    def open_new_tab(url: str, tab_name: Optional[str] = None) -> ResponseModel:
        name_msg = f" with name '{tab_name}'" if tab_name else ""
        return ResponseModel(status="success", message=f"Opened new tab{name_msg} with {url}")

    @staticmethod
    def close_current_tab() -> ResponseModel:
        return ResponseModel(status="success", message="Closed the current tab")

    @staticmethod
    def close_tab(tab_identifier: Union[int, str]) -> ResponseModel:
        if isinstance(tab_identifier, int):
            return ResponseModel(status="success", message=f"Closed tab at index {tab_identifier}")
        elif isinstance(tab_identifier, str):
            return ResponseModel(status="success", message=f"Closed tab with name '{tab_identifier}'")
        else:
            return ResponseModel(status="error", message="Invalid tab identifier. Must be an int (index) or str (name)")

    @staticmethod
    def switch_to_tab(tab_identifier: Union[int, str]) -> ResponseModel:
        if isinstance(tab_identifier, int):
            return ResponseModel(status="success", message=f"Switched to tab at index {tab_identifier}")
        elif isinstance(tab_identifier, str):
            return ResponseModel(status="success", message=f"Switched to tab with name '{tab_identifier}'")
        else:
            return ResponseModel(status="error", message="Invalid tab identifier. Must be an int (index) or str (name)")

    @staticmethod
    def get_tab_info() -> TabResponse:
        tabs = [
            TabInfo(index=0, name="Main", url="https://example.com"),
            TabInfo(index=1, name="Search", url="https://search.example.com"),
        ]
        return TabResponse(status="success", tabs=tabs)
