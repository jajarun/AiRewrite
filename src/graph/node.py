from src.graph.types import State
from langgraph.types import RunnableConfig
from src.llms.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from newspaper import Article

def coordinator_node(state: State, config: RunnableConfig):
    if not state["url"] and not state["article_content"]:
        raise ValueError("url or article_content is required")
    if state["url"]:
        article = Article(state["url"])
        article.download()
        article.parse()
        return State(
            article_title=article.title,
            article_content=article.text,
        )
    
def rewrite_node(state: State, config: RunnableConfig) -> State:
    if not state["article_title"] and not state["article_content"]:
        raise ValueError("article_title and article_content are required")
    llm = get_llm()
    result = llm.invoke(
        input=[
            SystemMessage(content="You are a helpful assistant that can rewrite articles."),
            HumanMessage(content=f"Rewrite the article: {state['article_content']}"),
        ]
    )
    return State(
        messages=[result]
    )