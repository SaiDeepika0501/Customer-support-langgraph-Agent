from graph.tool_workflow import graph

queries = [
    "Where is my order ORD-123?",
    "What is my refund for ORD-123?",
    "Track ORD-123 and tell me my refund"
]

for q in queries:
    print("\n" + "=" * 50)
    print("Query:", q)

    result = graph.invoke({"query": q})

    print("Tasks:", result.get("tasks"))
    print("Answer:", result["answer"])

    
# ==================================================
# Query: Where is my order ORD-123?
# Tasks: ['order_status']
# Answer: Your order status is: Out for delivery.

# ==================================================
# Query: What is my refund for ORD-123?
# Tasks: ['refund']
# Answer: Eligible refund amount: ₹499.00.

# ==================================================
# Query: Track ORD-123 and tell me my refund
# Tasks: ['order_status', 'refund']
# Answer: Your order status is: Out for delivery. Eligible refund amount: ₹499.00.