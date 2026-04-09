#!/bin/bash
# Convert JSON chat data to SQL database
# Usage: ./run_sql.sh
#
# Requires: Python 3 and json_to_sql.py
# Output: chat_data.db

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/json_to_sql.py"

echo "🔄 Converting JSON to SQL..."

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: $PYTHON_SCRIPT not found"
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/data/chat_history/latest.json" ]; then
    echo "⚠️  No chat data found. Downloading first..."
    ./sync_chats.sh
fi

python3 "$PYTHON_SCRIPT"

echo ""
echo "📊 Run queries with:"
echo "   sqlite3 chat_data.db"
echo "   or: python json_to_sql.py --query"