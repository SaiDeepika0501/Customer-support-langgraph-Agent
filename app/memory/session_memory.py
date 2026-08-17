import sqlite3
from datetime import datetime

DB_PATH = "support.db"


def init_session_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            current_order_id TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_session(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT current_order_id
        FROM sessions
        WHERE session_id = ?
    """, (session_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return {}

    return {
        "current_order_id": row[0]
    }


def update_session(session_id: str, current_order_id=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    now = datetime.utcnow().isoformat()

    cur.execute("""
        INSERT INTO sessions (
            session_id,
            current_order_id,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(session_id)
        DO UPDATE SET
            current_order_id = COALESCE(
                excluded.current_order_id,
                sessions.current_order_id
            ),
            updated_at = excluded.updated_at
    """, (
        session_id,
        current_order_id,
        now,
        now
    ))

    conn.commit()
    conn.close()


def save_message(session_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO messages (
            session_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        session_id,
        role,
        content,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()