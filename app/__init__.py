import os
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(32))
    CORS(app)

    from routes.main import main_bp
    from routes.chat import chat_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)

    return app
