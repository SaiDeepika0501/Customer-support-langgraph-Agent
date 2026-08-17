from typing import TypedDict, List, Any, Dict

class FinalState(TypedDict, total=False):
    # User input
    query: str

    # Memory
    current_order_id: str

    # Planning
    needs_rag: bool
    needs_tool: bool

    # Retrieved knowledge
    rag_context: str

    # Tool results
    order_status: str
    tracking_number: str
    customer_name: str

    refund_amount: float
    refund_note: str
    refund_status: str

    needs_order_clarification: bool
    order_not_found: bool
    refund_not_found: bool

  
    history: List[Dict[str, Any]]


    # Response generation
    answer: str

    # Reflection
    critique: str
    needs_revision: bool
    revision_count: int