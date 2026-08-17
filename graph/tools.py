def check_order_status(order_id: str) -> str:
    # Mock external API
    fake_db = {
        "ORD-123": "Out for delivery",
        "ORD-456": "Delivered yesterday",
        "ORD-789": "Processing in warehouse",
    }

    return fake_db.get(order_id, "Order not found")


def calculate_refund(order_id: str) -> float:
    fake_refunds = {
        "ORD-123": 499.0,
        "ORD-456": 1299.0,
    }

    return fake_refunds.get(order_id, 0.0)