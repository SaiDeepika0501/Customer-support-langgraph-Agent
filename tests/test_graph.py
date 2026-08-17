# from graph.workflow import graph

# result = graph.invoke({
#     "query": "I was charged twice for my order"
# })

# print(result)

# from graph.workflow import graph

# result = graph.invoke({
#     "query": "I want to cancel my order"
# })

# print(result)


## output->{'query': 'I want to cancel my order',
#  'intent': 'cancellation', 
# 'answer': 'I can help cancel your order if it has not shipped yet.',
#  'confidence': 0.9}


from graph.workflow import graph

queries = [
    "When will I get my refund?",
    "My shipment is delayed",
    "Hello there"
]

for q in queries:
    print("\n" + "=" * 40)
    print("Query:", q)

    result = graph.invoke({"query": q})

    print("Intent:", result["intent"])
    print("Answer:", result["answer"])



#     Query: When will I get my refund?
# Intent: refund
# Answer: Refunds are usually processed within 5 business days after approval.

# ========================================
# Query: My shipment is delayed
# Intent: shipping
# Answer: Shipping delays may occur during holidays and weekends.

# ========================================
# Query: Hello there
# Intent: other
# Answer: Could you please provide more details about your issue?