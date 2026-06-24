"""Admin panel routes for user and chatbot statistics."""
from flask import Blueprint, render_template

from database.db import get_db
from utils.auth_helpers import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def panel():
    """Admin dashboard with users list and chatbot usage stats."""
    conn = get_db()

    users = conn.execute(
        """
        SELECT id, name, email, phone, preferred_language, is_admin, created_at
        FROM users ORDER BY created_at DESC
        """
    ).fetchall()

    stats = conn.execute(
        """
        SELECT
            COUNT(*) AS total_queries,
            COUNT(DISTINCT user_id) AS unique_users,
            SUM(CASE WHEN date(created_at) = date('now') THEN 1 ELSE 0 END) AS today_queries
        FROM chat_queries
        """
    ).fetchone()

    recent_queries = conn.execute(
        """
        SELECT cq.id, cq.query_text, cq.response_text, cq.language, cq.created_at,
               u.name AS user_name, u.email AS user_email
        FROM chat_queries cq
        LEFT JOIN users u ON cq.user_id = u.id
        ORDER BY cq.created_at DESC
        LIMIT 20
        """
    ).fetchall()

    language_stats = conn.execute(
        """
        SELECT language, COUNT(*) AS count
        FROM chat_queries
        GROUP BY language
        ORDER BY count DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "admin/panel.html",
        users=users,
        stats=stats,
        recent_queries=recent_queries,
        language_stats=language_stats,
    )
