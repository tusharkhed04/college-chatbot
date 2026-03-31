from flask import Blueprint, request, jsonify, session
from app.models.models import Student
from app import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if Student.query.filter_by(email=data.get("email")).first():
        return jsonify({"error": "Email already registered"}), 400
    student = Student(
        name=data.get("name"),
        email=data.get("email"),
        branch=data.get("branch", "CSE"),
        year=int(data.get("year", 1)),
    )
    student.set_password(data.get("password"))
    db.session.add(student)
    db.session.commit()
    session["user_id"] = student.id
    session["user_name"] = student.name
    session.setdefault("context", {})["branch"] = student.branch
    session["context"]["year"] = student.year
    return jsonify({"message": "Account created", "name": student.name, "branch": student.branch, "year": student.year})


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    student = Student.query.filter_by(email=data.get("email")).first()
    if not student or not student.check_password(data.get("password", "")):
        return jsonify({"error": "Invalid credentials"}), 401
    session["user_id"] = student.id
    session["user_name"] = student.name
    session.setdefault("context", {})["branch"] = student.branch
    session["context"]["year"] = student.year
    return jsonify({"message": "Logged in", "name": student.name, "branch": student.branch, "year": student.year})


@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@auth_bp.route("/auth/me", methods=["GET"])
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"logged_in": False})
    student = Student.query.get(user_id)
    if not student:
        return jsonify({"logged_in": False})
    return jsonify({"logged_in": True, "name": student.name, "branch": student.branch, "year": student.year})
