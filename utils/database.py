import sqlite3
import os

DB_PATH = "/app/chat_history.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Main messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            synced INTEGER DEFAULT 0
        )
    """)

    # Sync queue for offline messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            synced INTEGER DEFAULT 0,
            retry_count INTEGER DEFAULT 0
        )
    """)

    # Sync metadata
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized at:", DB_PATH)


def add_message(role, content):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)", (role, content)
    )
    conn.commit()
    conn.close()


def get_messages(limit=50):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content, created_at FROM messages ORDER BY created_at DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "created_at": r[2]} for r in rows]


def get_all_conversations():
    init_db()
    return [{"id": 1, "created_at": "N/A", "message_count": len(get_messages(1000))}]


def add_to_queue(role, content):
    """Add message to sync queue (for offline support)"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sync_queue (role, content) VALUES (?, ?)", (role, content)
    )
    conn.commit()
    conn.close()


def get_queue():
    """Get all unsynced messages from queue"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, role, content, created_at FROM sync_queue WHERE synced = 0 ORDER BY created_at"
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": r[0], "role": r[1], "content": r[2], "created_at": r[3]} for r in rows
    ]


def mark_synced(ids):
    """Mark messages as synced"""
    if not ids:
        return
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    placeholders = ",".join("?" * len(ids))
    cursor.execute(
        f"UPDATE sync_queue SET synced = 1 WHERE id IN ({placeholders})", ids
    )
    conn.commit()
    conn.close()


def increment_retry(ids):
    """Increment retry count for failed syncs"""
    if not ids:
        return
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    placeholders = ",".join("?" * len(ids))
    cursor.execute(
        f"UPDATE sync_queue SET retry_count = retry_count + 1 WHERE id IN ({placeholders})",
        ids,
    )
    conn.commit()
    conn.close()


def get_queue_count():
    """Get count of pending messages"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sync_queue WHERE synced = 0")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def clear_messages():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()


init_db()
