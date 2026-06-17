import os

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'digital-saathi-secret-key')

users = {}


def get_response(message):
    text = (message or "").strip().lower()

    if not text:
        return "Please tell me what you need help with."

    if any(word in text for word in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hi there! I'm here to help with payments, balance checks, loans, and anything else you need."

    if any(word in text for word in ["how do i pay", "how to pay", "pay bill", "make payment", "pay my bill", "pay the bill", "upi payment", "send money", "transfer money", "bank transfer", "transfer"]):
        return "You can do that by opening your UPI app or bank app, entering the amount, adding the receiver details, and then confirming the payment."

    if any(word in text for word in ["what is my balance", "check balance", "account balance", "how much money", "remaining money", "money left", "my balance", "balance check", "how much is left"]):
        return "You can check that from your bank app, the bank website, or your recent statement."

    if any(word in text for word in ["loan", "emi", "credit", "borrow", "interest", "loan details", "monthly installment", "repayment"]):
        return "For loan or EMI details, it is best to check your bank app or call support so they can explain it clearly."

    if any(word in text for word in ["call support", "call customer care", "call helpline", "support number", "customer care number", "contact support", "phone number", "can i call", "can i call you"]):
        return "You can call the support team at +91 1800 123 4567, or just use the Call Support button here."

    if any(word in text for word in ["whatsapp", "how to use whatsapp", "how do i use whatsapp", "use whatsapp", "chat on whatsapp", "message on whatsapp", "support on whatsapp", "how to open whatsapp"]):
        return "Sure, here's the easiest way: open WhatsApp, tap the chat icon, search for +91 99999 99999, and send a message like 'Hi, I need help.'"

    if any(word in text for word in ["what can you do", "who are you", "what do you do"]):
        return "I'm here to help with payments, balance checks, loans, EMI details, and general support questions."

    if any(word in text for word in ["help", "support", "customer care", "problem", "issue", "complaint", "unable", "not working", "can't", "cannot", "need help"]):
        return "Of course. Tell me exactly what is going wrong, and I'll guide you step by step."

    if any(word in text for word in ["talk to agent", "speak to agent", "talk to someone", "speak to someone", "can i talk to someone", "can i talk", "can i speak", "talk with someone", "speak with someone", "need a person", "human support", "representative", "agent", "human"]):
        return "Yes, absolutely. You can use the Talk to Agent button or the Call Support button for direct help."

    if "thank" in text or "thanks" in text:
        return "You're very welcome. I'm glad I could help."

    return (
        "I'm here to help with payments, balance checks, loan details, and support questions. "
        "If you tell me exactly what you need, I'll explain it in a simple way."
    )


@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html')


@app.route('/login')
def login_page():
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/register')
def register_page():
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if email not in users or not check_password_hash(users[email]['password'], password):
        return jsonify({"success": False, "message": "Invalid email or password."})

    session['user'] = users[email]['name']
    session['email'] = email
    return jsonify({"success": True, "message": "Login successful."})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not name or not email or not password:
        return jsonify({"success": False, "message": "All fields are required."})

    if email in users:
        return jsonify({"success": False, "message": "This email already exists."})

    users[email] = {
        'name': name,
        'password': generate_password_hash(password)
    }

    return jsonify({"success": True, "message": "Account created successfully. Please login."})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


@app.route('/ask', methods=['POST'])
def ask():
    if 'user' not in session:
        return jsonify({"response": "Please login first. Use the Login button above or create an account to continue."})

    user_input = request.json.get('message', '')
    response = get_response(user_input)
    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)