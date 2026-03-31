from flask import Blueprint, request, jsonify, render_template, session
from app.models.models import Timetable, Faculty, Subject, ExamSchedule
from app import db
from functools import wraps

admin_bp = Blueprint("admin", __name__)

ADMIN_PASSWORD = "admin123"


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/admin")
def admin_panel():
    return render_template("admin.html")


@admin_bp.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    if data.get("password") == ADMIN_PASSWORD:
        session["is_admin"] = True
        return jsonify({"success": True})
    return jsonify({"error": "Wrong password"}), 401


@admin_bp.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("is_admin", None)
    return jsonify({"success": True})


# ── TIMETABLE ────────────────────────────────────────────────────────

@admin_bp.route("/admin/timetable", methods=["GET"])
@admin_required
def get_timetable():
    year = request.args.get("year", type=int)
    query = Timetable.query
    if year:
        query = query.filter_by(year=year)
    rows = query.order_by(Timetable.year, Timetable.day, Timetable.time_slot).all()
    return jsonify([{
        "id": r.id, "branch": r.branch, "year": r.year,
        "day": r.day, "time_slot": r.time_slot,
        "subject_id": r.subject_id,
        "subject": r.subject.name if r.subject else "",
        "room": r.room
    } for r in rows])


@admin_bp.route("/admin/timetable", methods=["POST"])
@admin_required
def add_timetable():
    data = request.get_json()
    subject = Subject.query.get(int(data.get("subject_id", 0)))
    if not subject:
        return jsonify({"error": "Subject not found"}), 404
    row = Timetable(
        branch=data["branch"], year=int(data["year"]),
        day=data["day"], time_slot=data["time_slot"],
        subject_id=subject.id, room=data["room"]
    )
    db.session.add(row)
    db.session.commit()
    return jsonify({"message": "Added", "id": row.id})


@admin_bp.route("/admin/timetable/<int:row_id>", methods=["PUT"])
@admin_required
def update_timetable(row_id):
    row = Timetable.query.get_or_404(row_id)
    data = request.get_json()
    if "branch"     in data: row.branch    = data["branch"]
    if "year"       in data: row.year      = int(data["year"])
    if "day"        in data: row.day       = data["day"]
    if "time_slot"  in data: row.time_slot = data["time_slot"]
    if "room"       in data: row.room      = data["room"]
    if "subject_id" in data:
        subj = Subject.query.get(int(data["subject_id"]))
        if subj:
            row.subject_id = subj.id
    db.session.commit()
    return jsonify({"message": "Updated"})


@admin_bp.route("/admin/timetable/<int:row_id>", methods=["DELETE"])
@admin_required
def delete_timetable(row_id):
    row = Timetable.query.get_or_404(row_id)
    db.session.delete(row)
    db.session.commit()
    return jsonify({"message": "Deleted"})


# ── FACULTY ──────────────────────────────────────────────────────────

@admin_bp.route("/admin/faculty", methods=["GET"])
@admin_required
def get_faculty():
    rows = Faculty.query.order_by(Faculty.name).all()
    return jsonify([{
        "id": f.id, "name": f.name, "department": f.department,
        "subject": f.subject, "email": f.email,
        "cabin": f.cabin, "phone": f.phone
    } for f in rows])


@admin_bp.route("/admin/faculty", methods=["POST"])
@admin_required
def add_faculty():
    data = request.get_json()
    f = Faculty(
        name=data.get("name", ""),
        department=data.get("department", ""),
        subject=data.get("subject", ""),
        email=data.get("email", ""),
        cabin=data.get("cabin", ""),
        phone=data.get("phone", ""),
    )
    db.session.add(f)
    db.session.commit()
    return jsonify({"message": "Added", "id": f.id})


@admin_bp.route("/admin/faculty/<int:fid>", methods=["PUT"])
@admin_required
def update_faculty(fid):
    f = Faculty.query.get_or_404(fid)
    data = request.get_json()
    for field in ["name", "department", "subject", "email", "cabin", "phone"]:
        if field in data:
            setattr(f, field, data[field])
    db.session.commit()
    return jsonify({"message": "Updated"})


@admin_bp.route("/admin/faculty/<int:fid>", methods=["DELETE"])
@admin_required
def delete_faculty(fid):
    f = Faculty.query.get_or_404(fid)
    db.session.delete(f)
    db.session.commit()
    return jsonify({"message": "Deleted"})


# ── SYLLABUS (SUBJECTS) ──────────────────────────────────────────────

@admin_bp.route("/admin/syllabus", methods=["GET"])
@admin_required
def get_syllabus():
    year = request.args.get("year", type=int)
    query = Subject.query
    if year:
        query = query.filter_by(year=year)
    rows = query.order_by(Subject.year, Subject.name).all()
    return jsonify([{
        "id": s.id, "name": s.name, "code": s.code,
        "branch": s.branch, "year": s.year,
        "semester": s.semester, "credits": s.credits,
        "faculty_id": s.faculty_id,
        "faculty": s.faculty.name if s.faculty else "Not Assigned"
    } for s in rows])


@admin_bp.route("/admin/syllabus", methods=["POST"])
@admin_required
def add_syllabus():
    data = request.get_json()
    s = Subject(
        name=data.get("name", ""),
        code=data.get("code", ""),
        branch=data.get("branch", "CSE"),
        year=int(data.get("year", 1)),
        semester=int(data.get("semester", 1)),
        credits=int(data.get("credits", 3)),
        faculty_id=data.get("faculty_id") or None,
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({"message": "Added", "id": s.id})


@admin_bp.route("/admin/syllabus/<int:sid>", methods=["PUT"])
@admin_required
def update_syllabus(sid):
    s = Subject.query.get_or_404(sid)
    data = request.get_json()
    if "name"       in data: s.name       = data["name"]
    if "code"       in data: s.code       = data["code"]
    if "branch"     in data: s.branch     = data["branch"]
    if "year"       in data: s.year       = int(data["year"])
    if "semester"   in data: s.semester   = int(data["semester"])
    if "credits"    in data: s.credits    = int(data["credits"])
    if "faculty_id" in data: s.faculty_id = data["faculty_id"] or None
    db.session.commit()
    return jsonify({"message": "Updated"})


@admin_bp.route("/admin/syllabus/<int:sid>", methods=["DELETE"])
@admin_required
def delete_syllabus(sid):
    s = Subject.query.get_or_404(sid)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"message": "Deleted"})


# ── EXAM SCHEDULE ────────────────────────────────────────────────────

@admin_bp.route("/admin/exams", methods=["GET"])
@admin_required
def get_exams():
    year = request.args.get("year", type=int)
    query = ExamSchedule.query
    if year:
        query = query.filter_by(year=year)
    rows = query.order_by(ExamSchedule.year, ExamSchedule.exam_date).all()
    return jsonify([{
        "id": e.id, "branch": e.branch, "year": e.year,
        "exam_type": e.exam_type,
        "subject_id": e.subject_id,
        "subject": e.subject.name if e.subject else "",
        "exam_date": e.exam_date,
        "start_time": e.start_time, "room": e.room
    } for e in rows])


@admin_bp.route("/admin/exams", methods=["POST"])
@admin_required
def add_exam():
    data = request.get_json()
    subj = Subject.query.get(int(data.get("subject_id", 0)))
    if not subj:
        return jsonify({"error": "Subject not found"}), 404
    e = ExamSchedule(
        branch=data.get("branch", "CSE"),
        year=int(data.get("year", 1)),
        exam_type=data.get("exam_type", "Mid-Term"),
        subject_id=subj.id,
        exam_date=data.get("exam_date", ""),
        start_time=data.get("start_time", "10:00"),
        room=data.get("room", ""),
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({"message": "Added", "id": e.id})


@admin_bp.route("/admin/exams/<int:eid>", methods=["PUT"])
@admin_required
def update_exam(eid):
    e = ExamSchedule.query.get_or_404(eid)
    data = request.get_json()
    if "branch"     in data: e.branch     = data["branch"]
    if "year"       in data: e.year       = int(data["year"])
    if "exam_type"  in data: e.exam_type  = data["exam_type"]
    if "exam_date"  in data: e.exam_date  = data["exam_date"]
    if "start_time" in data: e.start_time = data["start_time"]
    if "room"       in data: e.room       = data["room"]
    if "subject_id" in data:
        subj = Subject.query.get(int(data["subject_id"]))
        if subj: e.subject_id = subj.id
    db.session.commit()
    return jsonify({"message": "Updated"})


@admin_bp.route("/admin/exams/<int:eid>", methods=["DELETE"])
@admin_required
def delete_exam(eid):
    e = ExamSchedule.query.get_or_404(eid)
    db.session.delete(e)
    db.session.commit()
    return jsonify({"message": "Deleted"})


# ── SHARED HELPERS ───────────────────────────────────────────────────

@admin_bp.route("/admin/subjects-list", methods=["GET"])
@admin_required
def subjects_list():
    rows = Subject.query.order_by(Subject.name).all()
    return jsonify([{"id": s.id, "name": s.name, "year": s.year} for s in rows])


@admin_bp.route("/admin/faculty-list", methods=["GET"])
@admin_required
def faculty_list():
    rows = Faculty.query.order_by(Faculty.name).all()
    return jsonify([{"id": f.id, "name": f.name} for f in rows])
