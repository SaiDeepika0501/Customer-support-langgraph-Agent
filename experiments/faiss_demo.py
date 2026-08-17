# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS

# documents = [
#     "Electronics can be returned within 30 days of delivery.",
#     "Refunds are issued within 5 business days after approval.",
#     "Orders can be cancelled before they are shipped.",
#     "Shipping delays may occur during holidays and weekends.",
# ]

# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# # Create FAISS index
# vector_store = FAISS.from_texts(
#     texts=documents,
#     embedding=embeddings
# )

# print("FAISS index created successfully!")


from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

documents = [
    "Electronics can be returned within 30 days of delivery.",
    "Refunds are issued within 5 business days after approval.",
    "Orders can be cancelled before they are shipped.",
    "Shipping delays may occur during holidays and weekends.",
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = FAISS.from_texts(documents, embeddings)

query = "Can I cancel my order before shipping?"

# results = vector_store.similarity_search(query, k=2)

# print(f"Query: {query}\n")

# for i, doc in enumerate(results, 1):
#     print(f"Result {i}:")
#     print(doc.page_content)
#     print()

# Query: Can I cancel my order before shipping?

# Result 1:
# Orders can be cancelled before they are shipped.

# Result 2:
# Shipping delays may occur during holidays and weekends.

results = vector_store.similarity_search_with_score(query, k=3)

for i, (doc, score) in enumerate(results, 1):
    print(f"Result {i} | Score: {score:.4f}")
    print(doc.page_content)
    print()

# Result 1 | Score: 0.3932
# Orders can be cancelled before they are shipped.

# Result 2 | Score: 1.1078
# Shipping delays may occur during holidays and weekends.

# Result 3 | Score: 1.2911
# Electronics can be returned within 30 days of delivery.