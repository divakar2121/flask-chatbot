import os
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(32))
    CORS(app)

    from routes.main import main_bp
    from routes.chat import chat_bp
    from routes.upload import upload_bp
    from routes.sync import sync_bp
    from routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(sync_bp)
    app.register_blueprint(auth_bp)

    return app


app = create_app()
