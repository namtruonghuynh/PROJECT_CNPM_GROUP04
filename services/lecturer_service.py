from services.course_service import CourseService
from services.registration_service import RegistrationService


class LecturerService:
    @staticmethod
    def view_teaching_courses(lecturer):
        courses = CourseService.get_course()

        print("\n--- Teaching Courses ---")
        for c in courses:
            if c.get("lecturer_id") == lecturer["user_id"]:
                print(f"{c['course_id']} - {c['course_name']}")

    @staticmethod
    def view_registered_students(course, registrations, users_data):
        student_ids = [
            r["student_id"]
            for r in registrations
            if r["course"]["course_id"] == course["course_id"]
        ]

        return [
            u for u in users_data
            if u["user_id"] in student_ids
        ]
    
    @staticmethod
    def view_student_list(course_id):
        print(f"\n--- Student list for course {course_id} ---")

        registrations = RegistrationService.get_registrations()
        
        found = False
        for r in registrations:
            if r["course"]["course_id"] == course_id:
                print(f"- Student ID: {r['student_id']}")
                found = True

        if not found:
            print("No students registered")