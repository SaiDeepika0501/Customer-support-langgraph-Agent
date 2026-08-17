
from dotenv import load_dotenv
load_dotenv()
from collections import defaultdict
from app.memory.memory_store import get_session, update_session

session_store = defaultdict(list)

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import time
import uuid


# Import your LangGraph workflow
from app.graph.final_workflow import graph
from app.memory.session_memory import (
    init_session_db,
    get_session,
    update_session,
    save_message
)

# -----------------------------------------------------
# Step 1: Create FastAPI app
# -----------------------------------------------------
app = FastAPI(title="AI Customer Support API")
init_session_db()
# -----------------------------------------------------
# Step 2: Define request and response schemas
# -----------------------------------------------------
class ChatRequest(BaseModel):
    session_id: str
    message: str
    


class ChatResponse(BaseModel):
    request_id: str
    answer: str
    source: str
    latency_ms: float


# -----------------------------------------------------
# Step 3: Health endpoint
# Used by monitoring / deployment systems
# -----------------------------------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}


# -----------------------------------------------------
# Step 4: Main chat endpoint
# Async + latency measurement + request ID + error handling
# -----------------------------------------------------
# @app.post("/chat", response_model=ChatResponse)
# async def chat(req: ChatRequest):
#     request_id = str(uuid.uuid4())
#     start = time.perf_counter()
#     # history = session_store[req.session_id][-10:]  # last 10 messages
    
#     try:
#         # Run blocking LangGraph workflow in a background thread
#         # result = await asyncio.to_thread(
#         #     graph.invoke,
#         #     {
#         #         "query": req.message,
#         #         "history": history,
#         #         "revision_count": 0
#         #     }
#         # )

#         session = get_session(req.session_id)

#         result = await asyncio.to_thread(
#             graph.invoke,
#             {
#                 "query": req.message,
#                 "revision_count": 0,
#                 **session
#             }
#         )
#         update_session(
#           req.session_id,
#           {
#               "current_order_id": result.get("current_order_id"),
#           }
#       )
#         # # Save user message
#         # session_store[req.session_id].append({
#         #     "role": "user",
#         #     "content": req.message
#         # })

#         latency_ms = (time.perf_counter() - start) * 1000

#         print(f"[{request_id}] Request took {latency_ms:.2f} ms")

#         # Save assistant message
#         # session_store[req.session_id].append({
#         #     "role": "assistant",
#         #     "content": result["answer"]
#         # })

#         return ChatResponse(
#             request_id=request_id,
#             answer=result["answer"],
#             source="langgraph-agent",
#             latency_ms=round(latency_ms, 2)
#         )

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Agent execution failed: {str(e)}"
#         )



@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):

    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    try:

        # -----------------------------------------
        # 1. Load persistent session state
        # -----------------------------------------

        session = get_session(req.session_id)

        print(
            f"[{request_id}] "
            f"Session: {req.session_id}"
        )

        print(
            f"[{request_id}] "
            f"Previous session state: {session}"
        )

        # -----------------------------------------
        # 2. Save user message
        # -----------------------------------------

        save_message(
            req.session_id,
            "user",
            req.message
        )

        # -----------------------------------------
        # 3. Run LangGraph
        # -----------------------------------------

        result = await asyncio.to_thread(
            graph.invoke,
            {
                "query": req.message,
                "revision_count": 0,
                **session
            }
        )

        # -----------------------------------------
        # 4. Save updated session state
        # -----------------------------------------

        update_session(
            req.session_id,
            result.get("current_order_id")
        )

        # -----------------------------------------
        # 5. Save assistant response
        # -----------------------------------------

        save_message(
            req.session_id,
            "assistant",
            result["answer"]
        )

        # -----------------------------------------
        # 6. Calculate latency
        # -----------------------------------------

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        print(
            f"[{request_id}] "
            f"Request took {latency_ms:.2f} ms"
        )

        # -----------------------------------------
        # 7. Return response
        # -----------------------------------------

        return ChatResponse(
            request_id=request_id,
            answer=result["answer"],
            source="langgraph-agent",
            latency_ms=round(latency_ms, 2)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )
# -----------------------------------------------------
# Step 5: Streaming helper
# Sends the answer word by word
# -----------------------------------------------------
async def fake_stream(answer: str):
    for word in answer.split():
        yield word + " "
        await asyncio.sleep(0.05)


# -----------------------------------------------------
# Step 6: Streaming endpoint
# Useful for ChatGPT-like typing effect
# -----------------------------------------------------
@app.post("/chat-stream")
async def chat_stream(req: ChatRequest):
    try:
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Streaming failed: {str(e)}"
        )


@app.get("/history/{session_id}")
async def get_history(session_id: str):
    return session_store.get(session_id, [])