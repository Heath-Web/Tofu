from bs4 import BeautifulSoup
import re
from utils.Parser import parse_target_info, target_info
from utils.PlayWrightBrowser import PlayWrightBrowser

class WebsiteContentExtractor:
    def __init__(self):
        self.headers =  {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.browser = PlayWrightBrowser()

    def extract_content(self, soup) -> list:
        content = []

        for script in soup(['script', 'style', 'noscript', 'iframe']):
            script.decompose()

        desc = soup.find('meta', attrs={'name': 'description'})
        if desc :
            content.append(f"Describtion: {desc['content']}")
        
        # main_content = soup.find(['article', 'main', 'div'], class_=re.compile(r'content|main|post|article', re.I))
        main_content  = soup.find('body')
        if main_content:
            for tag in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
                text = self.clean_text(tag.get_text())
                if text:
                    if tag.name.startswith('h'):
                        level = int(tag.name[1])
                        content.append(f"{'#' * level} {text}")
                    else:
                        content.append(text)
        return content
    
    def clean_text(self, text):
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def get_page_content(self, url, timeout:int=8000) -> list:
        try:
            print(f"正在抓取页面： {url}")

            page = self.browser.new_page()
            page.goto(url=url)
            page.mouse.move(100, 100)
            page.wait_for_timeout(timeout)
            content = page.content()

            soup = BeautifulSoup(content, 'lxml')
            
            page_content = self.extract_content(soup)
            page.close()

            if page_content: return page_content
            else:  
                print("页面内容为空")
                return None
                        
        except Exception as e:
            print(f"抓取 {url} 时出错: {str(e)}")
            return None


if __name__ == "__main__":

    # company_websites = ["https://www.morrisathome.com/about-us"]
    company_websites = []
    for target in parse_target_info(target_info):
        company_websites.append(target['url'])

    extractor = WebsiteContentExtractor()
    page_contents = []
    for website in company_websites:
        content = extractor.get_page_content(website)
        if content: 
            page_contents.append(content)
    extractor.browser.close()

    print("\n内容预览:")
    for page in extractor.content_text:
        print(f"\nURL: {page['url']}")
        print("提取的内容:")


        

    