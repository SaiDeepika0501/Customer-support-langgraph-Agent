import re
from graph.state import SupportState

def remember_order_id(state: SupportState) -> SupportState:
    query = state["query"]

    match = re.search(r"ORD-\d+", query)

    if match:
        return {"current_order_id": match.group(0)}

    return {}


def resolve_order_id(state: SupportState) -> SupportState:
    query = state["query"]

    # If query already contains an order ID, do nothing
    if "ORD-" in query:
        return {}

    # Use remembered order ID
    remembered = state.get("current_order_id")

    if remembered:
        return {"query": f"{query} {remembered}"}

    return {}