from graph.final_workflow import graph

queries = [
    "What is your return policy?",
    "Where is my order ORD-123?",
    "I was charged twice for ORD-123",
    "Can I cancel my order and what is my refund amount for ORD-123?"
]

for q in queries:
    print("\n" + "="*70)
    print("Query:", q)

    result = graph.invoke({
        "query": q,
        "revision_count": 0
    })

    print("\nAnswer:")
    print(result["answer"])

    print("\nCritique:")
    print(result["critique"])


# Query: What is your return policy?

# Answer:
# Returns are accepted within 30 days if the item is unopened.

# Critique:
# Answer is sufficient

# ======================================================================
# Query: Where is my order ORD-123?

# Answer:
# Could you please provide more details about your request? Please provide your order ID if you need further assistance.

# Critique:
# order status missing

# ======================================================================
# Query: I was charged twice for ORD-123

# Answer:
# Eligible refund amount: ₹499.00.

# Critique:
# Answer is sufficient

# ======================================================================
# Query: Can I cancel my order and what is my refund amount for ORD-123?

# Answer:
# Eligible refund amount: ₹499.00. Orders can be cancelled before shipment.

# Critique:
# Answer is sufficient