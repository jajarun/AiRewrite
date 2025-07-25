from pydantic import BaseModel, Field

class RewriteRequest(BaseModel):
    thread_id: str = Field(default="")
    url: str = Field(default="")
    article_title: str = Field(default="")
    article_content: str = Field(default="")
    platforms: list[str] = Field(default=[])
    change_style: str = Field(default="Casual")
    local: str = Field(default="zh-CN")
    change_theme: str = Field(default="")