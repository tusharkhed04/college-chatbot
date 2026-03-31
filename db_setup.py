"""
Run this script ONCE to set your MySQL credentials.
It will update config.py automatically.

Usage:
    python db_setup.py
"""

import re

print("=" * 50)
print("  CollegeBot — MySQL Setup")
print("=" * 50)
print()

user     = input("MySQL Username (default: root): ").strip() or "root"
password = input("MySQL Password (leave blank if none): ").strip()
host     = input("MySQL Host (default: localhost): ").strip() or "localhost"
port     = input("MySQL Port (default: 3306): ").strip() or "3306"
db_name  = input("Database name (default: college_chatbot): ").strip() or "college_chatbot"

config_content = f'''import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "college-chatbot-secret-2024")

    # ── MySQL Configuration ──────────────────────────────────────────
    MYSQL_USER     = "{user}"
    MYSQL_PASSWORD = "{password}"
    MYSQL_HOST     = "{host}"
    MYSQL_PORT     = "{port}"
    MYSQL_DB       = "{db_name}"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{{MYSQL_USER}}:{{MYSQL_PASSWORD}}"
        f"@{{MYSQL_HOST}}:{{MYSQL_PORT}}/{{MYSQL_DB}}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    SESSION_PERMANENT = False
'''

with open("config.py", "w", encoding="utf-8") as f:
    f.write(config_content)

print()
print("✅ config.py updated with your MySQL credentials!")
print()
print("Now run:  python run.py")
print()
