from bs4 import BeautifulSoup
import re
from contextlib import asynccontextmanager
from utils.Parser import parse_target_info, target_info
from utils.PlayWrightBrowser import PlayWrightBrowser

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_content_from_soup(soup) -> list:
    content = []

    for script in soup(['script', 'style', 'noscript', 'iframe']):
        script.decompose()

    desc = soup.find('meta', attrs={'name': 'description'})
    if desc:
        content.append(f"Description: {desc['content']}")
        
    main_content = soup.find('body')
    if main_content:
        for tag in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
            text = clean_text(tag.get_text())
            if text:
                if tag.name.startswith('h'):
                    level = int(tag.name[1])
                    content.append(f"{'#' * level} {text}")
                else:
                    content.append(text)
    return content

class WebsiteContentExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.browser = None  # 延迟初始化

    async def __aenter__(self):
        self.browser = PlayWrightBrowser()
        await self.browser.start() 
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.browser.close() 
        return False

    @asynccontextmanager
    async def open_page(self, url, timeout=60000):
        async with self.browser.open_page() as page:
            await page.goto(url=url, wait_until="load", timeout=timeout)
            await page.mouse.move(100, 100)
            await page.wait_for_timeout(2000)
            yield page

    async def get_page_content(self, url, timeout=60000) -> list:
        try:
            print(f"正在抓取页面： {url}")

            async with self.open_page(url, timeout) as page:
                content = await page.content()
                soup = BeautifulSoup(content, 'lxml')
                page_content = extract_content_from_soup(soup)
                
                if page_content: 
                    print(f"页面 {url} 内容提取完成")
                    return page_content
                else:  
                    print(f"页面 {url} 内容为空")
                    return None
                        
        except Exception as e:
            print(f"抓取 {url} 时出错: {str(e)}")
            return None

import asyncio
async def main():
    company_websites = [target['url'] for target in parse_target_info(target_info)]
    
    async with WebsiteContentExtractor() as extractor:
        tasks = []
        for website in company_websites:
            tasks.append(asyncio.create_task(extractor.get_page_content(website)))
        
        page_contents = await asyncio.gather(*tasks)
        
        valid_contents = [content for content in page_contents if content is not None]
        
        print(f"\n成功抓取 {len(valid_contents)}/{len(company_websites)} 个页面")
        print("\n内容预览:")
        
        for i, content in enumerate(valid_contents):
            print(f"\n页面 {i+1} 内容:")
            print(content)

if __name__ == "__main__":
    asyncio.run(main())
        

    