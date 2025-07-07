from langchain_openai import ChatOpenAI
from constant import DEEPSEEK_API_KEY, OPENAI_API_KEY
import asyncio

class LLMManager:
    _models: dict
    _lock: asyncio.Lock 

    def __init__(self):
        self._models = {}
        self._lock = asyncio.Lock()

    async def get_json_llm_model(self, model_name: str = "deepseek-chat") -> ChatOpenAI:
        if model_name in self._models:
            return self._models[model_name]
        
        async with self._lock:
            if model_name in self._models:
                return self._models[model_name]
            
            if model_name in ["deepseek-chat", "deepseek-reasoner"]:
                model = ChatOpenAI(
                    model=model_name,
                    api_key=DEEPSEEK_API_KEY,
                    base_url="https://api.deepseek.com",
                    model_kwargs={"response_format": {"type": "json_object"}}
                )
            else:
                model = ChatOpenAI(
                    model=model_name,
                    api_key=OPENAI_API_KEY,
                    model_kwargs={"response_format": {"type": "json_object"}}
                )
            
            self._models[model_name] = model
            return model

llm_manager_impl = LLMManager()
