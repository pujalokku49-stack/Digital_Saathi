"""Input validation helpers."""
import re

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")


def validate_registration(name, email, password, confirm_password, phone=None):
    """Validate registration form fields. Returns (is_valid, errors dict)."""
    errors = {}

    if not name or len(name.strip()) < 2:
        errors["name"] = "Name must be at least 2 characters."

    if not email or not EMAIL_PATTERN.match(email.strip()):
        errors["email"] = "Please enter a valid email address."

    if not password or len(password) < 8:
        errors["password"] = "Password must be at least 8 characters."

    if password != confirm_password:
        errors["confirm_password"] = "Passwords do not match."

    if phone and phone.strip() and not PHONE_PATTERN.match(phone.strip()):
        errors["phone"] = "Enter a valid 10-digit Indian mobile number."

    return len(errors) == 0, errors


def validate_login(email, password):
    """Validate login form fields."""
    errors = {}

    if not email or not EMAIL_PATTERN.match(email.strip()):
        errors["email"] = "Please enter a valid email address."

    if not password:
        errors["password"] = "Password is required."

    return len(errors) == 0, errors
