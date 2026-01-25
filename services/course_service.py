import json

class CourseService:

    @staticmethod
    def get_course():
        with open("data/courses.json", "r", encoding="utf-8") as f:
            courses = json.load(f)
        return courses

    @staticmethod
    def view_courses():
        with open("data/courses.json", "r", encoding="utf-8") as f:
            courses = json.load(f)

        print("\n--- COURSE LIST ---")
        for c in courses:
            print(f"ID: {c['id']} | {c['name']} | Credits: {c['credits']}")

    @staticmethod
    def search_course(keyword):
        with open("data/courses.json", "r", encoding="utf-8") as f:
            courses = json.load(f)

        print("\n--- SEARCH RESULT ---")
        for c in courses:
            if keyword.lower() in c["name"].lower():
                print(f"ID: {c['id']} | {c['name']}")
