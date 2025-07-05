from utils.Parser import parse_target_info, parse_company_info, original_text
from utils.WebsiteContentExtractor import WebsiteContentExtractor
from constant import LANDING_PAGE_FILE, OUTPUT_FILE_PREFIX
from utils.LLMUtils import gen_personalized_text, summary_website
from bs4 import BeautifulSoup

class Service():
    
    def __init__(self):
        self.personalized_text = {}
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

    def gen_personalized_page(self, playbook:dict):
        clean_target_info = parse_target_info(playbook['Target Info'])
        clean_company_info = parse_company_info(playbook['Company Info'])

        website_extractor = WebsiteContentExtractor()

        with open(LANDING_PAGE_FILE, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'lxml')

        template_page_content = website_extractor.extract_content(soup)
        
        for target in clean_target_info:
            company_name = target['name']
            if self.personalized_text.__contains__(company_name):
                replacements = dict(zip(original_text, self.personalized_text.get(company_name)))
                self.replace_html_content(input_file=LANDING_PAGE_FILE, replacements=replacements, 
                                          output_file=self.get_output_file_path(company_name))
                continue 

            content = website_extractor.get_page_content(target['url'])
            if content:
                summarized_content = summary_website(content)
                target['Details'] = summarized_content
                personalized_text = gen_personalized_text(company_info=clean_company_info, 
                                                               target_info=summarized_content,
                                                               template_page_content=template_page_content,
                                                               original_text=original_text)
                self.personalized_text[company_name] = personalized_text
                replacements = dict(zip(original_text, personalized_text))
                self.replace_html_content(input_file=LANDING_PAGE_FILE, replacements=replacements, 
                                          output_file=self.get_output_file_path(company_name))

        website_extractor.browser.close()

        return None


service_impl = Service()



