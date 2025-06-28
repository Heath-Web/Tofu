from utils.Parser import parse_target_info, parse_company_info, original_text
from utils.WebsiteContentExtractor import WebsiteContentExtractor, summary_website
from openai import OpenAI
from pathlib import Path
from playwright.sync_api import sync_playwright
from constant import LANDING_PAGE_FILE, OUTPUT_FILE_PREFIX,OPENAI_API_KEY
import json


class Service():
    
    def __init__(self):
        self.personalized_text = {}
        pass

    def get_output_file_path(self, company_name:str):
        return f"{output_file_prefix}{company_name}.html"

    def gen_personalized_text(self, company_info, target_info, template_page_content, original_text, client):
        prompt = f'''You are a marketing assistant helping personalize landing pages for different target companies.
        And you are working at a company called Stampli.

        Stampli Overview: {company_info}

        Target Company Info: {target_info}

        Here is the plain text information I extracted from the template landing page: {template_page_content} .
        In this content, # indicates a main heading, ## indicates a subheading, and text without any # is considered regular content.

        Please write 4 personalized text to replace the flowing 4 original text from the template langding page:
        {original_text}

        The newly generated personalized text should be :
        1. Tailored to appeal to the target company’s industry, keywords, goals or even products.
        2. Staying aligned with Stampli’s tone and core.
        3. Naturally integrate into the template landing page rather than a bunch of randomly assembled paragraphs.
        4. The word count should be similar to the original text.
        
        Finally, The format of your output should be a list like ["","","",""] without any other instruction.
        '''

        response = client.responses.create(
            model = "gpt-4o",
            input = prompt
        )
        res = response.output_text
        print(f"公司名称：  {target_info["Company Name"]} \n替换文字： {res} \n ================================================== ")
        return json.loads(res)

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
        template_url = "https://get.stampli.com/cfo-recession-toolkit-2022"
        template_page_content = website_extractor.get_page_content(template_url, timeout=2000)

        client = OpenAI(api_key=OPENAI_API_KEY)

        for target in clean_target_info:
            company_name = target['name']
            if self.personalized_text.__contains__(company_name):
                replacements = dict(zip(original_text, self.personalized_text.get(company_name)))
                self.replace_html_content(input_file=landing_page_file, replacements=replacements, 
                                          output_file=self.get_output_file_path(company_name))
                continue 

            content = website_extractor.get_page_content(target['url'])
            if content:
                summarized_content = summary_website(client, content)
                target['Details'] = summarized_content
                personalized_text = self.gen_personalized_text(company_info=clean_company_info, 
                                                               target_info=summarized_content,
                                                               template_page_content=template_page_content,
                                                               original_text=original_text,
                                                               client=client)
                self.personalized_text[company_name] = personalized_text
                replacements = dict(zip(original_text, personalized_text))
                self.replace_html_content(input_file=landing_page_file, replacements=replacements, 
                                          output_file=self.get_output_file_path(company_name))

        website_extractor.browser.close()

        return None


service_impl = Service()



