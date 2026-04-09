#!/bin/bash
# Complete Workflow: Download chats from server and convert to SQL
# Usage: ./sync_all.sh

cd "$(dirname "$0")"
SERVER="https://my-dev--flsk-chtbt-th8v.diploi.me"

echo "=============================================================="
echo "HealthGuard AI - Chat Sync Workflow"
echo "=============================================================="
echo ""

echo "Step 1: Downloading chats from server..."
mkdir -p data/chat_history/by_date data/chat_history/by_month

curl -s "$SERVER/chat/history" > data/chat_history/latest.json

python3 << 'PYSCRIPT'
import json
from pathlib import Path
from collections import defaultdict

with open('data/chat_history/latest.json') as f:
    messages = json.load(f).get('messages', [])

print(f'Downloaded {len(messages)} messages')

by_date = defaultdict(list)
by_month = defaultdict(list)

for m in messages:
    dt = m.get('created_at', '')
    date = dt[:10]
    month = dt[:7]
    by_date[date].append(m)
    by_month[month].append(m)

for date, msgs in by_date.items():
    Path(f'data/chat_history/by_date/{date}.json').write_text(json.dumps(msgs, indent=2))
    print(f'Saved {date}: {len(msgs)} msgs')

for month, msgs in by_month.items():
    Path(f'data/chat_history/by_month/{month}.json').write_text(json.dumps(msgs, indent=2))
PYSCRIPT

echo ""
echo "Step 2: Converting JSON to SQL..."
python3 json_to_sql.py

echo ""
echo "=============================================================="
echo "Workflow Complete!"
echo "=============================================================="
echo "Files: data/chat_history/latest.json, chat_data.db"
echo "Query: sqlite3 chat_data.db"