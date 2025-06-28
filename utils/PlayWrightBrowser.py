
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class PlayWrightBrowser():

    def __init__(self):
        p = sync_playwright().start()
        browser = p.chromium.launch(
            channel="chrome",  
            headless=False,    
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            locale="en-US",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
            }
        )
        
        context.add_init_script("""
        delete Object.getPrototypeOf(navigator).webdriver;
        window.chrome = {runtime: {}};
        """)

        self.browser = browser
        self.p = p

    def new_page(self):
        return self.browser.new_page()
    
    def close(self):
        self.browser.close()
        self.p.stop()
        return True
    
