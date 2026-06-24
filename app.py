"""
Digital Saathi – Empowering Women & Elders through Technology
Flask application entry point.
"""

import os

from dotenv import load_dotenv
from flask import Flask, session

from config import Config
from database.db import init_db
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.chatbot import chatbot_bp
from routes.dashboard import dashboard_bp
from routes.main import main_bp

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Ensure database directory exists before first connection
os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)


@app.context_processor
def inject_globals():
    """Make auth and language state available in all templates."""
    return {
        "is_logged_in": "user_id" in session,
        "user_name": session.get("user_name", ""),
        "is_admin": session.get("is_admin", False),
        "current_language": session.get("language", "en"),
    }


# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(admin_bp)

# Initialize database schema and seed admin user
init_db()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
