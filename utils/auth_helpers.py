"""Authentication route helpers and decorators."""
from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(view):
    """Require authenticated user for a route."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    """Require admin user for a route."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        if not session.get("is_admin"):
            flash("Admin access required.", "danger")
            return redirect(url_for("dashboard.home"))
        return view(*args, **kwargs)

    return wrapped
