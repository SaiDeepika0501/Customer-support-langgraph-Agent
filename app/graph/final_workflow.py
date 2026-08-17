from langgraph.graph import StateGraph, START, END

from app.graph.final_state import FinalState
from app.graph.final_nodes import (
    memory_node,
    planner_node,
    rag_node,
    tool_node,
    writer_node,
    reflect_node,
    revise_node,
    route_after_planner,
    route_after_rag,
    route_after_reflection,
)

builder = StateGraph(FinalState)

builder.add_node("memory", memory_node)
builder.add_node("planner", planner_node)
builder.add_node("rag", rag_node)
builder.add_node("tool", tool_node)
builder.add_node("writer", writer_node)
builder.add_node("reflect", reflect_node)
builder.add_node("revise", revise_node)

builder.add_edge(START, "memory")
builder.add_edge("memory", "planner")

builder.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "rag": "rag",
        "tool": "tool",
        "writer": "writer",
    },
)

builder.add_conditional_edges(
    "rag",
    route_after_rag,
    {
        "tool": "tool",
        "writer": "writer",
    },
)

builder.add_edge("tool", "writer")
builder.add_edge("writer", "reflect")

builder.add_conditional_edges(
    "reflect",
    route_after_reflection,
    {
        "revise": "revise",
        "end": END,
    },
)

builder.add_edge("revise", END)

graph = builder.compile()