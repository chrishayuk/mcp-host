import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch a Chromium browser instance (set headless to False to see the browser)
        browser = await p.chromium.launch(headless=False)
        
        # Create a new browser page
        page = await browser.new_page()
        
        # Navigate to the desired URL
        await page.goto("https://techmeme.com")
        
        # Optionally, wait for an element to ensure the page has loaded
        #await page.wait_for_selector("h1")
        
        # Close the browser
        await browser.close()

# Run the async function
asyncio.run(run())