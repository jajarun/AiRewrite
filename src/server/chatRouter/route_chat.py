from fastapi import APIRouter
from .chat_request import RewriteRequest
from src.graph.build import build_graph_with_memory
from src.graph.types import State
from fastapi.responses import StreamingResponse
import json
from typing import cast
from langchain_core.messages import AIMessageChunk, ToolMessage, BaseMessage
from langgraph.types import Command


graph = build_graph_with_memory()

chatRouter = APIRouter(
    prefix="/chat",
)

async def _astream_generate(request: RewriteRequest):
    if request.humman_message:
        input = Command(
            resume=request.humman_message
        )
    else:
        input = State(
            url=request.url,
            article_title=request.article_title,
            article_content=request.article_content,
            platforms=request.platforms,
            change_style=request.change_style,
            local=request.local,
            change_theme="",
        )

    async for agent, event_data in graph.astream(
        input,
        config={
            "thread_id": request.thread_id,
        },
        stream_mode=["messages", "updates"],
    ):
        if isinstance(event_data, dict):
            if "__interrupt__" in event_data:
                yield _make_event(
                    "interrupt",
                    {
                        "thread_id": request.thread_id,
                        "id": event_data["__interrupt__"][0].ns[0],
                        "role": "assistant",
                        "content": event_data["__interrupt__"][0].value,
                        "finish_reason": "interrupt",
                    },
                )
            continue
        message_chunk, message_metadata = cast(
            tuple[BaseMessage, dict[str, any]], event_data
        )
        # Handle empty agent tuple gracefully
        agent_name = "unknown"
        if agent and len(agent) > 0:
            agent_name = agent[0].split(":")[0] if ":" in agent[0] else agent[0]
        event_stream_message: dict[str, any] = {
            "thread_id": request.thread_id,
            "agent": agent_name,
            "id": message_chunk.id,
            "role": "assistant",
            "content": message_chunk.content,
        }
        if message_chunk.additional_kwargs.get("reasoning_content"):
            event_stream_message["reasoning_content"] = message_chunk.additional_kwargs[
                "reasoning_content"
            ]
        if message_chunk.response_metadata.get("finish_reason"):
            event_stream_message["finish_reason"] = message_chunk.response_metadata.get(
                "finish_reason"
            )
        if isinstance(message_chunk, ToolMessage):
            # Tool Message - Return the result of the tool call
            event_stream_message["tool_call_id"] = message_chunk.tool_call_id
            yield _make_event("tool_call_result", event_stream_message)
        elif isinstance(message_chunk, AIMessageChunk):
            # AI Message - Raw message tokens
            if message_chunk.tool_calls:
                # AI Message - Tool Call
                event_stream_message["tool_calls"] = message_chunk.tool_calls
                event_stream_message["tool_call_chunks"] = (
                    message_chunk.tool_call_chunks
                )
                yield _make_event("tool_calls", event_stream_message)
            elif message_chunk.tool_call_chunks:
                # AI Message - Tool Call Chunks
                event_stream_message["tool_call_chunks"] = (
                    message_chunk.tool_call_chunks
                )
                yield _make_event("tool_call_chunks", event_stream_message)
            else:
                # AI Message - Raw message tokens
                yield _make_event("message_chunk", event_stream_message)

def _make_event(event_type: str, data: dict[str, any]):
    if data.get("content") == "":
        data.pop("content")
    return f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

@chatRouter.post("/rewrite")
async def rewrite(request: RewriteRequest):
    return StreamingResponse(
        _astream_generate(request),
        media_type="text/event-stream"
    )
    # result = await graph.ainvoke(
    #     State(
    #         url=request.url,
    #         article_title=request.article_title,
    #         article_content=request.article_content,
    #         platforms=request.platforms,
    #         change_style=request.change_style,
    #         local=request.local,
    #         change_theme=request.change_theme,
    #     ),
    #     config={
    #         "thread_id": request.thread_id,
    #     }
    # )
    # res = {}
    # res["interrupt"] = result["__interrupt__"]
    # for platform, rewrite_result in result["rewrite_results"].items():
    #     res[platform] = rewrite_result.content
    # return {"result": res}