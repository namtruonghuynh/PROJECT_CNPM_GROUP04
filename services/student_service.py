import json

class StudentService:

    @staticmethod
    def view_registered_courses(student):
        with open("data/courses.json", "r", encoding="utf-8") as f:
            courses = json.load(f)

        print("\n--- REGISTERED COURSES ---")
        for c in courses:
            if c["id"] in student["registered_courses"]:
                print(f"{c['id']} - {c['name']}")

    @staticmethod
    def get_academic_records(student_id):
        """
        Lấy lịch sử học tập (các môn đã học) của sinh viên
        
        Args:
            student_id: ID của sinh viên (có thể là int hoặc string)
            
        Returns:
            List các records gồm course_id, course_name, grade, semester
        """
        try:
            with open("data/academic_records.json", "r", encoding="utf-8") as f:
                academic_records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        try:
            with open("data/courses.json", "r", encoding="utf-8") as f:
                courses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            courses = []
        
        # Map course_id -> course_name
        course_map = {c["course_id"]: c["name"] for c in courses}
        
        # Lấy records của sinh viên này
        student_records = []
        for record in academic_records:
            # So sánh cả int và string
            if str(record.get("student_id")) == str(student_id):
                course_id = record.get("course_id")
                course_name = course_map.get(course_id, f"Unknown Course {course_id}")
                
                student_records.append({
                    "course_id": course_id,
                    "course_name": course_name,
                    "grade": record.get("grade", 0),
                    "semester": record.get("semester", "Unknown"),
                    "record_id": record.get("record_id")
                })
        
        # Sắp xếp theo semester (mới nhất trước)
        student_records.sort(key=lambda x: x["semester"], reverse=True)
        
        return student_records

