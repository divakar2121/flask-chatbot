from flask import Blueprint, request, jsonify
from utils.openrouter import chat as openrouter_chat
from utils.database import (
    add_message,
    get_messages,
    clear_messages,
    get_all_conversations,
)

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = openrouter_chat([{"role": "user", "content": user_message}])
        add_message("user", user_message)
        add_message("assistant", response)
        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_bp.route("/chat/reset", methods=["POST"])
def reset_chat():
    clear_messages()
    return jsonify({"status": "chat reset"})


@chat_bp.route("/chat/conversations", methods=["GET"])
def list_conversations():
    conversations = get_all_conversations()
    return jsonify({"conversations": conversations})


@chat_bp.route("/chat/history", methods=["GET"])
def get_history():
    messages = get_messages(100)
    return jsonify({"messages": messages})
