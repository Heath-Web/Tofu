from utils.Parser import parse_target_info, parse_company_info, original_text
from utils.WebsiteContentExtractor import WebsiteContentExtractor,extract_content_from_soup
from constant import LANDING_PAGE_FILE, OUTPUT_FILE_PREFIX
from utils.LLMUtils import gen_personalized_text, summary_website, analyze_target_insights
from bs4 import BeautifulSoup
import aiofiles
import asyncio
import os
import threading
from concurrent.futures import ThreadPoolExecutor

class Service():
    
    def __init__(self):
        self.personalized_text = {}
        self.company_info = {}
        self.target_info = {}
        self.current_target = []

        with open(LANDING_PAGE_FILE, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'lxml')
        self.template_page_content = extract_content_from_soup(soup)

        self.backend_loop = None 
        threading.Thread(target=self.start_event_loop_thread, daemon=True).start()

    def get_output_file_path(self, company_name:str):
        return f"{OUTPUT_FILE_PREFIX}{company_name}.html"

    async def replace_html_content(self, input_file: str, output_file: str, replacements: dict):
        try:
            async with aiofiles.open(input_file, 'r', encoding='utf-8') as file:
                html_content = await file.read()
            
            for old_text, new_text in replacements.items():
                html_content = html_content.replace(old_text, new_text)
            
            async with aiofiles.open(output_file, 'w', encoding='utf-8') as file:
                await file.write(html_content)
            
            print(f"Personalized Landing Page Saved in: {output_file}")
            return True
        except Exception as e:
            print(f"Error when saving file {output_file}: {e}")
            return False
    
    async def extract_target_info(self, target_info:dict, extractor:WebsiteContentExtractor):
        company_name = target_info['name']
        if self.target_info.__contains__(company_name):
            return True
        
        try:
            content = await extractor.get_page_content(target_info['url'])
            if content:
                summarized_content = await summary_website(content)
                target_info['details'] = summarized_content
                target_insight = await analyze_target_insights(content)
                target_info['insight'] = target_insight
                self.target_info[company_name] = target_info  
                return True
        except Exception as e:
            print(f"Error when extracting {company_name}: {str(e)}")

        return False

    async def gen_single_personalized_page(self, target_info:dict):
        target_name = target_info['name']
        if self.personalized_text.__contains__(target_name):
            replacements = dict(zip(original_text, self.personalized_text.get(target_name)))
            await self.replace_html_content(
                input_file=LANDING_PAGE_FILE, 
                replacements=replacements, 
                output_file=self.get_output_file_path(target_name)
                )
            return True

        if not self.target_info.__contains__(target_name):
            print(f"无法生成，缺少{target_name}公司信息. 正在重试\n")
            async with WebsiteContentExtractor() as extractor:
                res =  await self.extract_target_info(target_info, extractor)
                if res:
                    target_info = self.target_info[target_name]
                else: return False

        target_info = self.target_info[target_name]
        summarized_content = target_info['details']
        target_insight = target_info['insight']
        if summarized_content and target_insight:
            personalized_text = await gen_personalized_text(
                company_info = self.company_info, 
                target_info = {"details": summarized_content, "insight": target_insight},
                template_page_content = self.template_page_content,
                original_text=original_text)
            
            self.personalized_text[target_name] = personalized_text
            replacements = dict(zip(original_text, personalized_text))
            await self.replace_html_content(
                input_file=LANDING_PAGE_FILE,
                replacements=replacements, 
                output_file=self.get_output_file_path(target_name))

    async def gen_personalized_page(self):
        tasks = [self.gen_single_personalized_page(t) for t in self.current_target]
        await asyncio.gather(*tasks, return_exceptions=True)
        return None
    
    def start_event_loop_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.backend_loop = loop
        loop.run_forever()

    async def save_playbook(self, playbook: dict):
        clean_target_info = parse_target_info(playbook['Target Info'])
        self.company_info = parse_company_info(playbook['Company Info'])
        self.current_target = clean_target_info

        async def gather_tasks():
            async with WebsiteContentExtractor() as extractor:
                tasks = [self.extract_target_info(target, extractor) for target in clean_target_info]
                await asyncio.gather(*tasks,return_exceptions=True)
            print(f'''------------------------\nSaving playbook finished.\nCurrent {len(self.current_target)} target company: {[t['name'] for t in self.current_target]}\nTotal {len(self.target_info.keys())} target in system: {self.target_info.keys()}''')

        asyncio.run_coroutine_threadsafe(gather_tasks(), self.backend_loop)
            
        return True

service_impl = Service()



