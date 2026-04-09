import os
from flask import Blueprint, jsonify, render_template, send_from_directory

main_bp = Blueprint("main", __name__)

STATIC_PATH = "/app/static"


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/health")
def health():
    return jsonify({"status": "healthy"})


@main_bp.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(STATIC_PATH, filename)
