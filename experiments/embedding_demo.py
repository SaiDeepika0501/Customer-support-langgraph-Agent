# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from utils.config import GOOGLE_API_KEY

# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/text-embedding-004",
#     google_api_key=GOOGLE_API_KEY
# )

# texts = [
#     "I was charged twice",
#     "A duplicate payment was processed",
#     "My package arrived late"
# ]

# vectors = embeddings.embed_documents(texts)

# for i, vec in enumerate(vectors):
#     print(f"Text {i+1}: {texts[i]}")
#     print(f"Vector length: {len(vec)}")
#     print(f"First 5 values: {vec[:5]}")
#     print()

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

texts = [
    "I was charged twice",
    "A duplicate payment was processed",
    "My package arrived late"
]

vectors = embeddings.embed_documents(texts)

for i, vec in enumerate(vectors):
    print(f"Text {i+1}: {texts[i]}")
    print(f"Vector length: {len(vec)}")
    print(f"First 5 values: {vec[:5]}")
    print()


# Text 1: I was charged twice
# Vector length: 384
# First 5 values: [0.006755173671990633, 0.02363368310034275, 0.019129134714603424, 0.05136603116989136, 0.06474460661411285]

# Text 2: A duplicate payment was processed
# Vector length: 384
# First 5 values: [-0.07945933192968369, 0.010988098569214344, 0.04847541078925133, -0.020771276205778122, -0.067325159907341]

# Text 3: My package arrived late
# Vector length: 384
# First 5 values: [-0.05813455581665039, -0.007765177637338638, -0.011694565415382385, 0.031107397750020027, 0.07241649925708771]

