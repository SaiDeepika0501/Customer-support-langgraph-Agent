from graph.state import SupportState

def planner_agent(state: SupportState) -> SupportState:
    query = state["query"].lower()

    tasks = []

    if "refund" in query:
        tasks.append("refund")

    if "charged twice" in query or "payment" in query:
        tasks.append("payment")

    if not tasks:
        tasks.append("general")

    return {"tasks": tasks}


def refund_retriever(state: SupportState) -> SupportState:
    return {
        "refund_info": "Refunds are issued within 5 business days after approval."
    }

def payment_retriever(state: SupportState) -> SupportState:
    return {
        "payment_info": (
            "Duplicate charges may occur due to temporary authorization holds "
            "and are usually reversed automatically."
        )
    }

def writer_agent(state: SupportState) -> SupportState:
    parts = []

    if state.get("payment_info"):
        parts.append(state["payment_info"])

    if state.get("refund_info"):
        parts.append(state["refund_info"])

    answer = " ".join(parts)

    if not answer:
        answer = "Could you please provide more details about your request?"

    return {"answer": answer}

def route_after_planner(state: SupportState) -> str:
    tasks = state["tasks"]

    if "payment" in tasks:
        return "payment"

    if "refund" in tasks:
        return "refund"

    return "writer"


def route_after_payment(state: SupportState) -> str:
    tasks = state["tasks"]

    if "refund" in tasks:
        return "refund"

    return "writer"