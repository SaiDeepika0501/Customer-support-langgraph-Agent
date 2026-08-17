# import sqlite3

# DB_PATH = "support.db"


# # =========================================================
# # GET ORDER INFORMATION
# # =========================================================

# def get_order(order_id: str):

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT
#             o.order_id,
#             o.status,
#             o.tracking_number,
#             c.customer_id,
#             c.name,
#             c.email
#         FROM orders o
#         JOIN customers c
#             ON o.customer_id = c.customer_id
#         WHERE o.order_id = ?
#     """, (order_id,))

#     row = cursor.fetchone()

#     conn.close()

#     if not row:
#         return None

#     return {
#         "order_id": row[0],
#         "status": row[1],
#         "tracking_number": row[2],
#         "customer_id": row[3],
#         "customer_name": row[4],
#         "customer_email": row[5],
#     }


# # =========================================================
# # GET REFUND INFORMATION
# # =========================================================

# def get_refund(order_id: str):

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT
#             refund_id,
#             amount,
#             status,
#             reason
#         FROM refunds
#         WHERE order_id = ?
#     """, (order_id,))

#     row = cursor.fetchone()

#     conn.close()

#     if not row:
#         return None

#     return {
#         "refund_id": row[0],
#         "amount": row[1],
#         "status": row[2],
#         "reason": row[3],
#     }


from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "support.db"


# =========================================================
# GET ORDER INFORMATION
# =========================================================

def get_order(order_id: str):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            o.order_id,
            o.status,
            o.tracking_number,
            c.customer_id,
            c.name,
            c.email
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_id = ?
    """, (order_id,))

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return {
        "order_id": row[0],
        "status": row[1],
        "tracking_number": row[2],
        "customer_id": row[3],
        "customer_name": row[4],
        "customer_email": row[5],
    }


# =========================================================
# GET REFUND INFORMATION
# =========================================================

def get_refund(order_id: str):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            refund_id,
            amount,
            status,
            reason
        FROM refunds
        WHERE order_id = ?
    """, (order_id,))

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return {
        "refund_id": row[0],
        "amount": row[1],
        "status": row[2],
        "reason": row[3],
    }