from datetime import datetime


class Registration:
    def __init__(self, registration_id: int, student_id: str,
                 course_id: int, period_id: int, status: str):
        self.registration_id = registration_id
        self.student_id = student_id
        self.course_id = course_id
        self.period_id = period_id
        self.registration_date = datetime.now()
        self.status = status  # registered / dropped

    def create_registration(self) -> None:
        pass

    def cancel_registration(self) -> None:
        pass
