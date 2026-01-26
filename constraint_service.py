class ConstraintService:

    @staticmethod
    def check_capacity(course):
        # Check using either capacity or max_capacity field
        max_cap = course.get("max_capacity") or course.get("capacity", 0)
        return course.get("current_enrollment", 0) < max_cap

    @staticmethod
    def check_schedule(student_courses, new_course):
        for c in student_courses:
            if c["schedule"] == new_course["schedule"]:
                return False
        return True
