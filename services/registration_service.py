import json
from datetime import datetime
from services.notification_service import NotificationService
from services.prerequisite_service import PrerequisiteService
from services.constraint_service import ConstraintService
from services.registration_period_service import RegistrationPeriodService

class RegistrationService:
    registrations = []

    @staticmethod
    def get_registrations():
        return RegistrationService.registrations

    @staticmethod
    def register_course(student, course_id):
        # Load data
        with open("data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        
        with open("data/courses.json", "r", encoding="utf-8") as f:
            courses = json.load(f)

        # Convert course_id to int
        course_id = int(course_id)

        # Check if registration period is open
        is_open, message = RegistrationPeriodService.check_period()
        if not is_open:
            return False, message

        # Find course
        course = None
        for c in courses:
            if c["course_id"] == course_id:
                course = c
                break
        
        if not course:
            return False, "Course not found"

        # Find student in users and check duplicate registration
        student_found = False
        for u in users:
            if u["id"] == student["id"]:
                student_found = True
                if "registered_courses" not in u:
                    u["registered_courses"] = []
                
                if course_id in u["registered_courses"]:
                    return False, "Already registered"
                break
        
        if not student_found:
            return False, "Student not found"

        # Check capacity constraint
        if not ConstraintService.check_capacity(course):
            return False, "Course is full"

        # Check prerequisite
        academic_records = []
        try:
            with open("data/academic_records.json", "r", encoding="utf-8") as f:
                academic_records = json.load(f)
        except:
            academic_records = []

        # Check prerequisite - skip if no prerequisites
        if course.get("prerequisites") and len(course["prerequisites"]) > 0:
            student_copy = student.copy()
            # Ensure student has proper ID field
            if "student_id" not in student_copy:
                student_copy["student_id"] = student_copy.get("id")
            
            prereq_ok, prereq_msg, _ = PrerequisiteService.check(student_copy, course, academic_records)
            if not prereq_ok:
                return False, prereq_msg

        # Register course - MUST have registered_courses initialized
        for u in users:
            if u["id"] == student["id"]:
                if "registered_courses" not in u:
                    u["registered_courses"] = []
                u["registered_courses"].append(course_id)
                break

        # Update course enrollment
        for c in courses:
            if c["course_id"] == course_id:
                if "current_enrollment" not in c:
                    c["current_enrollment"] = 0
                c["current_enrollment"] += 1
                break

        # Save updates
        with open("data/users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
        
        with open("data/courses.json", "w", encoding="utf-8") as f:
            json.dump(courses, f, indent=4, ensure_ascii=False)

        NotificationService.notify(student, "Register course successfully")
        return True, "Register success"

    @staticmethod
    def drop_course(student, course_id):
        with open("data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)

        with open("data/courses.json", "r", encoding="utf-8") as f:
            courses = json.load(f)

        # Convert course_id to int
        course_id = int(course_id)

        for u in users:
            if u["id"] == student["id"]:
                # Add registered_courses field if it doesn't exist
                if "registered_courses" not in u:
                    u["registered_courses"] = []
                
                if course_id not in u["registered_courses"]:
                    return False
                u["registered_courses"].remove(course_id)

        # Update course enrollment
        for c in courses:
            if c["course_id"] == course_id:
                if "current_enrollment" not in c:
                    c["current_enrollment"] = 0
                c["current_enrollment"] = max(0, c["current_enrollment"] - 1)
                break

        with open("data/users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

        with open("data/courses.json", "w", encoding="utf-8") as f:
            json.dump(courses, f, indent=4, ensure_ascii=False)

        return True
