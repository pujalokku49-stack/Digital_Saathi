"""Dashboard and learning module routes."""
from flask import Blueprint, render_template, session

from utils.auth_helpers import login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def home():
    """Main user dashboard with module cards."""
    return render_template(
        "dashboard.html",
        user_name=session.get("user_name"),
        is_admin=session.get("is_admin", False),
    )


@dashboard_bp.route("/literacy")
@login_required
def literacy():
    """Digital literacy tutorials module."""
    return render_template("modules/literacy.html")


@dashboard_bp.route("/schemes")
@login_required
def schemes():
    """Government schemes information module."""
    return render_template("modules/schemes.html")


@dashboard_bp.route("/safety")
@login_required
def safety():
    """Online safety tips module."""
    return render_template("modules/safety.html")


@dashboard_bp.route("/healthcare")
@login_required
def healthcare():
    """Healthcare and emergency help module."""
    return render_template("modules/healthcare.html")
