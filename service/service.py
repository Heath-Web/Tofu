from utils.Parser import parse_target_info, parse_company_info, original_text
from utils.WebsiteContentExtractor import WebsiteContentExtractor,extract_content_from_soup
from constant import LANDING_PAGE_FILE, OUTPUT_FILE_PREFIX
from utils.LLMUtils import gen_personalized_text, summary_website
from bs4 import BeautifulSoup
import aiofiles
import asyncio
import os

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
            return
        
        try:
            content = await extractor.get_page_content(target_info['url'])
            if content:
                summarized_content = await summary_website(content)
                target_info['details'] = summarized_content
                self.target_info[company_name] = target_info  
                return True
        except Exception as e:
            print(f"Error when extracting {company_name}: {str(e)}")

        return False

    async def gen_single_personalized_page(self, target_name:str):
        if self.personalized_text.__contains__(target_name):
            replacements = dict(zip(original_text, self.personalized_text.get(target_name)))
            await self.replace_html_content(
                input_file=LANDING_PAGE_FILE, 
                replacements=replacements, 
                output_file=self.get_output_file_path(target_name)
                )
            return True

        if not self.target_info.__contains__(target_name):
            print(f"无法生成，缺少{target_name}公司信息\n")
            return False

        target_info = self.target_info[target_name]
        summarized_content = target_info['details']
        if summarized_content:
            personalized_text = await gen_personalized_text(
                company_info = self.company_info, 
                target_info = summarized_content,
                template_page_content = self.template_page_content,
                original_text=original_text)
            
            self.personalized_text[target_name] = personalized_text
            replacements = dict(zip(original_text, personalized_text))
            await self.replace_html_content(
                input_file=LANDING_PAGE_FILE,
                replacements=replacements, 
                output_file=self.get_output_file_path(target_name))

    async def gen_personalized_page(self):
        tasks = [self.gen_personalized_page(target_name) for target_name in self.current_target]
        await asyncio.gather(*tasks, return_exceptions=True)
        return None
    
    async def save_playbook(self, playbook: dict):
        clean_target_info = parse_target_info(playbook['Target Info'])
        self.company_info = parse_company_info(playbook['Company Info'])
        self.current_target = [target['name'] for target in clean_target_info]

        async with WebsiteContentExtractor() as extractor:
            tasks = [self.extract_target_info(target, extractor) for target in clean_target_info ]
            await asyncio.gather(*tasks, return_exceptions=True)

        print(f'''Saving playbook finished.\nCurrent {len(self.current_target)} target company: {self.current_target}\nTotal {len(self.target_info.keys())} target in system: {self.target_info.keys()}''')
        return True
      



service_impl = Service()



