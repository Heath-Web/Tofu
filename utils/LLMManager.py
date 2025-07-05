
from langchain_openai import ChatOpenAI
from constant import OPENAI_API_KEY

class LLMManager:

    llm: ChatOpenAI 

    def __init__(self):
        self.llm = None  

    def get_json_llm_model(self, modle:str="deepseek-chat") -> ChatOpenAI:
        if self.llm:
            return self.llm

        self.llm = ChatOpenAI(
            model="deepseek-chat",
            api_key= OPENAI_API_KEY,
            base_url="https://api.deepseek.com",
            model_kwargs={
                "response_format": {"type": "json_object"}  
            }
        )

        return self.llm


llm_manager_impl = LLMManager()    

