# def route_intent(intent: str) -> str:
#     routes = {
#         "refund": "refund_chain",
#         "shipping": "shipping_chain",
#         "cancellation": "cancellation_chain",
#         "policy": "policy_chain",
#         "order_status": "order_chain",
#         "other": "general_chain"
#     }

#     return routes.get(intent, "general_chain")

def route_intent(intent: str, confidence: float) -> str: 
    THRESHOLD = 0.80 
    if confidence < THRESHOLD: return "clarification_chain" 
    routes = {
        "refund": "refund_chain",
        "shipping": "shipping_chain",
        "cancellation": "cancellation_chain",
        "policy": "policy_chain",
        "order_status": "order_chain",
        "other": "general_chain"
    }
    # routes = { "refund": "refund_chain", "shipping": "shipping_chain", "cancellation": "cancellation_chain", "policy": "policy_chain", "order_status": "order_chain", "other": "general_chain" } 
    return routes.get(intent, "general_chain")