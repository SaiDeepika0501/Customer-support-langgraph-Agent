from langgraph.graph import StateGraph, START, END

from graph.state import SupportState
from graph.tool_nodes import (
    planner,
    order_status_node,
    refund_node,
    writer,
    route_after_planner,
    route_after_order,
)

builder = StateGraph(SupportState)

builder.add_node("planner", planner)
builder.add_node("order_status", order_status_node)
builder.add_node("refund", refund_node)
builder.add_node("writer", writer)

builder.add_edge(START, "planner")

builder.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "order_status": "order_status",
        "refund": "refund",
        "writer": "writer",
    },
)

builder.add_conditional_edges(
    "order_status",
    route_after_order,
    {
        "refund": "refund",
        "writer": "writer",
    },
)

builder.add_edge("refund", "writer")
builder.add_edge("writer", END)

graph = builder.compile()