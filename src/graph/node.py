from src.graph.types import State
from langgraph.types import RunnableConfig, Send
from src.llms.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from newspaper import Article
from src.prompts.template import apply_prompt_template
from src.graph.types import workerState
from datetime import datetime

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
    
async def worker_rewrite_node(state: workerState, config: RunnableConfig) -> State:
    print("platform:"+state.platform+" start time:"+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    llm = get_llm()
    input = apply_prompt_template("rewrite", state)
    input += [
        HumanMessage(content=f"Rewrite the article: {state.article_content}"),
    ]
    result = await llm.ainvoke(input=input)
    #打印当前时间
    print("platform:"+state.platform+" end time:"+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return State(
        rewrite_results={
            state.platform: result,
        }
    )
    
def assgin_worker_write(state: State, config: RunnableConfig):
    if not state["article_title"] and not state["article_content"]:
        raise ValueError("article_title and article_content are required")
    return [
        Send("worker_rewrite",workerState(
            platform=platform,
            article_title=state["article_title"],
            article_content=state["article_content"],
            change_style=state["change_style"],
        )) for platform in state["platforms"]
    ]
    # llm = get_llm()
    # input = apply_prompt_template("rewrite", workerState(
    #     platform="facebook",
    #     article_title=state["article_title"],
    #     article_content=state["article_content"],
    #     change_style="Casual",
    # ))
    # input += [
    #     HumanMessage(content=f"Rewrite the article: {state['article_content']}"),
    # ]
    # result = llm.invoke(
    #     input=input
    # )
    # return State(
    #     messages=[result]
    # )