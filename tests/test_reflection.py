from graph.reflection_workflow import graph

result = graph.invoke({
    "query": "I was charged twice and my refund is delayed",
    "revision_count": 0
})

print("Final Answer:\n")
print(result["answer"])

print("\nCritique:")
print(result["critique"])

print("\nRevision Count:")
print(result.get("revision_count", 0))