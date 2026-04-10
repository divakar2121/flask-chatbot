#!/bin/bash
# Live chat monitor - fetches new messages in real-time
# Usage: ./live_monitor.sh [interval_seconds]

INTERVAL=${1:-5}
SERVER="https://my-dev--flsk-chtbt-th8v.diploi.me"
LAST_FILE="/tmp/last_fetch_time"
DATA_DIR="data/chat_history/live"
mkdir -p "$DATA_DIR"

echo "=========================================="
echo "🔴 HealthGuard AI - Live Monitor"
echo "=========================================="
echo "Watching for new messages every ${INTERVAL} seconds..."
echo "Press Ctrl+C to stop"
echo ""

# Load last fetch time
if [ -f "$LAST_FILE" ]; then
    LAST_TIME=$(cat "$LAST_FILE")
else
    LAST_TIME="2026-01-01"
fi

fetch_new() {
    # Get all messages
    curl -s "$SERVER/chat/history" | python3 -c "
import sys, json
from datetime import datetime

data = json.load(sys.stdin)
msgs = data.get('messages', [])
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Filter to today's messages
today = datetime.now().strftime('%Y-%m-%d')
new_msgs = [m for m in msgs if m.get('created_at', '').startswith(today)]

if new_msgs:
    print(f'📨 {len(new_msgs)} new messages today')
    for m in new_msgs[-5:]:
        preview = m['content'][:100].replace('\n', ' ')
        print(f\"  [{m['role']}] {m['created_at'][11:19]} | {preview}...\")
else:
    print('No new messages')
" 2>/dev/null
}

# Save current time
date +"%Y-%m-%d %H:%M:%S" > "$LAST_FILE"

while true; do
    fetch_new
    echo "⏳ Waiting ${INTERVAL}s..."
    sleep $INTERVAL
done