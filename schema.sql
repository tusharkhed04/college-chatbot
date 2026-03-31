-- CollegeBot Database Schema
-- SQLite compatible (also works with MySQL with minor type adjustments)

CREATE TABLE IF NOT EXISTS students (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256),
    branch      VARCHAR(50),
    year        INTEGER,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS faculty (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(100) NOT NULL,
    department  VARCHAR(80),
    subject     VARCHAR(100),
    email       VARCHAR(120),
    cabin       VARCHAR(30),
    phone       VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS subjects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(100) NOT NULL,
    code        VARCHAR(20) UNIQUE,
    branch      VARCHAR(50),
    year        INTEGER,
    semester    INTEGER,
    credits     INTEGER,
    faculty_id  INTEGER REFERENCES faculty(id)
);

CREATE TABLE IF NOT EXISTS timetable (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    branch      VARCHAR(50),
    year        INTEGER,
    day         VARCHAR(15),
    time_slot   VARCHAR(30),
    subject_id  INTEGER REFERENCES subjects(id),
    room        VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS exam_schedule (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    branch      VARCHAR(50),
    year        INTEGER,
    exam_type   VARCHAR(30),
    subject_id  INTEGER REFERENCES subjects(id),
    exam_date   VARCHAR(20),
    start_time  VARCHAR(10),
    room        VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS chat_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  VARCHAR(100),
    role        VARCHAR(10),
    message     TEXT,
    timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sample Data

INSERT INTO faculty (name, department, subject, email, cabin, phone) VALUES
('Dr. Priya Sharma',  'Computer Science', 'Data Structures',       'priya.sharma@college.edu',  'CS-101', '9876543210'),
('Prof. Rahul Mehta', 'Computer Science', 'Operating Systems',     'rahul.mehta@college.edu',   'CS-102', '9876543211'),
('Dr. Anita Desai',   'Computer Science', 'Database Management',   'anita.desai@college.edu',   'CS-103', '9876543212'),
('Prof. Suresh Patil','Computer Science', 'Computer Networks',     'suresh.patil@college.edu',  'CS-104', '9876543213'),
('Dr. Kavita Joshi',  'Mathematics',      'Engineering Mathematics','kavita.joshi@college.edu', 'MA-201', '9876543214'),
('Prof. Amit Kumar',  'Computer Science', 'Machine Learning',      'amit.kumar@college.edu',    'CS-105', '9876543215');

INSERT INTO subjects (name, code, branch, year, semester, credits, faculty_id) VALUES
('Data Structures',        'CS201', 'CSE', 2, 3, 4, 1),
('Operating Systems',      'CS301', 'CSE', 3, 5, 4, 2),
('Database Management',    'CS302', 'CSE', 3, 5, 3, 3),
('Computer Networks',      'CS401', 'CSE', 4, 7, 4, 4),
('Engineering Mathematics','MA101', 'CSE', 1, 1, 4, 5),
('Machine Learning',       'CS501', 'CSE', 3, 6, 4, 6);

INSERT INTO timetable (branch, year, day, time_slot, subject_id, room) VALUES
('CSE', 3, 'Monday',    '9:00-10:00',  2, 'CS-Lab1'),
('CSE', 3, 'Monday',    '10:00-11:00', 3, 'CS-202'),
('CSE', 3, 'Monday',    '11:30-12:30', 6, 'CS-203'),
('CSE', 3, 'Tuesday',   '9:00-10:00',  3, 'CS-202'),
('CSE', 3, 'Tuesday',   '10:00-11:00', 6, 'CS-203'),
('CSE', 3, 'Tuesday',   '11:30-12:30', 2, 'CS-Lab1'),
('CSE', 3, 'Wednesday', '9:00-10:00',  2, 'CS-Lab1'),
('CSE', 3, 'Wednesday', '10:00-11:00', 3, 'CS-202'),
('CSE', 3, 'Thursday',  '9:00-10:00',  6, 'CS-203'),
('CSE', 3, 'Thursday',  '10:00-11:00', 2, 'CS-Lab1'),
('CSE', 3, 'Friday',    '9:00-10:00',  3, 'CS-202'),
('CSE', 3, 'Friday',    '10:00-11:00', 6, 'CS-203'),
('CSE', 2, 'Monday',    '9:00-10:00',  1, 'CS-201'),
('CSE', 2, 'Monday',    '10:00-11:00', 5, 'CS-204'),
('CSE', 2, 'Tuesday',   '9:00-10:00',  5, 'CS-204'),
('CSE', 2, 'Wednesday', '9:00-10:00',  1, 'CS-201');

INSERT INTO exam_schedule (branch, year, exam_type, subject_id, exam_date, start_time, room) VALUES
('CSE', 3, 'Mid-Term', 2, '2024-03-10', '10:00', 'Exam Hall A'),
('CSE', 3, 'Mid-Term', 3, '2024-03-12', '10:00', 'Exam Hall B'),
('CSE', 3, 'Mid-Term', 6, '2024-03-14', '10:00', 'Exam Hall A'),
('CSE', 3, 'End-Term', 2, '2024-05-05', '10:00', 'Main Hall'),
('CSE', 3, 'End-Term', 3, '2024-05-08', '10:00', 'Main Hall'),
('CSE', 3, 'End-Term', 6, '2024-05-10', '10:00', 'Main Hall'),
('CSE', 2, 'Mid-Term', 1, '2024-03-11', '10:00', 'Exam Hall C'),
('CSE', 2, 'End-Term', 1, '2024-05-06', '10:00', 'Main Hall');
