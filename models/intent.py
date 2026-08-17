from pydantic import BaseModel, Field
from typing import Literal

class IntentOutput(BaseModel):
    intent: Literal[
        "refund",
        "shipping",
        "cancellation",
        "policy",
        "order_status",
        "payment",
        "other"
    ] = Field(description="Detected customer intent")

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )
    # confidence: int = Field( ge=0, le=100, description="Confidence score as an integer percentage" )