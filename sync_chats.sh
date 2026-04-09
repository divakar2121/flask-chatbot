#!/bin/bash
# Download chat history from Diploi server
# Usage: ./sync_chats.sh

SERVER="https://my-dev--flsk-chtbt-th8v.diploi.me"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔄 Fetching chat history from server..."

# Month names array
MONTHS=("" "jan" "feb" "mar" "apr" "may" "jun" "jul" "aug" "sep" "oct" "nov" "dec")

# Fetch and save to chats/latest.json
curl -s "$SERVER/chat/history" | python3 -c "
import sys, json
from pathlib import Path
from collections import defaultdict

data = json.load(sys.stdin)
messages = data.get('messages', [])
if not messages:
    print('No messages found')
    sys.exit(1)

# Save latest.json
latest = Path('chats/latest.json')
latest.parent.mkdir(exist_ok=True)
with open(latest, 'w') as f:
    json.dump(messages, f, indent=2)

# Group by date and save
grouped = defaultdict(list)
for m in messages:
    date = m.get('created_at', '')[:10]
    grouped[date].append(m)

month_names = ['', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

for date, msgs in grouped.items():
    year, month_num, day = date.split('-')
    month = month_names[int(month_num)]
    folder = Path(f'chats/{year}/{month_num}_{month}')
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / f'{date}.json'
    with open(filepath, 'w') as f:
        json.dump(msgs, f, indent=2)
    print(f'✅ {date}: {len(msgs)} messages')

print(f'📊 Total: {len(messages)} messages')
print('✅ Saved to chats/ folder')
"