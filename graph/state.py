from typing import TypedDict, List, Dict

class SupportState(TypedDict, total=False):
    query: str
    intent: str
    retrieved_docs: List[str]
    answer: str
    confidence: float
    critique: str
    needs_revision: bool
    revision_count: int
    # Planner output
    tasks: List[str]

    # Retrieved information
    refund_info: str
    payment_info: str


    # Conversation memory
    messages: List[Dict[str, str]]
    current_order_id: str

    # Tool outputs
    order_status: str
    refund_amount: float
    
    # Final response
    answer: str