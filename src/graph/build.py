from langgraph.graph import StateGraph, START, END
from src.graph.types import State
from src.graph.node import coordinator_node, rewrite_node

def _build_base_graph():
    graph = StateGraph(State)
    graph.add_node("coordinator", coordinator_node)
    graph.add_node("rewrite", rewrite_node)
    graph.add_edge(START, "coordinator")
    graph.add_edge("coordinator", "rewrite")
    graph.add_edge("rewrite", END)
    return graph

if __name__ == "__main__":
    graph = _build_base_graph()
    workflow = graph.compile()
    workflow.get_graph().draw_mermaid_png(
        output_file_path="graph.png",
    )
    # result = workflow.invoke(
    #     State(
    #         url="https://blog.respon.ai/zh/docs/difference-between-whatspp-messenger-business-and-api",
    #         article_title="",
    #         article_content="",
    #     )
    # )
    # print(result)