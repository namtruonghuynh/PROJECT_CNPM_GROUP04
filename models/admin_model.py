from .course_model import Course
from .user_model import User


class Administrator:
    def __init__(self, admin_id: str, user_id: int):
        self.admin_id = admin_id
        self.user_id = user_id

    def add_course(self, course: Course) -> None:
        """FR: Add Course"""
        pass

    def update_course(self, course: Course) -> None:
        """FR: Update Course"""
        pass

    def delete_course(self, course_id: int) -> None:
        """FR: Delete Course"""
        pass

    def assign_lecturer(self, course_id: int, lecturer_id: str) -> None:
        """FR: Assign Lecturer to Course"""
        pass

    def manage_registration_period(self) -> None:
        """FR: Manage Registration Period"""
        pass

    def manage_user_account(self, user: User) -> None:
        """FR: Manage User Accounts"""
        pass

    def view_reports(self):
        """FR: View Registration Reports"""
        pass
