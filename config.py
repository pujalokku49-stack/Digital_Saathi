"""Application configuration for Digital Saathi."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Flask configuration loaded from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "digital-saathi-dev-key-change-in-production")
    DATABASE = str(BASE_DIR / "database" / "saathi.db")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

    # Session cookie settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
