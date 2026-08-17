# FROM python:3.12-slim

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --no-cache-dir --default-timeout=300 -r requirements.txt

# COPY app ./app

# # Root-level modules used by the final application
# COPY memory_store.py .
# COPY session_memory.py .
# COPY rag_engine.py .
# COPY router.py .
# COPY support_engine.py .

# COPY graph ./graph
# COPY data ./data
# COPY models ./models
# COPY prompts ./prompts
# COPY faiss_index ./faiss_index
# COPY support.db .

# EXPOSE 8000

# CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=300 -r requirements.txt

# Application
COPY app ./app

# Runtime data
COPY data ./data
COPY models ./models
COPY prompts ./prompts
COPY faiss_index ./faiss_index
COPY database ./database
# COPY support.db .

EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]