class ReportService:

    @staticmethod
    def report_students_per_course(courses_data, registrations):
        report = {}
        for c in courses_data:
            report[c["course_id"]] = 0

        for r in registrations:
            cid = r["course"]["course_id"]
            report[cid] += 1

        return report

    @staticmethod
    def report_offered_courses(courses_data):
        return courses_data

    @staticmethod
    def credit_statistics(registrations, courses_data):
        stats = {}
        for r in registrations:
            sid = r["student_id"]
            course = r["course"]
            stats.setdefault(sid, 0)
            stats[sid] += course["credits"]
        return stats

    @staticmethod
    def view_reports():
        """Display registration reports to admin"""
        import json
        
        try:
            with open("data/courses.json", "r", encoding="utf-8") as f:
                courses_data = json.load(f)
        except:
            courses_data = []
        
        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users_data = json.load(f)
        except:
            users_data = []
        
        # Build registrations list from users data
        registrations = []
        for user in users_data:
            if user.get("role") == "student":
                for course_id in user.get("registered_courses", []):
                    for course in courses_data:
                        if course["course_id"] == course_id:
                            registrations.append({
                                "student_id": user["id"],
                                "course": course
                            })
                            break
        
        print("\n===== REGISTRATION REPORTS =====")
        print("1. Students per course")
        print("2. Offered courses")
        print("3. Credit statistics")
        print("0. Back")
        
        choice = input("Choose report: ")
        
        if choice == "1":
            report = ReportService.report_students_per_course(courses_data, registrations)
            print("\n--- Students Per Course ---")
            for course_id, count in report.items():
                print(f"Course {course_id}: {count} students")
        
        elif choice == "2":
            courses = ReportService.report_offered_courses(courses_data)
            print("\n--- Offered Courses ---")
            for course in courses:
                print(f"[{course['course_id']}] {course['course_name']} - Credits: {course['credits']}")
        
        elif choice == "3":
            stats = ReportService.credit_statistics(registrations, courses_data)
            print("\n--- Credit Statistics ---")
            for student_id, total_credits in stats.items():
                print(f"Student {student_id}: {total_credits} total credits")
        
        elif choice == "0":
            return
        
        else:
            print("Invalid choice")