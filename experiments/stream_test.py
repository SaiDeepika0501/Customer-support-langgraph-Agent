import requests

r = requests.post(
    "http://127.0.0.1:8000/chat-stream",
    json={"message": "Where is my order ORD-123?"},
    stream=True
)

for chunk in r.iter_content(chunk_size=1):
    if chunk:
        print(chunk.decode(), end="", flush=True)





#         url -X 'POST' \
#   'http://127.0.0.1:8000/chat' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "message": "Where is my order ORD-123?"
# }'
# Request URL
# http://127.0.0.1:8000/chat
# Server response
# Code	Details
# 200	
# Response body
# Download
# {
#   "request_id": "4fee9110-161d-441c-a66d-3ae860b3cfbb",
#   "answer": "Could you please provide more details about your request?",
#   "source": "langgraph-agent",
#   "latency_ms": 8.32
# }
# Response headers
#  content-length: 167 
#  content-type: application/json 
#  date: Fri,14 Aug 2026 11:22:10 GMT 
#  server: uvicorn 