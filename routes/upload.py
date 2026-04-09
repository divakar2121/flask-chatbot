import os
import uuid
from flask import Blueprint, request, jsonify

PdfReader = None
_pdf_error = "Unknown"

try:
    from pypdf import PdfReader

    _pdf_error = None
except ImportError as e:
    _pdf_error = f"pypdf not found: {e}"
    try:
        from PyPDF2 import PdfReader

        _pdf_error = None
    except ImportError as e2:
        _pdf_error = f"PyPDF2 also not found: {e2}"

from utils.openrouter import chat as openrouter_chat
from utils.database import add_message, get_messages, clear_messages

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "/app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

document_texts = {}


@upload_bp.route("/upload", methods=["POST"])
def upload_pdf():
    if PdfReader is None:
        return jsonify(
            {"error": f"PDF library not installed. Debug: {_pdf_error}"}
        ), 500

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    doc_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, f"{doc_id}.pdf")
    file.save(file_path)

    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        text = text.strip()
        if not text:
            return jsonify({"error": "Could not extract text from PDF"}), 400

        document_texts[doc_id] = text
        os.remove(file_path)

        summary = f"Document uploaded successfully! It contains {len(text)} characters. You can now ask me questions about this document."

        return jsonify(
            {"document_id": doc_id, "message": summary, "characters": len(text)}
        )
    except Exception as e:
        return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500


@upload_bp.route("/upload/chat", methods=["POST"])
def chat_with_document():
    data = request.json
    user_message = data.get("message", "")
    doc_id = data.get("document_id", "")
    mode = data.get(
        "mode", "analyst"
    )  # Default to analyst, can be "analyst" or "salesman"

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    if doc_id and doc_id in document_texts:
        context = f"Here's content from the uploaded document:\n\n{document_texts[doc_id][:8000]}\n\nBased on this document, please answer the following question:"
        prompt = f"{context}\n\nQuestion: {user_message}"
        messages = [{"role": "user", "content": prompt}]
    else:
        messages = [{"role": "user", "content": user_message}]

    try:
        response = openrouter_chat(messages, mode=mode)
        add_message("user", user_message)
        add_message("assistant", response)
        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@upload_bp.route("/upload/reset", methods=["POST"])
def reset_upload():
    document_texts.clear()
    return jsonify({"status": "upload reset"})
