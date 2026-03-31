from app import db
from app.models.models import Faculty, Subject, Timetable, ExamSchedule, Student


def seed_data():
    if Faculty.query.first():
        return

    faculty_list = [
        Faculty(name="Dr. Priya Sharma", department="Computer Science", subject="Data Structures", email="priya.sharma@college.edu", cabin="CS-101", phone="9876543210"),
        Faculty(name="Prof. Rahul Mehta", department="Computer Science", subject="Operating Systems", email="rahul.mehta@college.edu", cabin="CS-102", phone="9876543211"),
        Faculty(name="Dr. Anita Desai", department="Computer Science", subject="Database Management", email="anita.desai@college.edu", cabin="CS-103", phone="9876543212"),
        Faculty(name="Prof. Suresh Patil", department="Computer Science", subject="Computer Networks", email="suresh.patil@college.edu", cabin="CS-104", phone="9876543213"),
        Faculty(name="Dr. Kavita Joshi", department="Mathematics", subject="Engineering Mathematics", email="kavita.joshi@college.edu", cabin="MA-201", phone="9876543214"),
        Faculty(name="Prof. Amit Kumar", department="Computer Science", subject="Machine Learning", email="amit.kumar@college.edu", cabin="CS-105", phone="9876543215"),
    ]
    db.session.add_all(faculty_list)
    db.session.flush()

    subjects = [
        Subject(name="Data Structures", code="CS201", branch="CSE", year=2, semester=3, credits=4, faculty_id=faculty_list[0].id),
        Subject(name="Operating Systems", code="CS301", branch="CSE", year=3, semester=5, credits=4, faculty_id=faculty_list[1].id),
        Subject(name="Database Management", code="CS302", branch="CSE", year=3, semester=5, credits=3, faculty_id=faculty_list[2].id),
        Subject(name="Computer Networks", code="CS401", branch="CSE", year=4, semester=7, credits=4, faculty_id=faculty_list[3].id),
        Subject(name="Engineering Mathematics", code="MA101", branch="CSE", year=1, semester=1, credits=4, faculty_id=faculty_list[4].id),
        Subject(name="Machine Learning", code="CS501", branch="CSE", year=3, semester=6, credits=4, faculty_id=faculty_list[5].id),
    ]
    db.session.add_all(subjects)
    db.session.flush()

    timetable = [
        Timetable(branch="CSE", year=3, day="Monday", time_slot="9:00-10:00", subject_id=subjects[1].id, room="CS-Lab1"),
        Timetable(branch="CSE", year=3, day="Monday", time_slot="10:00-11:00", subject_id=subjects[2].id, room="CS-202"),
        Timetable(branch="CSE", year=3, day="Monday", time_slot="11:30-12:30", subject_id=subjects[5].id, room="CS-203"),
        Timetable(branch="CSE", year=3, day="Tuesday", time_slot="9:00-10:00", subject_id=subjects[2].id, room="CS-202"),
        Timetable(branch="CSE", year=3, day="Tuesday", time_slot="10:00-11:00", subject_id=subjects[5].id, room="CS-203"),
        Timetable(branch="CSE", year=3, day="Tuesday", time_slot="11:30-12:30", subject_id=subjects[1].id, room="CS-Lab1"),
        Timetable(branch="CSE", year=3, day="Wednesday", time_slot="9:00-10:00", subject_id=subjects[1].id, room="CS-Lab1"),
        Timetable(branch="CSE", year=3, day="Wednesday", time_slot="10:00-11:00", subject_id=subjects[2].id, room="CS-202"),
        Timetable(branch="CSE", year=3, day="Thursday", time_slot="9:00-10:00", subject_id=subjects[5].id, room="CS-203"),
        Timetable(branch="CSE", year=3, day="Thursday", time_slot="10:00-11:00", subject_id=subjects[1].id, room="CS-Lab1"),
        Timetable(branch="CSE", year=3, day="Friday", time_slot="9:00-10:00", subject_id=subjects[2].id, room="CS-202"),
        Timetable(branch="CSE", year=3, day="Friday", time_slot="10:00-11:00", subject_id=subjects[5].id, room="CS-203"),

        Timetable(branch="CSE", year=2, day="Monday", time_slot="9:00-10:00", subject_id=subjects[0].id, room="CS-201"),
        Timetable(branch="CSE", year=2, day="Monday", time_slot="10:00-11:00", subject_id=subjects[4].id, room="CS-204"),
        Timetable(branch="CSE", year=2, day="Tuesday", time_slot="9:00-10:00", subject_id=subjects[4].id, room="CS-204"),
        Timetable(branch="CSE", year=2, day="Wednesday", time_slot="9:00-10:00", subject_id=subjects[0].id, room="CS-201"),
    ]
    db.session.add_all(timetable)

    exams = [
        ExamSchedule(branch="CSE", year=3, exam_type="Mid-Term", subject_id=subjects[1].id, exam_date="2024-03-10", start_time="10:00", room="Exam Hall A"),
        ExamSchedule(branch="CSE", year=3, exam_type="Mid-Term", subject_id=subjects[2].id, exam_date="2024-03-12", start_time="10:00", room="Exam Hall B"),
        ExamSchedule(branch="CSE", year=3, exam_type="Mid-Term", subject_id=subjects[5].id, exam_date="2024-03-14", start_time="10:00", room="Exam Hall A"),
        ExamSchedule(branch="CSE", year=3, exam_type="End-Term", subject_id=subjects[1].id, exam_date="2024-05-05", start_time="10:00", room="Main Hall"),
        ExamSchedule(branch="CSE", year=3, exam_type="End-Term", subject_id=subjects[2].id, exam_date="2024-05-08", start_time="10:00", room="Main Hall"),
        ExamSchedule(branch="CSE", year=3, exam_type="End-Term", subject_id=subjects[5].id, exam_date="2024-05-10", start_time="10:00", room="Main Hall"),
        ExamSchedule(branch="CSE", year=2, exam_type="Mid-Term", subject_id=subjects[0].id, exam_date="2024-03-11", start_time="10:00", room="Exam Hall C"),
        ExamSchedule(branch="CSE", year=2, exam_type="End-Term", subject_id=subjects[0].id, exam_date="2024-05-06", start_time="10:00", room="Main Hall"),
    ]
    db.session.add_all(exams)

    demo_student = Student(name="Demo Student", email="demo@college.edu", branch="CSE", year=3)
    demo_student.set_password("demo123")
    db.session.add(demo_student)

    db.session.commit()
