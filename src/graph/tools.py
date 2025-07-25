from langchain_core.tools import tool
from src.graph.types import State, _platfrom_types

@tool
def fetch_article_by_url(url: str, article_title: str, article_content: str) -> State:
    """
    Fetch an article from a given URL.
    """
    print(f"Fetching article from {url}")
    print(f"Article title: {article_title}")
    print(f"Article content: {article_content}")
    return State(
        article_title=article_title,
        article_content=article_content,
    )

@tool
def analyze_feedback(need_change_platforms: list[_platfrom_types], change_theme_or_suggestion: str):
    """
    分析用户的反馈并从中提取出需要修改的社媒平台和修改建议
    """
    # print(f"Need change platforms: {need_change_platforms}")
    # print(f"Change theme or suggestion: {change_theme_or_suggestion}")
    return