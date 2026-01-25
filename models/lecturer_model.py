from typing import List
from models.course_model import Course
from models.student_model import Student


class Lecturer:
    def __init__(self, lecturer_id: str, user_id: int):
        self.lecturer_id = lecturer_id
        self.user_id = user_id

    def view_teaching_courses(self) -> List[Course]:
        """FR: View Teaching Courses"""
        pass

    def view_student_list(self, course: Course) -> List[Student]:
        """FR: View Registered Student List"""
        pass
