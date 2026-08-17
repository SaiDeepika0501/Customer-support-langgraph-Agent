from langgraph.graph import StateGraph, START, END

from graph.state import SupportState
from graph.multi_agent_nodes import (
    planner_agent,
    refund_retriever,
    payment_retriever,
    writer_agent,
    route_after_planner,
    route_after_payment,
)

builder = StateGraph(SupportState)

builder.add_node("planner", planner_agent)
builder.add_node("payment", payment_retriever)
builder.add_node("refund", refund_retriever)
builder.add_node("writer", writer_agent)

builder.add_edge(START, "planner")

builder.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "payment": "payment",
        "refund": "refund",
        "writer": "writer",
    },
)

builder.add_conditional_edges(
    "payment",
    route_after_payment,
    {
        "refund": "refund",
        "writer": "writer",
    },
)

builder.add_edge("refund", "writer")
builder.add_edge("writer", END)

graph = builder.compile()