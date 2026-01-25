class AcademicRecord:
    def __init__(self, record_id: int, student_id: str,
                 course_id: int, grade: float, semester: str):
        self.record_id = record_id
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade
        self.semester = semester
