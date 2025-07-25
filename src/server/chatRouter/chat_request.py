from pydantic import BaseModel, Field
from src.graph.types import _platfrom_types, _change_style_types

class RewriteRequest(BaseModel):
    thread_id: str = Field(default="")
    url: str = Field(default="")
    article_title: str = Field(default="")
    article_content: str = Field(default="")
    platforms: list[_platfrom_types] = Field(default=[])
    change_style: _change_style_types = Field(default="Casual")
    local: str = Field(default="zh-CN")
    humman_message: str = Field(default="")