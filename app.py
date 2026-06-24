"""
Digital Saathi – Empowering Women & Elders through Technology
Main Flask application entry point.
"""
import os
from dotenv import load_dotenv
from flask import Flask

from config import Config

load_dotenv()


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure database directory exists
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)

    # ✅ ADD YOUR HOME ROUTE HERE
    @app.route("/")
    def home():
        return "Digital Saathi is LIVE 🚀"

    @app.context_processor
    def inject_globals():
        from flask import session

        return {
            "current_language": session.get("language", "en"),
            "user_name": session.get("user_name"),
            "is_logged_in": "user_id" in session,
            "is_admin": session.get("is_admin", False),
        }

    return app


# ✅ ONLY ONE APP INSTANCE
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
