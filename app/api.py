from dotenv import load_dotenv

load_dotenv()

import asyncio
import logging
import time
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.graph.final_workflow import graph
from app.memory.session_memory import (
    init_session_db,
    get_session,
    update_session,
    save_message,
)


# =====================================================
# Structured logging configuration
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("customer-support-agent")


# =====================================================
# FastAPI application
# =====================================================

app = FastAPI(
    title="AI Customer Support API",
    version="0.1.0",
)


# Initialize persistent session database
init_session_db()


# =====================================================
# Request / Response schemas
# =====================================================

class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    request_id: str
    answer: str
    source: str
    latency_ms: float


# =====================================================
# Health endpoint
# Used by Render / monitoring / deployment systems
# =====================================================

@app.get("/health")
async def health():
    logger.info("Health check requested")

    return {
        "status": "ok"
    }


# =====================================================
# Main chat endpoint
# =====================================================

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):

    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    logger.info(
        "Request received | request_id=%s | session_id=%s",
        request_id,
        req.session_id,
    )

    try:

        # ---------------------------------------------
        # 1. Load persistent session state
        # ---------------------------------------------

        session = get_session(req.session_id)

        logger.info(
            "Session state loaded | request_id=%s | session_id=%s",
            request_id,
            req.session_id,
        )

        # ---------------------------------------------
        # 2. Save user message
        # ---------------------------------------------

        save_message(
            req.session_id,
            "user",
            req.message,
        )

        logger.info(
            "User message saved | request_id=%s | session_id=%s",
            request_id,
            req.session_id,
        )

        # ---------------------------------------------
        # 3. Run LangGraph workflow
        # ---------------------------------------------

        logger.info(
            "LangGraph execution started | request_id=%s",
            request_id,
        )

        result = await asyncio.to_thread(
            graph.invoke,
            {
                "query": req.message,
                "revision_count": 0,
                **session,
            },
        )

        logger.info(
            "LangGraph execution completed | request_id=%s",
            request_id,
        )

        # ---------------------------------------------
        # 4. Save updated session state
        # ---------------------------------------------

        update_session(
            req.session_id,
            result.get("current_order_id"),
        )

        logger.info(
            "Session state updated | request_id=%s | session_id=%s",
            request_id,
            req.session_id,
        )

        # ---------------------------------------------
        # 5. Save assistant response
        # ---------------------------------------------

        save_message(
            req.session_id,
            "assistant",
            result["answer"],
        )

        # ---------------------------------------------
        # 6. Calculate latency
        # ---------------------------------------------

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        logger.info(
            "Request completed | request_id=%s | latency_ms=%.2f",
            request_id,
            latency_ms,
        )

        # ---------------------------------------------
        # 7. Return response
        # ---------------------------------------------

        return ChatResponse(
            request_id=request_id,
            answer=result["answer"],
            source="langgraph-agent",
            latency_ms=round(latency_ms, 2),
        )

    except Exception:

        logger.exception(
            "Agent execution failed | request_id=%s | session_id=%s",
            request_id,
            req.session_id,
        )

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed",
        )


# =====================================================
# Streaming helper
# =====================================================

async def fake_stream(answer: str):

    for word in answer.split():

        yield word + " "

        await asyncio.sleep(0.05)


# =====================================================
# Streaming endpoint
# =====================================================

@app.post("/chat-stream")
async def chat_stream(req: ChatRequest):

    request_id = str(uuid.uuid4())

    logger.info(
        "Streaming request received | request_id=%s | session_id=%s",
        request_id,
        req.session_id,
    )

    try:

        result = await asyncio.to_thread(
            graph.invoke,
            {
                "query": req.message,
                "revision_count": 0,
            },
        )

        logger.info(
            "Streaming workflow completed | request_id=%s",
            request_id,
        )

        return StreamingResponse(
            fake_stream(result["answer"]),
            media_type="text/plain",
        )

    except Exception:

        logger.exception(
            "Streaming failed | request_id=%s | session_id=%s",
            request_id,
            req.session_id,
        )

        raise HTTPException(
            status_code=500,
            detail="Streaming failed",
        )


# =====================================================
# Session history endpoint
# =====================================================

@app.get("/history/{session_id}")
async def get_history_endpoint(session_id: str):

    logger.info(
        "History requested | session_id=%s",
        session_id,
    )

    try:

        history = get_session(session_id)

        return history

    except Exception:

        logger.exception(
            "History retrieval failed | session_id=%s",
            session_id,
        )

        raise HTTPException(
            status_code=500,
            detail="Could not retrieve session history",
        )