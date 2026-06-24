"""AI Chatbot routes with OpenAI integration and query logging."""
from datetime import datetime

from flask import Blueprint, jsonify, render_template, request, session

from config import Config
from database.db import get_db
from utils.auth_helpers import login_required

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")


SYSTEM_PROMPT = """You are Digital Saathi, a friendly and patient AI assistant helping women and elders in India with digital literacy.

Guidelines:
- Use simple, clear language without jargon
- Give step-by-step instructions when explaining technology
- Be culturally sensitive and supportive
- Focus on: smartphones, UPI, WhatsApp, government apps, online safety, telemedicine
- Keep answers concise (2-4 short paragraphs max)
- If asked about emergencies, always mention calling 112 (India emergency) or 108 (ambulance)
- Respond in the user's preferred language when possible"""


def get_ai_response(user_message, language="en"):
    """Call OpenAI API or return a helpful fallback response."""
    if not Config.OPENAI_API_KEY:
        return (
            "I'm Digital Saathi! (Demo mode – add OPENAI_API_KEY in .env for full AI responses)\n\n"
            f"You asked: \"{user_message}\"\n\n"
            "Here's a quick tip: To send a WhatsApp message, open WhatsApp, tap the green chat icon, "
            "select a contact, type your message, and tap the send arrow. "
            "For emergencies in India, dial 112 or 108."
        )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        lang_note = {"en": "English", "hi": "Hindi", "te": "Telugu"}.get(language, "English")

        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + f"\nPreferred response language: {lang_note}"},
                {"role": "user", "content": user_message},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f"Sorry, I couldn't connect to the AI service right now. Error: {exc}"


def save_query(user_id, query_text, response_text, language, source="chatbot"):
    """Persist chat query to SQLite."""
    conn = get_db()
    conn.execute(
        """
        INSERT INTO chat_queries (user_id, query_text, response_text, language, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, query_text, response_text, language, source, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


@chatbot_bp.route("/")
@login_required
def chat_page():
    """Render chatbot interface."""
    return render_template("chatbot.html")


@chatbot_bp.route("/ask", methods=["POST"])
@login_required
def ask():
    """Handle chatbot API requests."""
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    language = data.get("language") or session.get("language", "en")

    if not message:
        return jsonify({"error": "Message is required."}), 400

    if len(message) > 1000:
        return jsonify({"error": "Message too long (max 1000 characters)."}), 400

    response_text = get_ai_response(message, language)
    save_query(session["user_id"], message, response_text, language)

    return jsonify({"response": response_text, "language": language})
