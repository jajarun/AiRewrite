from langgraph.graph import StateGraph, START, END
from src.graph.types import State
from src.graph.node import coordinator_node, assgin_worker_write, worker_rewrite_node, human_interrupt_node
from dotenv import load_dotenv
import asyncio
from langgraph.checkpoint.memory import MemorySaver

def _build_base_graph():
    load_dotenv()
    graph = StateGraph(State)
    graph.add_node("coordinator", coordinator_node)
    graph.add_node("worker_rewrite", worker_rewrite_node)
    graph.add_node("human_interrupt", human_interrupt_node)
    graph.add_edge(START, "coordinator")
    graph.add_conditional_edges(
        "coordinator",
        assgin_worker_write,
        ["worker_rewrite"]
    )
    graph.add_edge("worker_rewrite", "human_interrupt")
    return graph

def build_graph_with_memory():
    graph = _build_base_graph()
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)

def build_graph():
    """Build and return the agent workflow graph without memory."""
    # build state graph
    builder = _build_base_graph()
    return builder.compile()


graph = build_graph()

async def main():
    graph = _build_base_graph()
    workflow = graph.compile()
    # workflow.get_graph().draw_mermaid_png(
    #     output_file_path="graph.png",
    # )
    result = await workflow.ainvoke(
        State(
            url="https://blog.respon.ai/zh/docs/difference-between-whatspp-messenger-business-and-api",
            article_title="",
            article_content="",
            platforms=["facebook","instagram","x"],
            change_style="Casual",
            change_theme="",
            local="zh-CN",
        )
    )
    for platform, result in result["rewrite_results"].items():
        print("--------------------------------")
        print(platform)
        print(result.content)
        print("--------------------------------")

if __name__ == "__main__":
    asyncio.run(main())