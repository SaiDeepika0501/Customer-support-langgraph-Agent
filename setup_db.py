import sqlite3

# Database file
DB_PATH = "support.db"

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# =========================================================
# 1. CUSTOMERS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
)
""")


# =========================================================
# 2. ORDERS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    tracking_number TEXT,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
)
""")


# =========================================================
# 3. REFUNDS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS refunds (
    refund_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    reason TEXT,
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
)
""")


# =========================================================
# 4. INSERT SAMPLE CUSTOMERS
# =========================================================

customers = [
    ("CUST-001", "Alice", "alice@example.com"),
    ("CUST-002", "Bob", "bob@example.com"),
    ("CUST-003", "Deepika", "deepika@example.com"),
]

cursor.executemany("""
INSERT OR REPLACE INTO customers
(customer_id, name, email)
VALUES (?, ?, ?)
""", customers)


# =========================================================
# 5. INSERT SAMPLE ORDERS
# =========================================================

orders = [
    ("ORD-111", "CUST-001", "Out for delivery", "TRK-111"),
    ("ORD-222", "CUST-002", "Processing", "TRK-222"),
    ("ORD-555", "CUST-003", "Delivered", "TRK-555"),
]

cursor.executemany("""
INSERT OR REPLACE INTO orders
(order_id, customer_id, status, tracking_number)
VALUES (?, ?, ?, ?)
""", orders)


# =========================================================
# 6. INSERT SAMPLE REFUNDS
# =========================================================

refunds = [
    ("REF-001", "ORD-111", 0.0, "Not requested", None),
    ("REF-002", "ORD-222", 299.0, "Pending", "Customer requested refund"),
    ("REF-003", "ORD-555", 499.0, "Completed", "Duplicate charge"),
]

cursor.executemany("""
INSERT OR REPLACE INTO refunds
(refund_id, order_id, amount, status, reason)
VALUES (?, ?, ?, ?, ?)
""", refunds)


# =========================================================
# 7. SAVE DATABASE
# =========================================================

conn.commit()
conn.close()

print("Database created successfully!")
print("Created tables:")
print("- customers")
print("- orders")
print("- refunds")