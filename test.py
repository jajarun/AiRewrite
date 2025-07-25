from src.prompts.template import apply_prompt_template
from src.graph.types import workerState
from src.llms.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from src.graph.tools import analyze_feedback
from dotenv import load_dotenv

load_dotenv()
llm = get_llm()
input = [
    SystemMessage(content="你是一个文章修改专家，用户要对你提炼出来的文章进行修改，从用户的反馈提炼出需要修改的社媒平台和修改建议"),
    HumanMessage(content="把Facebok和Instagam修改为专业风格"),
]
result = llm.bind_tools([analyze_feedback]).invoke(input=input)
print(result)