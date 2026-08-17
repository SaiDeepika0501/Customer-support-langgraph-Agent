from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load document
with open("data/policies.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=120,
    chunk_overlap=30
)

chunks = splitter.split_text(text)

print(f"Created {len(chunks)} chunks\n")

for i, chunk in enumerate(chunks, 1):
    print(f"Chunk {i}: {chunk}\n")

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Build FAISS index
vector_store = FAISS.from_texts(chunks, embeddings)

# Save index
vector_store.save_local("faiss_index")

print("FAISS index saved successfully!")