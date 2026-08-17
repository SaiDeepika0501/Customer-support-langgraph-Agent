from graph.memory_workflow import graph

# Initial memory
state = {
    "messages": [],
}

# Turn 1
state["query"] = "Where is my order ORD-123?"
state = graph.invoke(state)

print("Turn 1:")
print(state["answer"])
print("Remembered order:", state.get("current_order_id"))

print("\n" + "="*50 + "\n")

# Turn 2
state["query"] = "What about my refund?"
state = graph.invoke(state)

print("Turn 2:")
print(state["answer"])
print("Remembered order:", state.get("current_order_id"))

