class Course:
    def __init__(self, course_id: int, course_code: str, course_name: str,
                 credits: int, max_capacity: int, schedule: str,
                 department: str, status: str):
        self.course_id = course_id
        self.course_code = course_code
        self.course_name = course_name
        self.credits = credits
        self.max_capacity = max_capacity
        self.current_enrollment = 0
        self.schedule = schedule
        self.department = department
        self.status = status

    def check_capacity(self) -> bool:
        """FR: Check Course Capacity"""
        return self.current_enrollment < self.max_capacity

    def check_prerequisite(self) -> bool:
        """FR: Check Prerequisites"""
        pass
