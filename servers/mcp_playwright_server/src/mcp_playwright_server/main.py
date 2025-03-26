# main.py
# imports
from models import AlertAction
from tools.navigation_tools import NavigationTools
from tools.tab_management_tools import TabManagementTools
from tools.interaction_tools import InteractionTools

def main():
    # Example usage of Navigation Tools
    nav_response = NavigationTools.navigate_to_url("https://example.com")
    print(nav_response.model_dump_json())

    # Example usage of Tab Management Tools
    tab_response = TabManagementTools.get_tab_info()
    print(tab_response.model_dump_json())

    # Example usage of Interaction Tools
    alert_action = AlertAction(action="accept", prompt_text="Sample prompt")
    alert_response = InteractionTools.handle_alert(alert_action)
    print(alert_response.model_dump_json())

if __name__ == "__main__":
    main()
