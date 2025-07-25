from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
import os
_llm_cache: dict[str, BaseChatModel] = {}

def get_llm(model_name: str = "deepseek") -> BaseChatModel:
    if model_name in _llm_cache:
        return _llm_cache[model_name]
    
    _llm_cache[model_name] = ChatOpenAI(
        model="deepseek-v3",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0,
    )
    return _llm_cache[model_name]