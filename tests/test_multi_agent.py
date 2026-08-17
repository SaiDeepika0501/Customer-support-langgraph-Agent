from graph.multi_agent_workflow import graph

query = "I was charged twice and my refund is delayed"

result = graph.invoke({"query": query})

print("Tasks:", result.get("tasks"))
print()
print("Payment Info:", result.get("payment_info"))
print()
print("Refund Info:", result.get("refund_info"))
print()
print("Final Answer:")
print(result["answer"])



# Tasks: ['refund', 'payment']

# Payment Info: Duplicate charges may occur due to temporary authorization holds and are usually reversed automatically.

# Refund Info: Refunds are issued within 5 business days after approval.

# Final Answer:
# Duplicate charges may occur due to temporary authorization holds and are usually reversed automatically. Refunds are issued within 5 business days after approval.