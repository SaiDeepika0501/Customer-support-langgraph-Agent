# from langgraph.graph import StateGraph, START, END

# from graph.state import SupportState
# from graph.nodes import classify_intent

# # Create graph
# builder = StateGraph(SupportState)

# # Add node
# builder.add_node("classify", classify_intent)

# # Add edges
# builder.add_edge(START, "classify")
# builder.add_edge("classify", END)

# # Compile graph
# graph = builder.compile()



# from langgraph.graph import StateGraph, START, END

# from graph.state import SupportState
# from graph.nodes import classify_intent, generate_response

# builder = StateGraph(SupportState)

# builder.add_node("classify", classify_intent)
# builder.add_node("respond", generate_response)

# builder.add_edge(START, "classify")
# builder.add_edge("classify", "respond")
# builder.add_edge("respond", END)

# graph = builder.compile()



from langgraph.graph import StateGraph, START, END

from graph.state import SupportState
from graph.nodes import (
    classify_intent,
    refund_node,
    shipping_node,
    generic_node,
    route_intent,
)

builder = StateGraph(SupportState)

builder.add_node("classify", classify_intent)
builder.add_node("refund", refund_node)
builder.add_node("shipping", shipping_node)
builder.add_node("generic", generic_node)

builder.add_edge(START, "classify")

# Conditional routing
builder.add_conditional_edges(
    "classify",
    route_intent,
    {
        "refund": "refund",
        "shipping": "shipping",
        "generic": "generic",
    },
)

builder.add_edge("refund", END)
builder.add_edge("shipping", END)
builder.add_edge("generic", END)

graph = builder.compile()