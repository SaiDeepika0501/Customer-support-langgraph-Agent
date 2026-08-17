from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load saved index
vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

query = "I was charged twice"

results = vector_store.similarity_search(query, k=2)

print(f"Query: {query}\n")

for i, doc in enumerate(results, 1):
    print(f"Result {i}:")
    print(doc.page_content)
    print()