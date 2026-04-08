from flask import Blueprint, request, jsonify
from utils.openrouter import chat

chat_bp = Blueprint("chat", __name__)

messages = []


@chat_bp.route("/chat", methods=["POST"])
def chat():
    global messages
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    messages.append({"role": "user", "content": user_message})

    try:
        response = chat(messages)
        messages.append({"role": "assistant", "content": response})
        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_bp.route("/chat/reset", methods=["POST"])
def reset_chat():
    global messages
    messages = []
    return jsonify({"status": "chat reset"})
