#!/usr/bin/env python3
"""
Chat History Sync Tool
Fetches chat history from Diploi server and saves locally in organized folder structure.

Folder Structure:
    chats/
    ├── 2026/
    │   ├── 04_april/
    │   │   ├── 2026-04-09.json    # All chats from that day
    │   │   └── 2026-04-08.json
    │   └── 03_march/
    │       └── ...
    └── latest.json                 # Always has newest data

Usage:
    python sync_chats.py              # Default - fetch & save
    python sync_chats.py --dry-run     # Just show, don't save
    python sync_chats.py --latest    # Save only latest.json
"""

import requests
import json
import os
import argparse
from datetime import datetime
from pathlib import Path

SERVER_URL = os.environ.get("SERVER_URL", "https://my-dev--flsk-chtbt-th8v.diploi.me")
SCRIPT_DIR = Path(__file__).parent.resolve()
CHATS_DIR = SCRIPT_DIR / "chats"


def get_month_name(month_num):
    """Convert month number to name"""
    names = {
        1: "january",
        2: "february",
        3: "march",
        4: "april",
        5: "may",
        6: "june",
        7: "july",
        8: "august",
        9: "september",
        10: "october",
        11: "november",
        12: "december",
    }
    return names.get(month_num, "unknown")


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


def group_by_date(messages):
    """Group messages by date (YYYY-MM-DD)"""
    grouped = {}
    for msg in messages:
        date = msg.get("created_at", "")[:10]  # "2026-04-09"
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(msg)
    return grouped


def save_to_folder(messages, dry_run=False):
    """Save messages in organized folder structure"""
    if not messages:
        print("No messages to save")
        return

    grouped = group_by_date(messages)
    total_saved = 0

    for date, msgs in sorted(grouped.items()):
        year, month_num, day = date.split("-")
        month = int(month_num)
        month_name = get_month_name(month)

        # Create folder: chats/2026/04_april/
        folder = CHATS_DIR / year / f"{month_num}_{month_name}"
        folder.mkdir(parents=True, exist_ok=True)

        filepath = folder / f"{date}.json"

        if dry_run:
            print(f"[DRY-RUN] Would save {len(msgs)} messages to {filepath}")
        else:
            # Read existing to merge
            existing = []
            if filepath.exists():
                with open(filepath, "r") as f:
                    existing = json.load(f)

            # Merge (avoid duplicates by id)
            existing_ids = {m.get("id") for m in existing if m.get("id")}
            new_msgs = [m for m in msgs if m.get("id") not in existing_ids]
            all_msgs = existing + new_msgs

            with open(filepath, "w") as f:
                json.dump(all_msgs, f, indent=2, ensure_ascii=False)

            total_saved += len(all_msgs)
            print(f"✅ Saved {len(all_msgs)} messages to {filepath.name}")

    # Save latest.json
    latest_path = CHATS_DIR / "latest.json"
    with open(latest_path, "w") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)
    print(f"✅ Updated latest.json ({len(messages)} messages)")

    return total_saved


def print_summary(messages):
    """Print chat summary"""
    print(f"\n{'=' * 50}")
    print(f"📊 Total messages: {len(messages)}")

    grouped = group_by_date(messages)
    print(f"\n📅 Messages by date:")
    for date, msgs in sorted(grouped.items(), reverse=True):
        print(f"   {date}: {len(msgs)} messages")

    print(f"\n💬 Latest conversation:")
    if messages:
        latest = messages[0]
        preview = (
            latest["content"][:50] + "..."
            if len(latest["content"]) > 50
            else latest["content"]
        )
        print(f"   [{latest['role']}] {latest['created_at']}")
        print(f'   "{preview}"')


def main():
    parser = argparse.ArgumentParser(description="Sync chat history from server")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be saved"
    )
    parser.add_argument("--latest", action="store_true", help="Save only latest.json")
    args = parser.parse_args()

    print("🔄 Fetching chat history from server...")
    messages = fetch_chats()

    if messages:
        if args.latest:
            # Just save latest.json
            latest_path = CHATS_DIR / "latest.json"
            with open(latest_path, "w") as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)
            print(f"✅ Updated latest.json ({len(messages)} messages)")
        else:
            save_to_folder(messages, dry_run=args.dry_run)
            print_summary(messages)
    else:
        print("❌ No messages found")


if __name__ == "__main__":
    main()
