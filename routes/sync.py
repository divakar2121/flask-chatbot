from flask import Blueprint, jsonify
from utils.database import (
    get_queue,
    mark_synced,
    increment_retry,
    get_queue_count,
    add_to_queue,
)
from utils.sync import sync_messages_to_cloud, check_connection, get_insforge_client

sync_bp = Blueprint("sync", __name__)


@sync_bp.route("/sync/status", methods=["GET"])
def sync_status():
    """Get sync status"""
    queue_count = get_queue_count()
    is_online = check_connection()
    is_configured = get_insforge_client()

    return jsonify(
        {
            "online": is_online,
            "configured": is_configured,
            "pending_count": queue_count,
            "ready": is_online and is_configured,
        }
    )


@sync_bp.route("/sync/upload", methods=["POST"])
def upload_sync():
    """Upload queued messages to cloud"""
    if not get_insforge_client():
        return jsonify({"error": "Cloud sync not configured"}), 400

    if not check_connection():
        return jsonify({"error": "No internet connection"}), 503

    queue = get_queue()
    if not queue:
        return jsonify({"status": "nothing to sync", "count": 0})

    # Sync to cloud
    success, message = sync_messages_to_cloud(queue)

    if success:
        ids = [msg["id"] for msg in queue]
        mark_synced(ids)
        return jsonify({"status": "synced", "count": len(queue)})
    else:
        ids = [msg["id"] for msg in queue]
        increment_retry(ids)
        return jsonify({"error": message}), 500


@sync_bp.route("/sync/queue/add", methods=["POST"])
def add_queue():
    """Manually add a message to sync queue"""
    from flask import request

    data = request.json
    if not data or not data.get("content"):
        return jsonify({"error": "Missing content"}), 400

    role = data.get("role", "user")
    add_to_queue(role, data["content"])
    return jsonify({"status": "queued"})
