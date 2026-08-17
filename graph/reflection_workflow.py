from langgraph.graph import StateGraph, START, END

from graph.state import SupportState
from graph.reflection_nodes import (
    generate_answer,
    reflect_answer,
    revise_answer,
    route_after_reflection,
)

builder = StateGraph(SupportState)

builder.add_node("generate", generate_answer)
builder.add_node("reflect", reflect_answer)
builder.add_node("revise", revise_answer)

builder.add_edge(START, "generate")
builder.add_edge("generate", "reflect")

builder.add_conditional_edges(
    "reflect",
    route_after_reflection,
    {
        "revise": "revise",
        "end": END,
    },
)

builder.add_edge("revise", "generate")

graph = builder.compile()