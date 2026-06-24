# Digital Saathi

**Empowering Women & Elders through Technology**

A modern full-stack web application built with Flask, SQLite, HTML/CSS/JavaScript featuring AI chatbot, voice assistant, multi-language support, and accessibility features.

---

## Features

- **User Authentication** – Secure login/register with server-side validation
- **AI Chatbot** – ChatGPT API integration for digital literacy Q&A (demo mode without API key)
- **Voice Assistant** – Speech-to-text and text-to-speech via Web Speech API
- **Dashboard Modules** – Digital Literacy, Government Schemes, Online Safety, Healthcare
- **Admin Panel** – View users and chatbot usage statistics
- **Multi-language** – English, Hindi (हिन्दी), Telugu (తెలుగు)
- **Accessibility** – Large text mode, voice support, skip links, ARIA labels

---

## Project Structure

```
.
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

### Step 1: Navigate to project folder

```bash
cd "New folder"
```

### Step 2: Create virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
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

**Windows:**
```powershell
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
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

1. **Register** a new account or use the admin credentials above
2. **Dashboard** – Choose a learning module (Literacy, Schemes, Safety, Healthcare)
3. **AI Assistant** – Ask technology questions (type or use the microphone)
4. **Language** – Switch between English, Hindi, Telugu from the navbar
5. **Large Text** – Click the **A** button in the navbar for elder-friendly font size
6. **Voice** – Click the microphone in the chatbot to speak your question

---

## API Endpoints

| Method | Endpoint                   | Description              |
|--------|----------------------------|--------------------------|
| GET    | `/`                        | Landing page             |
| GET/POST | `/register`              | User registration        |
| GET/POST | `/login`                 | User login               |
| GET    | `/logout`                  | Logout                   |
| GET    | `/dashboard/`              | User dashboard           |
| GET    | `/chatbot/`                | AI chatbot page          |
| POST   | `/chatbot/ask`             | Send chat message (JSON) |
| GET    | `/admin/`                  | Admin panel              |
| GET    | `/api/translations/<lang>` | Get i18n strings         |
| POST   | `/api/set-language`        | Update session language  |

---

## Tech Stack

- **Backend:** Python Flask, SQLite, Werkzeug
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **AI:** OpenAI ChatGPT API
- **Voice:** Web Speech API (browser-native)
- **Icons:** Bootstrap Icons

---

## Deployment

Your repo is already on GitHub: `https://github.com/pujalokku49-stack/Digital_Saathi.git`

The project includes **Render** config (`render.yaml`, `Procfile`, `runtime.txt`) and uses **Gunicorn** for production.

### Option A: Render (recommended, free tier)

1. **Push latest code to GitHub**
   ```powershell
   git add .
   git commit -m "Add deployment config"
   git push origin main
   ```

2. **Create a Render account** at [render.com](https://render.com) and connect GitHub.

3. **Deploy via Blueprint**
   - Dashboard → **New** → **Blueprint**
   - Select the `Digital_Saathi` repo
   - Render reads `render.yaml` automatically

4. **Set environment variables** in the Render dashboard:
   | Variable | Value |
   |----------|-------|
   | `SECRET_KEY` | Auto-generated (or your own random string) |
   | `OPENAI_API_KEY` | Your OpenAI key (optional) |
   | `FLASK_DEBUG` | `0` |

5. **Deploy** – Render builds with `pip install -r requirements.txt` and starts:
   ```
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```

6. Your live URL will look like: `https://digital-saathi.onrender.com`

### Option B: Manual Render Web Service

If you prefer not to use the Blueprint:

| Setting | Value |
|---------|-------|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |
| Python Version | `3.11.9` |

### Option C: Railway / Heroku

Both support the included `Procfile`:

```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

Connect the GitHub repo, set the same env vars, and deploy.

### Important: SQLite on cloud hosts

On **free-tier** Render/Railway, the filesystem is **ephemeral** — the SQLite database resets when the app redeploys or restarts. For a demo or class project this is fine (admin user is re-seeded automatically).

For **persistent production data**, upgrade to:
- Render **Persistent Disk** mounted at `/data`, with `DATABASE=/data/saathi.db`, or
- **PostgreSQL** (Render/Railway free DB tier) — requires a small code change to swap SQLite for Postgres.

### Production checklist

- [ ] Set a strong `SECRET_KEY` (never use the dev default)
- [ ] Set `FLASK_DEBUG=0`
- [ ] Add `OPENAI_API_KEY` for live AI responses
- [ ] Change the default admin password after first login
- [ ] Use HTTPS (Render provides this automatically)

---

## License

Built for educational purposes – Digital Saathi Project.
