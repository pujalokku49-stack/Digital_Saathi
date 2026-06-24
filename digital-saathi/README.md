# Digital Saathi

**Empowering Women & Elders through Technology**

A modern full-stack web application built with Flask, SQLite, HTML/CSS/JavaScript featuring AI chatbot, voice assistant, multi-language support, and accessibility features.

---

## Features

- **User Authentication** – Secure login/register with validation
- **AI Chatbot** – ChatGPT API integration for digital literacy Q&A
- **Voice Assistant** – Speech-to-text and text-to-speech (Web Speech API)
- **Dashboard Modules** – Digital Literacy, Government Schemes, Online Safety, Healthcare
- **Admin Panel** – View users and chatbot usage statistics
- **Multi-language** – English, Hindi (हिन्दी), Telugu (తెలుగు)
- **Accessibility** – Large text mode, voice support, high contrast UI

---

## Project Structure

```
digital-saathi/
├── app.py                  # Flask application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── database/
│   ├── __init__.py
│   └── db.py               # SQLite schema & initialization
├── routes/
│   ├── auth.py             # Login, register, logout
│   ├── dashboard.py        # Dashboard & module pages
│   ├── chatbot.py          # AI chatbot API
│   ├── admin.py            # Admin panel
│   └── main.py             # Landing page & i18n API
├── utils/
│   ├── auth_helpers.py     # Login decorators
│   └── validators.py       # Form validation
├── templates/
│   ├── base.html           # Base layout
│   ├── index.html          # Landing page
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── chatbot.html
│   ├── modules/            # Learning modules
│   └── admin/              # Admin panel
├── static/
│   ├── css/style.css       # Custom styles
│   └── js/                 # i18n, chatbot, voice, main
└── translations/           # en.json, hi.json, te.json
```

---

## Setup & Run Locally

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Chrome browser (recommended for voice features)

### Step 1: Clone or navigate to project

```bash
cd digital-saathi
```

### Step 2: Create virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment

```bash
copy .env.example .env
```

Edit `.env` and set:
- `SECRET_KEY` – any random string for session security
- `OPENAI_API_KEY` – your OpenAI API key (optional; demo mode works without it)

### Step 5: Run the application

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## Default Admin Account

| Field    | Value                    |
|----------|--------------------------|
| Email    | admin@digitalsaathi.in   |
| Password | Admin@123                |

Use this to access the Admin Panel at `/admin`.

---

## Usage Guide

1. **Register** a new account or use the admin credentials
2. **Dashboard** – Choose a learning module
3. **AI Assistant** – Ask technology questions (type or use microphone)
4. **Language** – Switch between English, Hindi, Telugu from navbar
5. **Large Text** – Click the "A" button in navbar for elder-friendly font size
6. **Voice** – Click microphone in chatbot to speak your question

---

## API Endpoints

| Method | Endpoint              | Description              |
|--------|-----------------------|--------------------------|
| GET    | `/`                   | Landing page             |
| GET/POST | `/register`         | User registration        |
| GET/POST | `/login`              | User login               |
| GET    | `/logout`             | Logout                   |
| GET    | `/dashboard/`         | User dashboard           |
| GET    | `/chatbot/`           | AI chatbot page          |
| POST   | `/chatbot/ask`        | Send chat message (JSON) |
| GET    | `/admin/`             | Admin panel              |
| GET    | `/api/translations/<lang>` | Get i18n strings    |

---

## Tech Stack

- **Backend:** Python Flask, SQLite, Werkzeug
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **AI:** OpenAI ChatGPT API
- **Voice:** Web Speech API (browser-native)
- **Icons:** Bootstrap Icons

---

## License

Built for educational purposes – Digital Saathi Project.
