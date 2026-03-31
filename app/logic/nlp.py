import re
from datetime import datetime

INTENTS = {
    "timetable": ["timetable", "class", "classes", "lecture", "lectures", "today", "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday", "period", "timing", "time table"],
    "syllabus": ["syllabus", "subject", "subjects", "curriculum", "course", "semester", "topics", "what do we study"],
    "faculty": ["faculty", "teacher", "professor", "instructor", "who teaches", "staff", "dr.", "prof.", "hod", "head"],
    "exam": ["exam", "examination", "test", "mid-term", "midterm", "end-term", "endterm", "viva", "practical", "date sheet", "exam schedule", "schedule"],
    "greeting": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "namaste"],
    "farewell": ["bye", "goodbye", "see you", "thanks", "thank you", "exit", "quit"],
    "help": ["help", "what can you do", "features", "options", "commands"],
}

DAY_MAP = {
    "monday": "Monday", "tuesday": "Tuesday", "wednesday": "Wednesday",
    "thursday": "Thursday", "friday": "Friday", "today": None, "tomorrow": None,
}

BRANCH_KEYWORDS = {
    "cse": "CSE", "computer science": "CSE", "it": "IT", "information technology": "IT",
    "mech": "MECH", "mechanical": "MECH", "civil": "CIVIL", "entc": "ENTC",
}


def detect_intent(text):
    text_lower = text.lower()
    scores = {intent: 0 for intent in INTENTS}
    for intent, keywords in INTENTS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[intent] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "unknown"


def extract_day(text):
    text_lower = text.lower()
    today = datetime.now().strftime("%A")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for key, val in DAY_MAP.items():
        if key in text_lower:
            if key == "today":
                return today
            elif key == "tomorrow":
                idx = days.index(today)
                return days[(idx + 1) % 7]
            return val
    return today


def extract_branch(text, session_branch=None):
    text_lower = text.lower()
    for kw, branch in BRANCH_KEYWORDS.items():
        if kw in text_lower:
            return branch
    return session_branch or "CSE"


def extract_year(text, session_year=None):
    match = re.search(r'\b([1-4])(st|nd|rd|th)?\s*(year)?\b', text.lower())
    if match:
        return int(match.group(1))
    return session_year or 3


def resolve_context(text, context):
    text_lower = text.lower()
    follow_up_words = ["what about", "and", "also", "same for", "how about", "tomorrow", "next day"]
    is_follow_up = any(w in text_lower for w in follow_up_words) and len(text.split()) <= 6

    if is_follow_up and context.get("last_intent"):
        return context["last_intent"]
    return None
