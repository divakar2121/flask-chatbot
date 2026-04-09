from flask import Blueprint, request, jsonify
from utils.openrouter import chat as openrouter_chat
from utils.database import (
    add_message,
    get_messages,
    clear_messages,
    get_all_conversations,
    add_to_queue,
)
from utils.sync import check_connection, sync_messages_to_cloud

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    user_id = data.get("user_id") or request.headers.get("X-User-ID")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = openrouter_chat([{"role": "user", "content": user_message}])

        # Add to local DB with user_id
        add_message("user", user_message, user_id)
        add_message("assistant", response, user_id)

        # Queue for sync
        add_to_queue("user", user_message)
        add_to_queue("assistant", response)

        # Try immediate sync if online
        if check_connection():
            from utils.database import get_queue

            queue = get_queue()
            if queue:
                sync_messages_to_cloud(queue)

        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_bp.route("/chat/reset", methods=["POST"])
def reset_chat():
    user_id = request.headers.get("X-User-ID")
    clear_messages()
    return jsonify({"status": "chat reset"})


@chat_bp.route("/chat/conversations", methods=["GET"])
def list_conversations():
    user_id = request.headers.get("X-User-ID")
    conversations = get_all_conversations()
    return jsonify({"conversations": conversations})


@chat_bp.route("/chat/history", methods=["GET"])
def get_history():
    user_id = request.headers.get("X-User-ID")
    messages = get_messages(100, user_id)
    return jsonify({"messages": messages})
