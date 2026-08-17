
FROM python:3.12-slim

WORKDIR /app

COPY requirements.docker.txt .

RUN pip install --no-cache-dir --default-timeout=300 -r requirements.docker.txt

# Application code
COPY app ./app

# Runtime data
COPY data ./data
COPY database ./database
COPY models ./models
COPY prompts ./prompts
COPY faiss_index ./faiss_index

EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]