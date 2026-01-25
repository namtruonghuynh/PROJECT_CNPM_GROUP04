from typing import List
from models.course_model import Course

class Student:
    def __init__(self, student_id: str, user_id: int):
        self.student_id = student_id
        self.user_id = user_id

    def register_course(self, course: Course) -> bool:
        """FR: Register for a Course"""
        pass

    def drop_course(self, course: Course) -> bool:
        """FR: Drop a Registered Course"""
        pass

    def view_registered_courses(self) -> List[Course]:
        """FR: View Registered Courses"""
        pass

    def search_course(self, keyword: str) -> List[Course]:
        """FR: Search Courses"""
        pass
