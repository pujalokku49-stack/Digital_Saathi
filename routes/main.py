"""Main public routes and API endpoints."""
import json
from pathlib import Path

from flask import Blueprint, jsonify, render_template, request, session

main_bp = Blueprint("main", __name__)

TRANSLATIONS_DIR = Path(__file__).resolve().parent.parent / "translations"


@main_bp.route("/")
def index():
    """Landing page."""
    return render_template("index.html")


@main_bp.route("/api/translations/<lang>")
def get_translations(lang):
    """Serve translation JSON for frontend i18n."""
    allowed = {"en", "hi", "te"}
    if lang not in allowed:
        lang = "en"

    file_path = TRANSLATIONS_DIR / f"{lang}.json"
    if not file_path.exists():
        file_path = TRANSLATIONS_DIR / "en.json"

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)


@main_bp.route("/api/set-language", methods=["POST"])
def set_language():
    """Update session language preference."""
    data = request.get_json(silent=True) or {}
    lang = data.get("language", "en")

    if lang in {"en", "hi", "te"}:
        session["language"] = lang
        return jsonify({"success": True, "language": lang})

    return jsonify({"success": False, "error": "Unsupported language"}), 400
