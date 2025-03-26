# browser_script.py
# browser_script.py
import os
import sys

# Determine the project root directory.
project_root = os.path.abspath(os.path.dirname(__file__))
print(project_root)

# Define the absolute paths to your source directories.
# We use the parent directory of the package directories to ensure proper imports.
common_src = os.path.join(project_root, "common", "src")
runtime_src = os.path.join(project_root, "runtime", "src")

# Insert them into sys.path (if they're not already present).
# We reverse the order to ensure the first path is highest priority.
paths = [common_src, runtime_src]
for path in reversed(paths):
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

# Now import the browser tools from our modular structure.
from tools.navigation_tools import NavigationTools
from tools.tab_management_tools import TabManagementTools
from tools.interaction_tools import InteractionTools
from models import AlertAction

def simulate_ticket_search():
    responses = []
    
    # 1. Search for "Scouting for Girls" tickets by navigating to a search URL
    responses.append(NavigationTools.navigate_to_url("https://www.ticketsearch.com?q=Scouting+for+Girls"))
    responses.append(NavigationTools.wait_for_page_load(timeout=5000))
    
    # 2. Click on Bandsintown for Colchester tickets
    responses.append(InteractionTools.click_element("a[href='https://bandsintown.com/colchester']"))
    responses.append(NavigationTools.wait_for_page_load(timeout=5000))
    
    # 3. Select Ticketmaster for concert tickets
    responses.append(InteractionTools.click_element("a[href='https://ticketmaster.com/concerts']"))
    responses.append(NavigationTools.wait_for_page_load(timeout=5000))
    
    # 4. Navigate back to Bandsintown for tickets
    responses.append(NavigationTools.go_back())
    responses.append(NavigationTools.wait_for_page_load(timeout=5000))
    
    # 5. On Bandsintown, select "See Tickets"
    responses.append(InteractionTools.click_element("button#see-tickets"))
    responses.append(NavigationTools.wait_for_page_load(timeout=5000))
    
    # 6. Refresh the page
    responses.append(NavigationTools.refresh_page())
    
    # 7. Open a new tab for further ticket options and name it "Bandsintown"
    responses.append(TabManagementTools.open_new_tab("https://bandsintown.com/tickets", tab_name="Bandsintown"))
    responses.append(NavigationTools.wait_for_page_load(timeout=5000))
    
    # 8. Switch to the "Bandsintown" tab (simulate returning to it)
    responses.append(TabManagementTools.switch_to_tab("Bandsintown"))
    responses.append(NavigationTools.wait_for_page_load(timeout=5000))
    
    # 9. On Bandsintown, select "Gigantic tickets"
    responses.append(InteractionTools.click_element("button#gigantic-tickets"))
    responses.append(NavigationTools.wait_for_page_load(timeout=5000))
    
    # 10. Check ticket options for Busted: scroll and take a screenshot of options
    responses.append(InteractionTools.scroll_page(y=500))
    responses.append(NavigationTools.take_screenshot("busted_ticket_options.png"))
    
    # 11. Accept all cookies for browsing
    responses.append(NavigationTools.accept_cookies())
    
    # 12. Demonstrate additional interactions:
    responses.append(InteractionTools.enter_text("input#search", "Busted tickets"))
    responses.append(InteractionTools.hover_element("div#ticket-info"))
    responses.append(InteractionTools.execute_script("console.log('Custom script executed');"))
    # Pass an AlertAction instance instead of a simple string.
    responses.append(InteractionTools.handle_alert(AlertAction(action="accept")))
    responses.append(InteractionTools.wait_for_selector("div.ticket-list", timeout=5000))
    responses.append(InteractionTools.clear_cookies())
    responses.append(InteractionTools.clear_cache())
    
    # 13. Close the current tab
    responses.append(TabManagementTools.close_current_tab())
    
    # 14. Retrieve and print information about remaining open tabs
    tab_info = TabManagementTools.get_tab_info()
    responses.append(tab_info)
    
    # Print out responses for each step.
    for idx, response in enumerate(responses, start=1):
        try:
            # If the response is a Pydantic model, print its JSON representation.
            print(f"Step {idx}: {response.model_dump_json()}")
        except AttributeError:
            print(f"Step {idx}: {response}")

if __name__ == "__main__":
    simulate_ticket_search()
