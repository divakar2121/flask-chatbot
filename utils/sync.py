import os
import requests
import json
from typing import List, Dict, Any

# InsForge configuration
INSFORGE_BASE_URL = os.environ.get("INSFORGE_BASE_URL", "")
INSFORGE_ANON_KEY = os.environ.get("INSFORGE_ANON_KEY", "")
TABLE_NAME = "chat_messages"


def get_insforge_client():
    """Check if InsForge is configured"""
    return bool(INSFORGE_BASE_URL and INSFORGE_ANON_KEY)


def create_table_if_not_exists():
    """Create the chat_messages table in InsForge"""
    if not get_insforge_client():
        return False, "InsForge not configured"

    url = f"{INSFORGE_BASE_URL}/api/database/tables"
    payload = {
        "tableName": TABLE_NAME,
        "rlsEnabled": False,
        "columns": [
            {"name": "role", "type": "string", "nullable": False},
            {"name": "content", "type": "string", "nullable": False},
            {"name": "synced_at", "type": "string", "nullable": True},
            {"name": "device_id", "type": "string", "nullable": True},
        ],
    }

    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {INSFORGE_ANON_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        return response.status_code in (
            200,
            201,
        ) or "already exists" in response.text.lower(), response.text
    except Exception as e:
        return False, str(e)


def sync_messages_to_cloud(messages: List[Dict[str, Any]]) -> tuple[bool, str]:
    """Sync messages to InsForge cloud database"""
    if not get_insforge_client():
        return False, "InsForge not configured"

    if not messages:
        return True, "No messages to sync"

    url = f"{INSFORGE_BASE_URL}/api/database/{TABLE_NAME}"

    # Prepare data for bulk insert
    data = [
        {
            "role": msg["role"],
            "content": msg["content"],
            "synced_at": msg.get("created_at", ""),
            "device_id": "default",
        }
        for msg in messages
    ]

    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {INSFORGE_ANON_KEY}",
                "Content-Type": "application/json",
            },
            json=data,
            timeout=30,
        )

        if response.status_code in (200, 201):
            return True, f"Synced {len(messages)} messages"
        return False, f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return False, str(e)


def fetch_cloud_messages(limit: int = 100) -> tuple[List[Dict], str]:
    """Fetch messages from InsForge cloud"""
    if not get_insforge_client():
        return [], "InsForge not configured"

    url = f"{INSFORGE_BASE_URL}/api/database/{TABLE_NAME}?limit={limit}&order=created_at.desc"

    try:
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {INSFORGE_ANON_KEY}",
                "Content-Type": "application/json",
            },
            timeout=30,
        )

        if response.status_code == 200:
            return response.json().get("data", []), "Success"
        return [], f"Error: {response.status_code}"
    except Exception as e:
        return [], str(e)


def check_connection() -> bool:
    """Check if InsForge is reachable"""
    if not get_insforge_client():
        return False

    try:
        response = requests.get(
            INSFORGE_BASE_URL,
            headers={"Authorization": f"Bearer {INSFORGE_ANON_KEY}"},
            timeout=5,
        )
        return response.status_code == 200
    except:
        return False
