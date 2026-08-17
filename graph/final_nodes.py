##   memory node

import re
from graph.final_state import FinalState
from graph.db_tools import get_order,get_refund

# def memory_node(state: FinalState) -> FinalState:
#     query = state["query"]

#     match = re.search(r"ORD-\d+", query)

#     if match:
#         return {"current_order_id": match.group(0)}

#     return {}

def memory_node(state: FinalState) -> FinalState:
    query = state["query"]

    # Current message
    match = re.search(r"ORD-\d+", query)
    if match:
        return {"current_order_id": match.group(0)}

    # Look back in history
    for msg in reversed(state.get("history", [])):
        m = re.search(r"ORD-\d+", msg["content"])
        if m:
            return {"current_order_id": m.group(0)}

    return {}


# planner node

# def planner_node(state: FinalState) -> FinalState:
#     query = state["query"].lower()

#     needs_rag = any(
#         word in query
#         for word in ["policy", "return", "cancel", "refund policy"]
#     )

#     needs_tool = any(
#         word in query
#         for word in ["where is my order", "track", "refund amount", "charged twice"]
#     )

#     return {
#         "needs_rag": needs_rag,
#         "needs_tool": needs_tool
#     }

def planner_node(state: FinalState) -> FinalState:
    query = state["query"].lower()

    needs_rag = any(
        phrase in query
        for phrase in [
            "policy",
            "return",
            "return policy",
            "cancel",
            "cancellation",
            "refund policy",
            "shipping policy",
            "shipping",
            "warranty",
        ]
    )

    needs_tool = any(
        phrase in query
        for phrase in [
            "where is my order",
            "track",
            "track my order",
            "order status",
            "shipping status",
            "refund amount",
            "refund for",
            "refund",
            "refund status",
            "charged twice",
            "duplicate charge",
        ]
    )
    print(
    "PLANNER:",
    {
        "needs_rag": needs_rag,
        "needs_tool": needs_tool
    }
    )

    return {
        "needs_rag": needs_rag,
        "needs_tool": needs_tool
    }


# RAG Node
# def rag_node(state: FinalState) -> FinalState:
#     query = state["query"].lower()
#     contexts = []

#     if "return" in query:
#         contexts.append(
#             "Returns are accepted within 30 days if the item is unopened."
#         )

#     if "cancel" in query:
#         contexts.append(
#             "Orders can be cancelled before shipment."
#         )

#     if "refund" in query:
#         contexts.append(
#             "Refunds are issued within 5 business days after approval."
#         )

#     return {"rag_context": " ".join(contexts)}

def rag_node(state: FinalState) -> FinalState:
    query = state["query"].lower()

    contexts = []

    if "return" in query:
        contexts.append(
            "Returns are accepted within 30 days if the item is unopened."
        )

    if "cancel" in query or "cancellation" in query:
        contexts.append(
            "Orders can be cancelled before shipment. "
            "If payment has already been captured, cancellation may not be possible."
        )

    if "refund policy" in query:
        contexts.append(
            "Refunds are issued within 5 business days after approval."
        )

    if "shipping policy" in query:
        contexts.append(
            "Shipping delays may occur during holidays and weekends."
        )

    context = " ".join(contexts)
    print("RAG CONTEXT:", context)

    return {"rag_context": context}

# ## tool NOde


# def tool_node(state: FinalState) -> FinalState:
#     query = state["query"].lower()
#     order_id = state.get("current_order_id")

#     updates = {}

#     # Order tracking
#     if "track" in query or "where is my order" in query:
#         if not order_id:
#             updates["needs_order_clarification"] = True
#             return updates

#         updates["order_status"] = "Out for delivery"

#     # Duplicate payment / refund tool
#     if "refund amount" in query or "charged twice" in query:
#         updates["refund_amount"] = 499.0
#         updates["refund_note"] = (
#             "A duplicate charge may be caused by a temporary authorization hold."
#         )

#     return updates


def tool_node(state: FinalState) -> FinalState:
    query = state["query"].lower()
    order_id = state.get("current_order_id")

    updates = {}

    # -------------------------------------------------
    # No order ID available
    # -------------------------------------------------

    if not order_id:
        if (
            "track" in query
            or "where is my order" in query
            or "order status" in query
            or "refund amount" in query
            or "refund for my order" in query
        ):
            updates["needs_order_clarification"] = True

        return updates

    # -------------------------------------------------
    # Get order information from SQLite
    # -------------------------------------------------

    order = get_order(order_id)

    if not order:
        updates["order_not_found"] = True
        return updates

    # -------------------------------------------------
    # Order tracking / status
    # -------------------------------------------------

    if (
        "track" in query
        or "where is my order" in query
        or "order status" in query
        or "shipping status" in query
    ):
        updates["order_status"] = order["status"]
        updates["tracking_number"] = order["tracking_number"]
        updates["customer_name"] = order["customer_name"]

    # -------------------------------------------------
    # Refund information
    # -------------------------------------------------

    if (
        "refund" in query
        or "charged twice" in query
        or "duplicate charge" in query
    ):
        refund = get_refund(order_id)

        if refund:
            updates["refund_amount"] = refund["amount"]
            updates["refund_status"] = refund["status"]
            updates["refund_note"] = refund["reason"]

        else:
            updates["refund_not_found"] = True
    print("TOOL ORDER ID:", order_id)
    print("TOOL UPDATES:", updates)

    return updates


## Writer Node

# def writer_node(state: FinalState) -> FinalState:
#     parts = []

#     # Order clarification
#     if state.get("needs_order_clarification"):
#         parts.append(
#             "I can help track your order, but I could not identify a unique order from the product name. Please provide your order ID (for example, ORD-123)."
#         )

#     # Order status
#     if state.get("order_status"):
#         order_id = state.get("current_order_id", "your order")
#         parts.append(
#             f"Order {order_id} is currently {state['order_status']}."
#         )

#     # Refund / duplicate payment
#     if state.get("refund_amount") is not None:
#         parts.append(state.get("refund_note", ""))
#         parts.append(
#             f"If the extra charge is not reversed automatically, the eligible refund amount is ₹{state['refund_amount']:.2f}."
#         )

#     # RAG information
#     if state.get("rag_context"):
#         parts.append(state["rag_context"])

#     # Fallback
#     if not parts:
#         parts.append(
#             "I could not find this information in the available company policies."
#         )

#     answer = " ".join(p for p in parts if p)
#     print("STATE:",state)

#     return {"answer": answer}


def writer_node(state: FinalState) -> FinalState:
    parts = []

    # -------------------------------------------------
    # Unknown order
    # -------------------------------------------------

    if state.get("order_not_found"):
        parts.append(
            f"I couldn't find order {state.get('current_order_id')} "
            "in our system. Please check the order ID and try again."
        )

    # -------------------------------------------------
    # Missing order ID
    # -------------------------------------------------

    elif state.get("needs_order_clarification"):
        parts.append(
            "I can help with your order, but I need your order ID "
            "(for example, ORD-222) to look up the correct information."
        )

    # -------------------------------------------------
    # Order information
    # -------------------------------------------------

    if state.get("order_status"):
        order_id = state.get("current_order_id", "your order")

        message = (
            f"Order {order_id} is currently "
            f"{state['order_status']}."
        )

        if state.get("tracking_number"):
            message += (
                f" Tracking number: "
                f"{state['tracking_number']}."
            )

        parts.append(message)

    # -------------------------------------------------
    # Refund information
    # -------------------------------------------------

    if state.get("refund_amount") is not None:

        refund_message = (
            f"Refund amount: "
            f"₹{state['refund_amount']:.2f}."
        )

        if state.get("refund_status"):
            refund_message += (
                f" Refund status: "
                f"{state['refund_status']}."
            )

        if state.get("refund_note"):
            refund_message += (
                f" Reason: {state['refund_note']}."
            )

        parts.append(refund_message)

    elif state.get("refund_not_found"):
        parts.append(
            "I couldn't find refund information for this order."
        )

    # -------------------------------------------------
    # RAG information
    # -------------------------------------------------

    if state.get("rag_context"):
        parts.append(state["rag_context"])

    # -------------------------------------------------
    # No information found
    # -------------------------------------------------

    if not parts:
        parts.append(
            "I could not find this information in the "
            "available company policies."
        )

    answer = " ".join(parts)

    return {"answer": answer}


### Reflection Node

def reflect_node(state: FinalState) -> FinalState:
    answer = state["answer"].lower()
    query = state["query"].lower()

    issues = []

    if "charged twice" in query and "refund" not in answer:
        issues.append("refund information missing")

    if "where is my order" in query and "order" not in answer:
        issues.append("order status missing")

    if issues:
        return {
            "critique": ", ".join(issues),
            "needs_revision": True
        }

    return {
        "critique": "Answer is sufficient",
        "needs_revision": False
    }


def revise_node(state: FinalState) -> FinalState:
    count = state.get("revision_count", 0) + 1

    answer = state["answer"]

    # Ask for order ID only if we don't already have one
    if not state.get("current_order_id"):
        answer += " Please provide your order ID if you need further assistance."

    return {
        "answer": answer,
        "revision_count": count
    }

# Routing functions/

def route_after_planner(state: FinalState) -> str:
    if state.get("needs_rag") and state.get("needs_tool"):
        return "rag"

    if state.get("needs_rag"):
        return "rag"

    if state.get("needs_tool"):
        return "tool"

    return "writer"


def route_after_rag(state: FinalState) -> str:
    if state.get("needs_tool"):
        return "tool"
    return "writer"


def route_after_reflection(state: FinalState) -> str:
    if state.get("needs_revision", False):
        if state.get("revision_count", 0) >= 1:
            return "end"
        return "revise"

    return "end"