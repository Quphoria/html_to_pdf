from playwright.async_api import async_playwright


class PlaywrightService:
    def __init__(self, playwright):
        self.playwright = playwright
        self.browser = None

    @classmethod
    async def create(cls):
        playwright = await async_playwright().start()
        return cls(playwright=playwright)

    async def start_browser(self):
        self.browser = await self.playwright.chromium.launch(headless=True)
        return self

    async def stop(self):
        if self.browser:
            await self.browser.close()
            self.browser = None

        await self.playwright.stop()

    async def new_context(self, **kwargs):
        return await self.browser.new_context(**kwargs)
