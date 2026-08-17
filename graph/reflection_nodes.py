from graph.state import SupportState

def generate_answer(state: SupportState) -> SupportState:
    query = state["query"]

    # First attempt is intentionally short
    if state.get("revision_count", 0) == 0:
        answer = "Refunds are processed within 5 business days."
    else:
        answer = (
            "I understand you are concerned about being charged twice and the refund delay. "
            "Refunds are usually processed within 5 business days after approval. "
            "Please provide your order ID so I can help check the status of both the duplicate charge and the refund request."
        )

    return {"answer": answer}


def reflect_answer(state: SupportState) -> SupportState:
    answer = state["answer"].lower()
    query = state["query"].lower()

    missing = []

    if "charged twice" in query and "charged twice" not in answer:
        missing.append("duplicate charge not acknowledged")

    if "order id" not in answer:
        missing.append("order ID not requested")

    if missing:
        return {
            "critique": ", ".join(missing),
            "needs_revision": True
        }

    return {
        "critique": "Answer is sufficient",
        "needs_revision": False
    }

def revise_answer(state: SupportState) -> SupportState:
    count = state.get("revision_count", 0) + 1

    return {
        "revision_count": count
    }

def route_after_reflection(state: SupportState) -> str:
    if state.get("needs_revision", False):
        if state.get("revision_count", 0) >= 1:
            return "end"
        return "revise"

    return "end"