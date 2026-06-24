"""
Digital Saathi – Empowering Women & Elders through Technology
"""

import os
from dotenv import load_dotenv
from flask import Flask

from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# ensure db folder exists
os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)

@app.route("/")
def home():
    return "Digital Saathi is LIVE 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
