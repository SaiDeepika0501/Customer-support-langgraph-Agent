from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from graph.final_workflow import graph
import asyncio
import time

app = FastAPI(title="AI Customer Support API")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    source: str

@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi.responses import StreamingResponse
import asyncio

async def fake_stream(answer: str):
    for word in answer.split():
        yield word + " "
        await asyncio.sleep(0.1)

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    start = time.time()
    try:
        result = await asyncio.to_thread(graph.invoke({
            "query": req.message,
            "revision_count": 0
        }))

        duration = time.time() - start

        print(f"Request took {duration:.2f}s")

        return ChatResponse(
            answer=result["answer"],
            source="langgraph-agent"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )
# what is your return policy?
# {
#   "answer": "Returns are accepted within 30 days if the item is unopened.",
#   "source": "langgraph-agent"
# }

# import uuid

# class ChatResponse(BaseModel):
#     request_id: str
#     answer: str
#     source: str

# @app.post("/chat", response_model=ChatResponse)
# async def chat(req: ChatRequest):

#     request_id = str(uuid.uuid4())

#     result = await asyncio.to_thread(
#         graph.invoke,
#         {
#             "query": req.message,
#             "revision_count": 0
#         }
#     )

#     return ChatResponse(
#         request_id=request_id,
#         answer=result["answer"],
#         source="langgraph-agent"
#     )

from fastapi.responses import StreamingResponse
import asyncio

async def fake_stream(answer: str):
    for word in answer.split():
        yield word + " "
        await asyncio.sleep(0.1)

@app.post("/chat-stream")
async def chat_stream(req: ChatRequest):

    result = await asyncio.to_thread(
        graph.invoke,
        {
            "query": req.message,
            "revision_count": 0
        }
    )

    return StreamingResponse(
        fake_stream(result["answer"]),
        media_type="text/plain"
    )