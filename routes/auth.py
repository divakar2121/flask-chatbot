from flask import Blueprint, request, jsonify, session, redirect, url_for
from utils.database import add_or_update_user, get_user, update_user_profile
import os
import hashlib

auth_bp = Blueprint("auth", __name__)

# Simple secret for sessions (in production, use proper secret)
SECRET_KEY = os.environ.get("SECRET_KEY", "healthguard-secret-key-2024")

# Google OAuth config (set in .env)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.environ.get(
    "GOOGLE_REDIRECT_URI", "http://127.0.0.1:5000/auth/callback"
)


def generate_token(email):
    """Generate simple session token"""
    return hashlib.sha256(f"{email}{SECRET_KEY}".encode()).hexdigest()[:32]


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """Simple email-based login (alternative to Google)"""
    data = request.json
    email = data.get("email", "").strip().lower()
    name = data.get("name", "")

    if not email or "@" not in email:
        return jsonify({"error": "Valid email required"}), 400

    # Generate simple token
    token = generate_token(email)

    # Upsert user
    add_or_update_user(google_id=token, email=email, name=name)

    return jsonify(
        {"token": token, "email": email, "name": name, "message": "Login successful"}
    )


@auth_bp.route("/auth/profile", methods=["GET", "POST"])
def profile():
    """Get or update user profile"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")

    if not token:
        return jsonify({"error": "Authorization required"}), 401

    user = get_user(token)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == "POST":
        data = request.json
        update_user_profile(
            google_id=token,
            name=data.get("name", user.get("name")),
            gender=data.get("gender"),
            age=data.get("age"),
            salary_range=data.get("salary_range"),
            phone=data.get("phone"),
            family_members=data.get("family_members"),
            family_ages=data.get("family_ages"),
        )
        return jsonify({"status": "Profile updated"})

    return jsonify(user)


@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    """Logout user"""
    return jsonify({"status": "logged out"})


@auth_bp.route("/auth/google")
def google_login():
    """Redirect to Google OAuth"""
    if not GOOGLE_CLIENT_ID:
        return jsonify({"error": "Google OAuth not configured"}), 500

    import requests

    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    return redirect(
        f"{google_auth_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    )


@auth_bp.route("/auth/callback")
def google_callback():
    """Handle Google OAuth callback"""
    code = request.args.get("code")
    if not code or not GOOGLE_CLIENT_ID:
        return redirect("/")

    # Exchange code for token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        resp = requests.post(token_url, data=data).json()
        access_token = resp.get("access_token")

        # Get user info
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()

        email = user_info.get("email")
        name = user_info.get("name")
        google_id = user_info.get("id")

        # Create session token
        session_token = generate_token(email)

        # Save user
        add_or_update_user(google_id=session_token, email=email, name=name)

        return jsonify({"token": session_token, "email": email, "name": name})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
