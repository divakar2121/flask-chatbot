#!/usr/bin/env python3
"""
Chat History Sync Tool
Fetches chat history from Diploi server and saves locally.
Usage: python sync_chats.py
"""

import requests
import json
import os
from datetime import datetime

SERVER_URL = os.environ.get("SERVER_URL", "https://my-dev--flsk-chtbt-th8v.diploi.me")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_chats():
    """Fetch all chat history from server"""
    url = f"{SERVER_URL}/chat/history"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json().get("messages", [])
    except Exception as e:
        print(f"Error fetching: {e}")
        return []


def save_json(messages):
    """Save messages to JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTPUT_DIR, f"chat_history_{timestamp}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(messages)} messages to {filepath}")
    return filepath


def save_latest(messages):
    """Save as chat_history_latest.json"""
    filepath = os.path.join(OUTPUT_DIR, "chat_history_latest.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    print(f"Updated chat_history_latest.json")
    return filepath


def print_summary(messages):
    """Print chat summary"""
    print(f"\n{'=' * 50}")
    print(f"Total conversations: {len(messages)}")
    print(f"\nRecent chats:")
    for msg in messages[:10]:
        preview = (
            msg["content"][:60] + "..." if len(msg["content"]) > 60 else msg["content"]
        )
        print(f"  [{msg['role']}] {msg['created_at']}: {preview}")


def main():
    print("Fetching chat history from server...")
    messages = fetch_chats()

    if messages:
        save_json(messages)
        save_latest(messages)
        print_summary(messages)

        # Print latest message
        latest = messages[0]
        print(f"\nLatest: {latest['created_at']}")
    else:
        print("No messages found")


if __name__ == "__main__":
    main()
