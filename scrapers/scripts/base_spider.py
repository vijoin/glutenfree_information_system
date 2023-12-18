from playwright.sync_api import sync_playwright, Playwright


class Spider():

    async def get_browser(self):
        # async with async_playwright() as p:
        p = async_playwright()

        return await p.chromium.launch(headless=False)

    
        