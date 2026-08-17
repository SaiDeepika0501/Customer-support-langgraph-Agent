from evaluation_dataset import test_cases
from rag_engine import vector_store  # adjust import

correct = 0

mapping = {
    "REFUND": "refund",
    "CANCELLATION": "cancellation",
    "RETURN": "return",
    "PAYMENT": "payment",
    "SHIPPING": "shipping",
    "ORDER": "order"
}

for query, expected in test_cases:
    docs = vector_store.similarity_search(query, k=3)

    keyword = mapping[expected]

    if any(keyword in d.page_content.lower() for d in docs):
        correct += 1

accuracy = correct / len(test_cases) * 100

print(f"Top-3 retrieval accuracy: {accuracy:.1f}%")