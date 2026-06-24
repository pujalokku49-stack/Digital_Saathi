"""Authentication routes: login, register, logout."""
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db
from utils.validators import validate_login, validate_registration

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration with server-side validation."""
    if session.get("user_id"):
        return redirect(url_for("dashboard.home"))

    errors = {}
    form_data = {"name": "", "email": "", "phone": "", "language": "en"}

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        phone = request.form.get("phone", "").strip()
        language = request.form.get("language", "en")

        form_data = {"name": name, "email": email, "phone": phone, "language": language}
        is_valid, errors = validate_registration(name, email, password, confirm_password, phone)

        if is_valid:
            conn = get_db()
            existing = conn.execute(
                "SELECT id FROM users WHERE email = ?", (email,)
            ).fetchone()

            if existing:
                errors["email"] = "An account with this email already exists."
            else:
                conn.execute(
                    """
                    INSERT INTO users (name, email, password_hash, phone, preferred_language, is_admin, created_at)
                    VALUES (?, ?, ?, ?, ?, 0, ?)
                    """,
                    (
                        name,
                        email,
                        generate_password_hash(password),
                        phone or None,
                        language,
                        datetime.utcnow().isoformat(),
                    ),
                )
                conn.commit()
                conn.close()
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("auth.login"))

            conn.close()

    return render_template("register.html", errors=errors, form_data=form_data)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login with session management."""
    if session.get("user_id"):
        return redirect(url_for("dashboard.home"))

    errors = {}
    form_data = {"email": ""}

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        form_data = {"email": email}

        is_valid, errors = validate_login(email, password)

        if is_valid:
            conn = get_db()
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            ).fetchone()
            conn.close()

            if user and check_password_hash(user["password_hash"], password):
                session.clear()
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["is_admin"] = bool(user["is_admin"])
                session["language"] = user["preferred_language"] or "en"
                flash(f"Welcome back, {user['name']}!", "success")
                return redirect(url_for("dashboard.home"))

            errors["general"] = "Invalid email or password."

    return render_template("login.html", errors=errors, form_data=form_data)


@auth_bp.route("/logout")
def logout():
    """Clear session and redirect to landing page."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))
