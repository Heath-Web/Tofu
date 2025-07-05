from utils.LLMManager import llm_manager_impl 
from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json

class CompanyProfile(BaseModel):
    company_name: str = Field(description="Company Name")
    official_overview: str = Field(description="Official Overview")
    product_overview: str = Field(description="Product Overview")
    company_description: str = Field(description="Company Description")

def summary_website(website_content: str) -> dict:
    prompt_template = ChatPromptTemplate.from_template("""
    Below is the plain text information I extracted from the company's official website. 
    In this content, # indicates a main heading, ## indicates a subheading, and text without any # is considered regular content.

    Website content: {website_content}
                                                
    Considering several aspects mentioned in this format instruction: {format_instruction} 
                                                       
    Please extract and summarize the company's profile based on the Website content and the format instruction.
    Return ONLY valid JSON in the format instruction.
    """)
    output_parser = JsonOutputParser(pydantic_object=CompanyProfile)
    llm = llm_manager_impl.get_json_llm_model()

    chain = prompt_template | llm | output_parser 
    
    result = chain.invoke({"website_content":website_content, 
                           "format_instruction":output_parser.get_format_instructions()})
    print(f"Summary of the Website：\n{result}")
    return result

def gen_personalized_text(company_info:dict, target_info:dict, template_page_content:list, original_text:list):

    system_prompt = SystemMessagePromptTemplate.from_template("""
    You are a marketing assistant helping personalize landing pages for different target companies.
    And you are working at a company called Stampli.
    Stampli Overview: {company_info}
    
    Target Company Info: {target_info}

    Template landing page: {template_page_content}                                                          
    """)

    human_prompt = HumanMessagePromptTemplate.from_template("""
    Please write {text_count} personalized text to replace the following original texts in the template landing page:
    {original_text}

    The newly generated personalized text should be :
    1. Tailored to appeal to the target company’s name, industry, goals and products.
    2. Staying aligned with Stampli’s tone and core messaging.
    3. Naturally integrate into the template landing page rather than a bunch of randomly assembled paragraphs.
    4. The word count should be similar to the original text (within ±20% word count).
        
    Return an json array list that only contains exactly {text_count} strings in the same order as the original texts, like ["text1", "text2", ..., "textN"]
    """)

    prompt_template = ChatPromptTemplate.from_messages(
        [system_prompt, human_prompt]
    )

    output_parser = JsonOutputParser()
    llm = llm_manager_impl.get_json_llm_model()
    chain = prompt_template | llm | output_parser
    res = chain.invoke({"company_info":company_info,
                        "target_info":target_info,
                        "template_page_content": template_page_content,
                        "original_text": original_text,
                        "text_count": len(original_text)})
        
    print(f"公司名称：  {target_info["company_name"]} \n替换文字： {res} \n ================================================== ")
    if res.__contains__("personalized_texts"):
        return res["personalized_texts"]
    else:
        return res