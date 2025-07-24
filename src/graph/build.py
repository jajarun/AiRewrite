from langgraph.graph import StateGraph, START, END
from src.graph.types import State
from src.graph.node import coordinator_node, assgin_worker_write, worker_rewrite_node
import asyncio
def _build_base_graph():
    graph = StateGraph(State)
    graph.add_node("coordinator", coordinator_node)
    graph.add_node("worker_rewrite", worker_rewrite_node)
    graph.add_edge(START, "coordinator")
    graph.add_conditional_edges(
        "coordinator",
        assgin_worker_write,
        ["worker_rewrite"]
    )
    graph.add_edge("worker_rewrite", END)
    return graph

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
        )
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())