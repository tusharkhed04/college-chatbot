from app.models.models import Faculty, Subject, Timetable, ExamSchedule
from app.logic.nlp import extract_day, extract_branch, extract_year


def handle_timetable(text, context):
    branch = extract_branch(text, context.get("branch"))
    year = extract_year(text, context.get("year"))
    day = extract_day(text)

    slots = Timetable.query.filter_by(branch=branch, year=year, day=day).order_by(Timetable.time_slot).all()
    if not slots:
        return f"No timetable found for {branch} Year {year} on {day}.", {"branch": branch, "year": year, "last_day": day}

    rows = "\n".join([f"  🕐 {s.time_slot}  |  {s.subject.name}  |  Room: {s.room}" for s in slots])
    response = f"📅 <b>Timetable — {branch} Year {year} | {day}</b>\n\n{rows}"
    return response, {"branch": branch, "year": year, "last_day": day}


def handle_syllabus(text, context):
    branch = extract_branch(text, context.get("branch"))
    year = extract_year(text, context.get("year"))

    subjects = Subject.query.filter_by(branch=branch, year=year).all()
    if not subjects:
        return f"No syllabus found for {branch} Year {year}.", {"branch": branch, "year": year}

    rows = "\n".join([f"  📘 {s.name} ({s.code}) — {s.credits} Credits | By: {s.faculty.name if s.faculty else 'TBA'}" for s in subjects])
    response = f"📚 <b>Syllabus — {branch} Year {year}</b>\n\n{rows}"
    return response, {"branch": branch, "year": year}


def handle_faculty(text, context):
    text_lower = text.lower()
    faculty = Faculty.query.all()

    matched = [f for f in faculty if f.name.lower().split()[-1] in text_lower
               or f.subject.lower() in text_lower
               or f.department.lower() in text_lower]

    if not matched:
        matched = faculty

    rows = "\n".join([
        f"  👤 <b>{f.name}</b>\n     Subject: {f.subject}\n     Cabin: {f.cabin}\n     Email: {f.email}\n     Phone: {f.phone}"
        for f in matched
    ])
    response = f"🎓 <b>Faculty Directory</b>\n\n{rows}"
    return response, {}


def handle_exam(text, context):
    branch = extract_branch(text, context.get("branch"))
    year = extract_year(text, context.get("year"))
    text_lower = text.lower()

    exam_type = None
    if "mid" in text_lower:
        exam_type = "Mid-Term"
    elif "end" in text_lower or "final" in text_lower:
        exam_type = "End-Term"

    query = ExamSchedule.query.filter_by(branch=branch, year=year)
    if exam_type:
        query = query.filter_by(exam_type=exam_type)
    exams = query.order_by(ExamSchedule.exam_date).all()

    if not exams:
        return f"No exam schedule found for {branch} Year {year}.", {"branch": branch, "year": year}

    rows = "\n".join([
        f"  📝 {e.subject.name} — {e.exam_type}\n     Date: {e.exam_date}  |  Time: {e.start_time}  |  Room: {e.room}"
        for e in exams
    ])
    response = f"📋 <b>Exam Schedule — {branch} Year {year}</b>\n\n{rows}"
    return response, {"branch": branch, "year": year}


def handle_greeting():
    return ("👋 Hello! I'm your College Assistant Bot.\n\n"
            "I can help you with:\n"
            "  📅 Timetable\n  📚 Syllabus\n  🎓 Faculty Info\n  📋 Exam Schedule\n\n"
            "What would you like to know?"), {}


def handle_farewell():
    return "👋 Goodbye! Feel free to chat anytime. Good luck with your studies! 🎓", {}


def handle_help():
    return ("🤖 <b>Here's what I can do:</b>\n\n"
            "  📅 <b>Timetable</b> — Ask: \"Show timetable for Monday\"\n"
            "  📚 <b>Syllabus</b> — Ask: \"What subjects do we have in Year 3?\"\n"
            "  🎓 <b>Faculty</b> — Ask: \"Who teaches Operating Systems?\"\n"
            "  📋 <b>Exams</b> — Ask: \"When is the mid-term exam?\"\n\n"
            "💡 <b>Tip:</b> I remember context! After asking about Monday's timetable, you can ask \"What about Tuesday?\""), {}
