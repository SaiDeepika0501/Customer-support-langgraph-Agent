import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

# Knowledge base
documents = [
    "Electronics can be returned within 30 days of delivery.",
    "Refunds are issued within 5 business days after approval.",
    "Orders can be cancelled before they are shipped.",
    "Shipping delays may occur during holidays and weekends.",
]

# Initialize embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Embed documents once
doc_vectors = embeddings.embed_documents(documents)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve(query, top_k=2):
    query_vec = embeddings.embed_query(query)

    scores = []

    for doc, vec in zip(documents, doc_vectors):
        score = cosine_similarity(query_vec, vec)
        scores.append((doc, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:top_k]


# Test queries
queries = [
    "Can I return my laptop after 20 days?",
    "When will I get my refund?",
    "My order has not shipped yet, can I cancel it?",
]

for q in queries:
    print(f"\nQuery: {q}")
    results = retrieve(q)

    for doc, score in results:
        print(f"  {score:.4f} | {doc}")




# Query: Can I return my laptop after 20 days?
#   0.5929 | Electronics can be returned within 30 days of delivery.
#   0.3341 | Refunds are issued within 5 business days after approval.

# Query: When will I get my refund?
#   0.6693 | Refunds are issued within 5 business days after approval.
#   0.4205 | Electronics can be returned within 30 days of delivery.

# Query: My order has not shipped yet, can I cancel it?
#   0.7600 | Orders can be cancelled before they are shipped.
#   0.3760 | Shipping delays may occur during holidays and weekends.