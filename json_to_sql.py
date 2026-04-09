#!/usr/bin/env python3
"""
Convert chat JSON to SQL database for analysis
Usage: python json_to_sql.py [--db chat_data.db]
"""

import json
import sqlite3
import argparse
import os
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data" / "chat_history"
DB_FILE = "chat_data.db"


def clean_text(text):
    """Clean text for SQL - escape quotes and newlines"""
    if text is None:
        return ""
    # Replace single quotes with two single quotes (SQL escaping)
    text = text.replace("'", "''")
    # Replace newlines with space
    text = text.replace("\n", " ").replace("\r", " ")
    # Remove other problematic chars
    text = text.replace("\\", "")
    return text.strip()


def create_table(conn):
    """Create chat table"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            date TEXT,
            month TEXT,
            year TEXT,
            word_count INTEGER,
            char_count INTEGER,
            has_keywords TEXT
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON chats(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_role ON chats(role)")
    conn.commit()


def extract_keywords(text):
    """Extract simple keywords for filtering"""
    keywords = []
    text_lower = text.lower()

    # Insurance-related keywords
    insurance_words = [
        "insurance",
        "policy",
        "claim",
        "premium",
        "coverage",
        "hospital",
        "medical",
        "ircai",
        "sum insured",
        "deductible",
    ]
    for word in insurance_words:
        if word in text_lower:
            keywords.append(word)

    return ",".join(keywords)


def json_to_sql(json_file, db_file):
    """Convert JSON to SQL"""
    print(f"📂 Reading: {json_file}")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Handle {"messages": [...]} format
    if isinstance(data, dict) and "messages" in data:
        messages = data["messages"]
    else:
        messages = data

    print(f"📊 Found {len(messages)} messages")

    # Connect/create DB
    conn = sqlite3.connect(db_file)
    create_table(conn)

    # Clear existing data
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats")

    # Insert messages
    added = 0
    for msg in messages:
        content = msg.get("content", "")
        created_at = msg.get("created_at", "")

        # Extract date parts
        date = created_at[:10] if created_at else None
        month = created_at[:7] if created_at else None
        year = created_at[:4] if created_at else None

        # Features
        word_count = len(content.split())
        char_count = len(content)
        keywords = extract_keywords(content)

        cursor.execute(
            """
            INSERT INTO chats (role, content, created_at, date, month, year, word_count, char_count, has_keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                msg.get("role"),
                clean_text(content),
                created_at,
                date,
                month,
                year,
                word_count,
                char_count,
                keywords,
            ),
        )
        added += 1

    conn.commit()

    # Stats
    cursor.execute(
        "SELECT COUNT(*), AVG(word_count), MIN(created_at), MAX(created_at) FROM chats"
    )
    row = cursor.fetchone()
    print(f"\n✅ Added {row[0]} messages to {db_file}")
    print(f"📈 Avg words: {row[1]:.1f}")
    print(f"📅 From: {row[2]}")
    print(f"📅 To: {row[3]}")

    conn.close()
    print(f"\n🎉 SQL database ready: {db_file}")


def query_sample(db_file):
    """Show sample queries"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print("\n📊 Sample Queries:")
    print("-" * 50)

    # By date
    print("\n1. Messages by date:")
    cursor.execute("SELECT date, COUNT(*) FROM chats GROUP BY date ORDER BY date DESC")
    for row in cursor.fetchall():
        print(f"   {row[0]}: {row[1]} messages")

    # By role
    print("\n2. By role (user vs assistant):")
    cursor.execute("SELECT role, COUNT(*) FROM chats GROUP BY role")
    for row in cursor.fetchall():
        print(f"   {row[0]}: {row[1]}")

    # Search
    print("\n3. Search for 'insurance':")
    cursor.execute(
        "SELECT SUBSTR(content, 1, 80), date FROM chats WHERE has_keywords LIKE '%insurance%' LIMIT 3"
    )
    for row in cursor.fetchall():
        print(f"   [{row[1]}] {row[0]}...")

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Convert JSON to SQL")
    parser.add_argument("--db", default=DB_FILE, help="Output SQL database file")
    parser.add_argument("--query", action="store_true", help="Show sample queries")
    args = parser.parse_args()

    json_file = DATA_DIR / "latest.json"

    if not json_file.exists():
        print(f"❌ {json_file} not found. Run ./sync_chats.sh first")
        return

    if args.query:
        query_sample(args.db)
    else:
        json_to_sql(json_file, args.db)
        query_sample(args.db)


if __name__ == "__main__":
    main()
