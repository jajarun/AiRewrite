from fastapi import APIRouter
from .chat_request import RewriteRequest
from src.graph.build import build_graph_with_memory
from src.graph.types import State

graph = build_graph_with_memory()

chatRouter = APIRouter(
    prefix="/chat",
)

@chatRouter.post("/rewrite")
async def rewrite(request: RewriteRequest):
    result = await graph.ainvoke(
        State(
            url=request.url,
            article_title=request.article_title,
            article_content=request.article_content,
            platforms=request.platforms,
            change_style=request.change_style,
            local=request.local,
            change_theme=request.change_theme,
        ),
        config={
            "thread_id": request.thread_id,
        }
    )
    res = {}
    res["interrupt"] = result["__interrupt__"]
    for platform, rewrite_result in result["rewrite_results"].items():
        res[platform] = rewrite_result.content
    return {"result": res}