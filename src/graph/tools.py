from langchain_core.tools import tool
from src.graph.types import State

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