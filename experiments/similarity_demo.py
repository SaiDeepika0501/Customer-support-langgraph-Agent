import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

query = "I was charged twice"

documents = [
    "A duplicate payment was processed",
    "Refunds are issued within 5 business days",
    "My package arrived late"
]

# Create embeddings
query_vec = embeddings.embed_query(query)
doc_vecs = embeddings.embed_documents(documents)


# Cosine similarity function
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Compute similarities
scores = []

for doc, vec in zip(documents, doc_vecs):
    score = cosine_similarity(query_vec, vec)
    scores.append((doc, score))

# Sort by similarity
scores.sort(key=lambda x: x[1], reverse=True)

print(f"Query: {query}\n")

for doc, score in scores:
    print(f"Score: {score:.4f} | {doc}")

# Query: I was charged twice

# Score: 0.5130 | A duplicate payment was processed
# Score: 0.2589 | My package arrived late
# Score: 0.1634 | Refunds are issued within 5 business days


# 1.0- very similar 
# 0.7-0.9-related
# 0.3-0.6- weakly related
# 0.1 to 0.4-> unrelated
