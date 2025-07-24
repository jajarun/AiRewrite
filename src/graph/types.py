from langgraph.graph import MessagesState
from typing import Literal, Annotated
import operator
from pydantic import BaseModel
from langchain_core.messages import AIMessage
_platfrom_types = Literal["whatsapp", "facebook", "instagram", "x"]
_change_style_types = Literal["Casual", "Friendly", "Professional", "Persuasive"]

class State(MessagesState):
    write_type: Literal["url", "post"]
    url: str
    article_title: str
    article_content: str
    platforms: list[_platfrom_types]
    change_style: _change_style_types
    rewrite_results: Annotated[dict[_platfrom_types, AIMessage], operator.or_]

class workerState(BaseModel):
    platform: _platfrom_types
    article_title: str
    article_content: str
    change_style: _change_style_types