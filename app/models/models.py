from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    branch = db.Column(db.String(50))
    year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Faculty(db.Model):
    __tablename__ = "faculty"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(80))
    subject = db.Column(db.String(100))
    email = db.Column(db.String(120))
    cabin = db.Column(db.String(30))
    phone = db.Column(db.String(20))


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    branch = db.Column(db.String(50))
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    credits = db.Column(db.Integer)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
    faculty = db.relationship("Faculty", backref="subjects")


class Timetable(db.Model):
    __tablename__ = "timetable"
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(50))
    year = db.Column(db.Integer)
    day = db.Column(db.String(15))
    time_slot = db.Column(db.String(30))
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    subject = db.relationship("Subject", backref="slots")
    room = db.Column(db.String(20))


class ExamSchedule(db.Model):
    __tablename__ = "exam_schedule"
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(50))
    year = db.Column(db.Integer)
    exam_type = db.Column(db.String(30))
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    subject = db.relationship("Subject", backref="exams")
    exam_date = db.Column(db.String(20))
    start_time = db.Column(db.String(10))
    room = db.Column(db.String(20))


class ChatHistory(db.Model):
    __tablename__ = "chat_history"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    role = db.Column(db.String(10))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
