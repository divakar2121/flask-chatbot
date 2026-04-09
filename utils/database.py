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
            user_id TEXT,
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

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            google_id TEXT UNIQUE,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            gender TEXT,
            age INTEGER,
            salary_range TEXT,
            phone TEXT,
            family_members TEXT,
            family_ages TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized at:", DB_PATH)


def add_message(role, content, user_id=None):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
        (user_id, role, content),
    )
    conn.commit()
    conn.close()


def get_messages(limit=50, user_id=None):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if user_id:
        cursor.execute(
            "SELECT role, content, created_at FROM messages WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        )
    else:
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


def add_or_update_user(
    google_id,
    email,
    name=None,
    gender=None,
    age=None,
    salary_range=None,
    phone=None,
    family_members=None,
    family_ages=None,
):
    """Add or update user profile"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (google_id, email, name, gender, age, salary_range, phone, family_members, family_ages)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(google_id) DO UPDATE SET
            name=excluded.name,
            gender=excluded.gender,
            age=excluded.age,
            salary_range=excluded.salary_range,
            phone=excluded.phone,
            family_members=excluded.family_members,
            family_ages=excluded.family_ages
    """,
        (
            google_id,
            email,
            name,
            gender,
            age,
            salary_range,
            phone,
            family_members,
            family_ages,
        ),
    )
    conn.commit()
    conn.close()


def get_user(google_id):
    """Get user by google_id"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "google_id": row[1],
            "email": row[2],
            "name": row[3],
            "gender": row[4],
            "age": row[5],
            "salary_range": row[6],
            "phone": row[7],
            "family_members": row[8],
            "family_ages": row[9],
            "created_at": row[10],
        }
    return None


def get_all_users():
    """Get all users"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "google_id": r[1],
            "email": r[2],
            "name": r[3],
            "gender": r[4],
            "age": r[5],
            "salary_range": r[6],
            "phone": r[7],
            "family_members": r[8],
            "family_ages": r[9],
        }
        for r in rows
    ]


def update_user_profile(
    google_id, name, gender, age, salary_range, phone, family_members, family_ages
):
    """Update user profile"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE users SET name=?, gender=?, age=?, salary_range=?, phone=?, family_members=?, family_ages=?
        WHERE google_id=?
    """,
        (
            name,
            gender,
            age,
            salary_range,
            phone,
            family_members,
            family_ages,
            google_id,
        ),
    )
    conn.commit()
    conn.close()


init_db()
