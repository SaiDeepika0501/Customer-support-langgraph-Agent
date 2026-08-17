from graph.db_tools import get_order, get_refund


# =========================================================
# TEST 1 — GET ORDER
# =========================================================

print("========== ORDER TEST ==========")

order = get_order("ORD-222")

print(order)


# =========================================================
# TEST 2 — GET REFUND
# =========================================================

print("\n========== REFUND TEST ==========")

refund = get_refund("ORD-555")

print(refund)


# =========================================================
# TEST 3 — UNKNOWN ORDER
# =========================================================

print("\n========== UNKNOWN ORDER TEST ==========")

unknown_order = get_order("ORD-999")

print(unknown_order)