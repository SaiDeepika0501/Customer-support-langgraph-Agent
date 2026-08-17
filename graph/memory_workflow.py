from langgraph.graph import StateGraph, START, END

from graph.state import SupportState
from graph.memory_nodes import remember_order_id, resolve_order_id
from graph.tool_nodes import order_status_node, refund_node, writer

builder = StateGraph(SupportState)

builder.add_node("remember", remember_order_id)
builder.add_node("resolve", resolve_order_id)
builder.add_node("order_status", order_status_node)
builder.add_node("refund", refund_node)
builder.add_node("writer", writer)

builder.add_edge(START, "remember")
builder.add_edge("remember", "resolve")
builder.add_edge("resolve", "order_status")
builder.add_edge("order_status", "refund")
builder.add_edge("refund", "writer")
builder.add_edge("writer", END)

graph = builder.compile()