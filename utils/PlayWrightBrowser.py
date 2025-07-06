
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright 

class PlayWrightBrowser():
    def __init__(self):
        self.browser = None
        self.playwright = None
        self.context = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            channel="chrome",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            locale="en-US",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
            }
        )
        
        await self.context.add_init_script("""
        delete Object.getPrototypeOf(navigator).webdriver;
        window.chrome = {runtime: {}};
        """)

    async def new_page(self):
        return await self.context.new_page()
    
    @asynccontextmanager
    async def open_page(self):
        page = await self.new_page()
        try:
            yield page
        finally:
            await page.close()
   
    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        return True
    

import asyncio
async def main():
    async with PlayWrightBrowser() as browser:
        try:
            page = await browser.new_page()
            await page.goto("https://get.stampli.com/cfo-recession-toolkit-2022")
            content = await page.content()
            soup = BeautifulSoup(content, 'lxml')
            print(soup.title.text)
        finally:
            await page.close()

if __name__ == "__main__":
    asyncio.run(main())
    
