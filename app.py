"""
Digital Saathi – Empowering Women & Elders through Technology
Main Flask application entry point.
"""
import os

from dotenv import load_dotenv
from flask import Flask

from config import Config
from database.db import init_db
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.chatbot import chatbot_bp
from routes.dashboard import dashboard_bp
from routes.main import main_bp

load_dotenv()


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure database directory exists
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)
    init_db()

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_globals():
        """Make common variables available in all templates."""
        from flask import session

        return {
            "current_language": session.get("language", "en"),
            "user_name": session.get("user_name"),
            "is_logged_in": "user_id" in session,
            "is_admin": session.get("is_admin", False),
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
