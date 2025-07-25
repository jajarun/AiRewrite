from src.graph.types import State
from langgraph.types import RunnableConfig, Send,interrupt,Command
from src.llms.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from newspaper import Article
from src.prompts.template import apply_prompt_template
from src.graph.types import workerState
from datetime import datetime
from src.graph.tools import analyze_feedback
from typing import Literal

def coordinator_node(state: State, config: RunnableConfig):
    if not state["url"] and not state["article_content"]:
        raise ValueError("url or article_content is required")
    if state["url"] and not state["article_content"]:
        article = Article(state["url"])
        article.download()
        article.parse()
        return State(
            article_title=article.title,
            article_content=article.text,
        )
    
def worker_rewrite_node(state: workerState, config: RunnableConfig) -> Command[Literal["human_interrupt"]]:
    print("platform:"+state.platform+" start time:"+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    llm = get_llm()
    input = apply_prompt_template("rewrite", state)
    input += [
        HumanMessage(content=f"Rewrite the article: {state.article_content}"),
    ]
    if state.change_theme:
        input += [
            HumanMessage(content=f"Change the theme of the article: {state.change_theme}"),
        ]
    result = llm.invoke(input=input)
    #打印当前时间
    print("platform:"+state.platform+" end time:"+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return Command(
        goto="human_interrupt",
        update={
            "rewrite_results": {
                state.platform: result,
            }
        }
    )

def human_interrupt_node(state: State, config: RunnableConfig) -> Command[Literal["coordinator","__end__"]]:
    feedback = interrupt(
        "检查文章是否需要修改，如果需要修改，请告诉我哪些平台需要调整，并且可以告诉我你的修改想法，否则返回空字符串"
    )
    if str(feedback) == "":
        return Command(
            goto="__end__",
        )
    llm = get_llm()
    input = [
        SystemMessage(content="你是一个文章修改专家，用户要对你提炼出来的文章进行修改，从用户的反馈提炼出需要修改的社媒平台和修改建议"),
        HumanMessage(content=str(feedback)),
    ]
    result = llm.bind_tools([analyze_feedback]).invoke(input=input)
    if result.tool_calls:
        return Command(
            goto="coordinator",
            update={
                "platforms": result.tool_calls[0]["args"]["need_change_platforms"],
                "change_theme": result.tool_calls[0]["args"]["change_theme_or_suggestion"],
            }
        )
    else:
        return Command(
            goto="__end__",
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
            local=state["local"],
            change_theme=state["change_theme"],
        )) for platform in state["platforms"]
    ]