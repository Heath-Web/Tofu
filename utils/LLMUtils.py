from utils.LLMManager import llm_manager_impl 
from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import asyncio
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type, RetryError

class CompanyProfile(BaseModel):
    company_name: str = Field(description="Company Name")
    official_overview: str = Field(description="Official Overview")
    product_overview: str = Field(description="Product Overview")
    company_description: str = Field(description="Company Description")

class TargetInight(BaseModel):
    company_name: str = Field(description="Company Name")
    pain_points: str = Field(description="List of 3-5 key pain points the company likely faces")
    value_proposition: str = Field(description="List of 3-5 key value proposition the company likely faces")

SUMMARY_SEMAPHORE = asyncio.Semaphore(5)

async def summary_website(website_content: str) -> dict:
    async with SUMMARY_SEMAPHORE:
        prompt_template = ChatPromptTemplate.from_template("""
        Below is the plain text information I extracted from the company's official website. 
        In this content, # indicates a main heading, ## indicates a subheading, and text without any # is considered regular content.

        Website content: {website_content}
                                                    
        Considering several aspects mentioned in this format instruction: {format_instruction} 
                                                        
        Please extract and summarize the company's profile based on the Website content and the format instruction.
        Return ONLY valid JSON in the format instruction.
        """)
        output_parser = JsonOutputParser(pydantic_object=CompanyProfile)
        llm = await llm_manager_impl.get_json_llm_model(model_name="deepseek-chat")

        chain = prompt_template | llm | output_parser 
        
        result = await chain.ainvoke({
            "website_content":website_content, 
            "format_instruction":output_parser.get_format_instructions()
        })
        print(f"Summary of the Website：\n{result}")
        return result


ANALYZE_INSIGHT_SEMAPHORE = asyncio.Semaphore(5)
async def analyze_target_insights(website_content: str) -> dict:
    async with ANALYZE_INSIGHT_SEMAPHORE:
        prompt_template = ChatPromptTemplate.from_template("""
        You are a marketing assistant helping analyze target company's insights.
        Below is the plain text information I extracted from the company's official website. 
        In this content, # indicates a main heading, ## indicates a subheading, and text without any # is considered regular content.

        Website content: {website_content}
                                                    
        Considering several aspects mentioned in this format instruction: {format_instruction} 
                                                        
        Generate: 
        1. 3-5 key pain points the company likely faces
        2. 3-5 key value propositions the company likely faces
                                                           
        Return ONLY valid JSON in the format instruction.
        """)
        output_parser = JsonOutputParser(pydantic_object=TargetInight)
        llm = await llm_manager_impl.get_json_llm_model(model_name="deepseek-chat")

        chain = prompt_template | llm | output_parser 
        
        result = await chain.ainvoke({
            "website_content":website_content, 
            "format_instruction":output_parser.get_format_instructions()
        })
        print(f"Insights of the Website：\n{result}")
        return result


GEN_TEXT_SEMAPHORE = asyncio.Semaphore(5)

async def gen_personalized_text(company_info:dict, target_info:dict, template_page_content:list, original_text:list):
    async with GEN_TEXT_SEMAPHORE: 
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
        1. Tailored to appeal to the target company’s overview, pain points and value proposition.
        2. Staying aligned with Stampli’s tone and core messaging.
        3. Naturally integrate into the template landing page rather than a bunch of randomly assembled paragraphs.
        4. The word count should be similar to the original text (within ±20% word count).
            
        Return an json array list that only contains exactly {text_count} strings in the same order as the original texts, like ["text1", "text2", ..., "textN"]
        """)

        prompt_template = ChatPromptTemplate.from_messages(
            [system_prompt, human_prompt]
        )

        output_parser = JsonOutputParser()
        llm = await llm_manager_impl.get_json_llm_model(model_name="deepseek-chat")
        chain = prompt_template | llm | output_parser
        res = await chain.ainvoke({
            "company_info":company_info,
            "target_info":target_info,
            "template_page_content": template_page_content,
            "original_text": original_text,
            "text_count": len(original_text)
        })
            
        print(f"Compant Name：{target_info["company_name"]} \nPersonalized Text： {res} \n ================================================== ")
        if isinstance(res, dict) and "personalized_texts" in res:
            return res["personalized_texts"]
        elif isinstance(res, list):
            return res
        else:
            print(f"意外返回格式: {type(res)} - {res}")
            return []
    
from utils.Parser import parse_company_info, company_info, original_text
import asyncio
async def main():
    target_info = {
    'company_name': 'YMCA', 
    'official_overview': 'The YMCA is the leading nonprofit committed to strengthening individuals and communities across the country. At the Y, we’re here to help you find your “why” – your greater sense of purpose – by connecting you with opportunities to improve your health, support young people, make new friends and contribute to a stronger, more cohesive community for all.', 
    'product_overview': 'Our programs and services are focused on our primary areas of impact that help people achieve their goals and strengthen communities. With our breadth of offerings, you can find the support you need and help your neighborhood thrive.', 
    'company_description': 'Each year, we strive to transform lives and strengthen communities worldwide. Across the U.S., our Ys reach millions of people in 10,000 communities. We provide millions of pounds of groceries to families each month. Our day and overnight camps empowered kids by building lifelong skills, confidence and friendships. Ys reach millions of people across 50 states, plus the District of Columbia and Puerto Rico.'
    } 
    template_content = ['Describtion: This G2 Report download is a scorecard for all the players in the AP Automation market and how they compare to one another. G2 scores products based on reviews gathered from its community of 1.28+ million users, as well as data aggregated from online sources and social networks.', 
            '# Preparing for a recession toolkit', 
            'A recession readiness toolkit to guide CFOs and finance leaders through recessions and periods of economic instability.', 
            '## "2022 CFO Recession Toolkit"', '### Recession readiness toolkit to minimize the impact of an economic downturn.', 
            'Managers are dealing with a number of economic issues, and some analysts believe that the US is headed toward a recession.To respond to the challenge, take action to address a possible recession now, so that you’re ready to minimize the impact and outperform competitors who are not proactive.', 
            'Download our "2022 CFO Recession Toolkit" to receive actionable recession readiness insights on:', 
            '## Get your 2022 CFO Recession Toolkit', 
            "Download the toolkit here (it's free!).", 
            "By submitting your information, you acknowledge that your data will be handled in accordance with Stampli's Terms of Service and Privacy Policy, and you authorize Stampli to send you updates about Stampli products, services, and events."]
    clean_company_info = parse_company_info(company_info=company_info)
    
    # 异步调用
    personalized_texts = await gen_personalized_text(
        clean_company_info,
        target_info,
        template_content,
        original_text
    )
    
    print("生成的个性化文本:")
    for i, text in enumerate(personalized_texts):
        print(f"{i+1}. {text}")

if __name__ == "__main__":
    asyncio.run(main())