#!/bin/bash
# Download chat history from Diploi server
# Usage: ./sync_chats.sh
#
# Data saved to: data/chat_history/
#   data/chat_history/
#   ├── latest.json           # All chats (newest first)
#   ├── by_date/
#   │   └── 2026-04-09.json   # Chats by date
#   └── by_month/
#       └── 2026-04.json     # Chats by month

SERVER="https://my-dev--flsk-chtbt-th8v.diploi.me"
DATA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/data/chat_history"

echo "🔄 Fetching chat history from server..."

curl -s "$SERVER/chat/history" | python3 -c "
import sys, json
from pathlib import Path
from collections import defaultdict

data = json.load(sys.stdin)
messages = data.get('messages', [])
if not messages:
    print('No messages found')
    sys.exit(1)

# Create directories
by_date = Path('$DATA_DIR/by_date')
by_date.mkdir(parents=True, exist_ok=True)

by_month = Path('$DATA_DIR/by_month')
by_month.mkdir(parents=True, exist_ok=True)

# Save latest.json (all messages)
latest = Path('$DATA_DIR/latest.json')
with open(latest, 'w') as f:
    json.dump(messages, f, indent=2)

# Group by date and month
by_date_grouped = defaultdict(list)
by_month_grouped = defaultdict(list)

for m in messages:
    dt = m.get('created_at', '')
    date = dt[:10]      # 2026-04-09
    month = dt[:7]     # 2026-04
    by_date_grouped[date].append(m)
    by_month_grouped[month].append(m)

# Save by date
for date, msgs in by_date_grouped.items():
    filepath = by_date / f'{date}.json'
    with open(filepath, 'w') as f:
        json.dump(msgs, f, indent=2)
    print(f'📅 {date}: {len(msgs)} msgs')

# Save by month
for month, msgs in by_month_grouped.items():
    filepath = by_month / f'{month}.json'
    with open(filepath, 'w') as f:
        json.dump(msgs, f, indent=2)

print(f'📊 Total: {len(messages)} messages')
print('✅ Saved to data/chat_history/')
"