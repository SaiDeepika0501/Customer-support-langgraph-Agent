from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompts.rag_prompt import rag_prompt
from utils.config import GOOGLE_API_KEY

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS index
vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# Retriever
# retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# updated retriver
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.4,
        "k": 4
    }
)

# LLM
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

parser = StrOutputParser()


# def generate_rag_response(question: str):
#     # Retrieve documents
#     docs = retriever.invoke(question)

#     # Combine context
#     context = "\n\n".join(doc.page_content for doc in docs)

#     # Build chain
#     chain = rag_prompt | model | parser

#     # Generate answer
#     response = chain.invoke({
#         "context": context,
#         "question": question
#     })

#     return response, docs

### Add source citations->A production support bot should show where the answer came from.
def generate_rag_response(question: str):
    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    chain = rag_prompt | model | parser

    response = chain.invoke({
        "context": context,
        "question": question
    })

    sources = [doc.page_content for doc in docs]

    return response, sources