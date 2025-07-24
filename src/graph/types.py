from langgraph.graph import MessagesState
from typing import Literal, Annotated
import operator
from pydantic import BaseModel

_platfrom_types = Literal["whatsapp", "facebook", "instagram", "x"]

class State(MessagesState):
    write_type: Literal["url", "post"]
    url: str
    article_title: str
    article_content: str
    platforms: list[_platfrom_types]
    change_style: Literal["short", "long"]
    change_target: Literal["all", "specific"]
    change_topic_or_product: Literal["all", "specific"]
    rewrite_results: Annotated[dict[str, any], operator.or_]

class workerState(BaseModel):
    platform: _platfrom_types
    article_title: str
    article_content: str
    change_style: Literal["Casual", "Friendly", "Professional", "Persuasive"]
    # change_target: Literal["all", "specific"]
    # change_topic_or_product: Literal["all", "specific"]