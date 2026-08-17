# from graph.state import SupportState

# def classify_intent(state: SupportState) -> SupportState:
#     query = state["query"].lower()

#     if "refund" in query:
#         intent = "refund"
#     elif "cancel" in query:
#         intent = "cancellation"
#     elif "ship" in query:
#         intent = "shipping"
#     elif "charge" in query or "payment" in query:
#         intent = "payment"
#     else:
#         intent = "other"

#     return {
#         "intent": intent,
#         "confidence": 0.9
#     }


# def generate_response(state: SupportState) -> SupportState:
#     intent = state["intent"]

#     responses = {
#         "refund": "I can help with your refund request.",
#         "cancellation": "I can help cancel your order if it has not shipped yet.",
#         "shipping": "I can help check your shipping status.",
#         "payment": "I can help investigate the payment issue.",
#         "other": "Could you please provide more details?"
#     }

#     return {
#         "answer": responses[intent]
#     }

# //node-> it doesnt return the entire state but only returns the updates,,langgraph will merge them


from graph.state import SupportState

def classify_intent(state: SupportState) -> SupportState:
    query = state["query"].lower()

    if "refund" in query:
        intent = "refund"
    elif "ship" in query:
        intent = "shipping"
    else:
        intent = "other"

    return {"intent": intent}

def route_intent(state: SupportState) -> str:
    intent = state["intent"]

    if intent == "refund":
        return "refund"
    elif intent == "shipping":
        return "shipping"
    else:
        return "generic"

def refund_node(state: SupportState) -> SupportState:
    return {
        "answer": "Refunds are usually processed within 5 business days after approval."
    }


def shipping_node(state: SupportState) -> SupportState:
    return {
        "answer": "Shipping delays may occur during holidays and weekends."
    }


def generic_node(state: SupportState) -> SupportState:
    return {
        "answer": "Could you please provide more details about your issue?"
    }

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