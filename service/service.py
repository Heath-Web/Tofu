from utils.Parser import parse_target_info, parse_company_info, original_text
from utils.WebsiteContentExtractor import WebsiteContentExtractor
from constant import LANDING_PAGE_FILE, OUTPUT_FILE_PREFIX
from utils.LLMUtils import gen_personalized_text, summary_website
from bs4 import BeautifulSoup

class Service():
    
    def __init__(self):
        self.personalized_text = {}
        self.company_info = {}
        self.target_info = {}

        self.current_target = []
        pass

    def get_output_file_path(self, company_name:str):
        return f"{OUTPUT_FILE_PREFIX}{company_name}.html"

    def replace_html_content(self, input_file, output_file, replacements):
        with open(input_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        for old_text, new_text in replacements.items():
            html_content = html_content.replace(old_text, new_text)
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        print(f"文件已处理并保存为: {output_file}")
    
    def extract_target_info(self, target_info:dict, extractor:WebsiteContentExtractor):
        company_name = target_info['name']
        if self.target_info.__contains__(company_name):
            return
        
        content = extractor.get_page_content(target_info['url'])
        if content:
            summarized_content = summary_website(content)
            target_info['details'] = summarized_content
            
            self.target_info[company_name] = target_info  

    def gen_personalized_page(self):
        website_extractor = WebsiteContentExtractor()

        with open(LANDING_PAGE_FILE, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'lxml')
        template_page_content = website_extractor.extract_content(soup)

        website_extractor.browser.close()
        
        for target_name in self.current_target:
            if self.personalized_text.__contains__(target_name):
                replacements = dict(zip(original_text, self.personalized_text.get(target_name)))
                self.replace_html_content(input_file=LANDING_PAGE_FILE, replacements=replacements, 
                                          output_file=self.get_output_file_path(target_name))
                continue

            if not self.target_info.__contains__(target_name):
                print(f"无法生成，缺少{target_name}公司信息\n")
                continue

            target_info = self.target_info[target_name]
            summarized_content = target_info['details']
            if summarized_content:
                personalized_text = gen_personalized_text(company_info=self.company_info, 
                                                          target_info=summarized_content,
                                                          template_page_content=template_page_content,
                                                          original_text=original_text)
                self.personalized_text[target_name] = personalized_text
                replacements = dict(zip(original_text, personalized_text))
                self.replace_html_content(input_file=LANDING_PAGE_FILE, replacements=replacements, 
                                          output_file=self.get_output_file_path(target_name))

        return None
    
    def save_playbook(self, playbook:dict):
        clean_target_info = parse_target_info(playbook['Target Info'])
        self.company_info = parse_company_info(playbook['Company Info'])
        self.current_target = []

        website_extractor = WebsiteContentExtractor()
        
        for target in clean_target_info:
            self.current_target.append(target['name'])
            self.extract_target_info(target, website_extractor)

        website_extractor.browser.close()
        print(f'''Saving playbook finished.\nCurrent target company: {self.current_target}\nTotal target in system: {self.target_info.keys()}''')
        return None
      



service_impl = Service()



