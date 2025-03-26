# test_browser_sessions.py
import json
import pytest

# imports
from mcp_playwright_server.browser.playwright_browser.json_browser_session import JsonBrowserSession


# --- JSON Browser Session Tests ---
def test_json_browser_session_new_page():
    session = JsonBrowserSession()
    response = json.loads(session.new_page(url="http://example.com", name="TestPage"))
    assert response["status"] == "success", "New page should be created successfully"
    assert response["page"]["name"] == "TestPage", "Page name should match"
    assert response["page"]["url"] == "http://example.com", "Page URL should match"


def test_json_browser_session_close():
    session = JsonBrowserSession()
    # Create a page first.
    _ = session.new_page(url="http://example.com", name="TestPage")
    response_close = json.loads(session.close())
    assert response_close["status"] == "success", "Session should close successfully"
    # After closing, new_page should return an error.
    response_new = json.loads(session.new_page(url="http://example.com", name="AfterClose"))
    assert response_new["status"] == "error", "Should not be able to create a new page after session is closed"


# --- Playwright Browser Session Tests ---
# These tests require a working browser and Playwright installation.
# They are marked to skip by default. Remove the skip marker if you want to run them.

@pytest.mark.skip(reason="Requires Playwright and browser availability")
def test_playwright_browser_session_new_page():
    session = PlaywrightBrowserSession(browser_channel="msedge", headless=True)
    page = session.new_page(url="http://example.com", name="TestPage")
    # Check if the page navigated to the expected URL.
    # Note: Depending on network conditions, you might need to wait or perform additional checks.
    assert "example.com" in page.url, "Page URL should contain 'example.com'"
    session.close()


@pytest.mark.skip(reason="Requires Playwright and browser availability")
def test_playwright_browser_session_close():
    session = PlaywrightBrowserSession(browser_channel="msedge", headless=True)
    session.new_page(url="http://example.com", name="TestPage")
    session.close()
    # Our implementation doesn't explicitly prevent new page creation after close,
    # but we can check that the internal pages dictionary is emptied.
    assert session.pages == {}, "Pages dictionary should be empty after closing the session"
