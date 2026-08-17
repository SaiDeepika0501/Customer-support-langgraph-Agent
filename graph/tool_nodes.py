from graph.state import SupportState
from graph.tools import check_order_status, calculate_refund

def planner(state: SupportState) -> SupportState:
    query = state["query"].lower()

    tasks = []

    if "where is my order" in query or "track" in query:
        tasks.append("order_status")

    if "refund" in query:
        tasks.append("refund")

    return {"tasks": tasks}

# def order_status_node(state: SupportState) -> SupportState:
#     query = state["query"]

#     # Simple extraction
#     order_id = "ORD-123" if "ORD-123" in query else "UNKNOWN"

#     status = check_order_status(order_id)

#     return {"order_status": status}

# def refund_node(state: SupportState) -> SupportState:
#     query = state["query"]

#     order_id = "ORD-123" if "ORD-123" in query else "UNKNOWN"

#     amount = calculate_refund(order_id)

#     return {"refund_amount": amount}

def writer(state: SupportState) -> SupportState:
    parts = []

    if state.get("order_status"):
        parts.append(f"Your order status is: {state['order_status']}.")

    if state.get("refund_amount") is not None:
        parts.append(f"Eligible refund amount: ₹{state['refund_amount']:.2f}.")

    if not parts:
        parts.append("I could not determine the requested information.")

    return {"answer": " ".join(parts)}


def route_after_planner(state: SupportState) -> str:
    tasks = state.get("tasks", [])

    if "order_status" in tasks:
        return "order_status"

    if "refund" in tasks:
        return "refund"

    return "writer"


def route_after_order(state: SupportState) -> str:
    tasks = state.get("tasks", [])

    if "refund" in tasks:
        return "refund"

    return "writer"


import re
from graph.state import SupportState
from graph.tools import check_order_status, calculate_refund

def order_status_node(state: SupportState) -> SupportState:
    query = state["query"]

    match = re.search(r"ORD-\d+", query)
    order_id = match.group(0) if match else "UNKNOWN"

    status = check_order_status(order_id)

    return {"order_status": status}


def refund_node(state: SupportState) -> SupportState:
    query = state["query"]

    match = re.search(r"ORD-\d+", query)
    order_id = match.group(0) if match else "UNKNOWN"

    amount = calculate_refund(order_id)

    return {"refund_amount": amount}