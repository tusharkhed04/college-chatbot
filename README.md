# 🎓 CollegeBot — AI Chatbot for College Queries (MySQL Edition)

A full-stack AI chatbot using Flask + MySQL + modern dark UI.

---

## 📁 Project Structure

```
college_chatbot/
├── run.py                    ← Entry point
├── config.py                 ← MySQL credentials (edit this)
├── db_setup.py               ← Easy MySQL credential setup script
├── requirements.txt
├── schema.sql                ← Reference SQL schema
├── app/
│   ├── __init__.py           ← App factory (auto-creates DB)
│   ├── models/
│   │   ├── models.py         ← All database models
│   │   └── seed.py           ← Sample data (auto-seeded)
│   ├── routes/
│   │   ├── chat.py           ← /chat API (auth protected)
│   │   ├── auth.py           ← Login / Signup / Logout
│   │   ├── admin.py          ← Admin panel
│   │   └── main.py           ← Homepage
│   └── logic/
│       ├── nlp.py            ← Intent detection
│       ├── handlers.py       ← Query handlers
│       └── ai_handler.py     ← OpenAI integration
├── templates/
│   ├── index.html            ← Chat UI (auth gated)
│   └── admin.html            ← Admin panel
└── static/
    ├── css/style.css
    ├── css/admin.css
    └── js/app.js
```

---

## ⚙️ Setup Instructions

### Step 1 — Open MySQL Workbench
Make sure MySQL server is running.

### Step 2 — Open Terminal in Project Folder
```
cd D:\college_chatbot\college_chatbot
```

### Step 3 — Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 4 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Set Your MySQL Credentials

**Option A — Run the setup script (easiest):**
```bash
python db_setup.py
```
Enter your MySQL username, password, etc. when prompted.

**Option B — Edit config.py manually:**
Open `config.py` and change:
```python
MYSQL_USER     = "root"
MYSQL_PASSWORD = "your_password"
MYSQL_HOST     = "localhost"
MYSQL_PORT     = "3306"
MYSQL_DB       = "college_chatbot"
```

### Step 6 — Run the App
```bash
python run.py
```

The app will:
- ✅ Automatically CREATE the `college_chatbot` database in MySQL
- ✅ Create all tables
- ✅ Seed sample data (faculty, subjects, timetable, exams)
- ✅ Start server at http://localhost:5000

---

## 🌐 URLs

| URL | Description |
|-----|-------------|
| http://localhost:5000 | Chat (login required) |
| http://localhost:5000/admin | Admin panel |

---

## 🔑 Demo Login

| Email | Password |
|-------|----------|
| demo@college.edu | demo123 |

Admin password: `admin123`

---

## 🗄️ Verify Database in MySQL Workbench

After running the app, open MySQL Workbench and run:
```sql
USE college_chatbot;
SHOW TABLES;
SELECT * FROM faculty;
SELECT * FROM timetable;
SELECT * FROM students;
```

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, Flask 3.0 |
| Database | MySQL 8.0+ |
| ORM | Flask-SQLAlchemy + PyMySQL |
| Frontend | HTML5, CSS3, Vanilla JS |
| Auth | Session-based, Werkzeug hashing |
