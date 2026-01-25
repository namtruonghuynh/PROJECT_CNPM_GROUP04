from data.courses import courses_data

class AdminCourseService:

    @staticmethod
    def add_course():
        course_id = int(input("Course ID: "))
        name = input("Course name: ")
        capacity = int(input("Capacity: "))

        course = {
            "course_id": course_id,
            "name": name,
            "capacity": capacity,
            "current_enrollment": 0,
            "lecturer_id": None
        }

        courses_data.append(course)
        print("Course added successfully")


    @staticmethod
    def delete_course():
        course_id = int(input("Enter course ID to delete: "))

        for c in courses_data:
            if c["course_id"] == course_id:
                courses_data.remove(c)
                print("Course deleted")
                return
        print("Course not found")

    @staticmethod
    def assign_lecturer(course_id, lecturer_id):
        for c in courses_data:
            if c["course_id"] == course_id:
                c["lecturer_id"] = lecturer_id
                print("Lecturer assigned")
                return
        print("Course not found")

    
    @staticmethod
    def update_course():
        course_id = int(input("Enter course ID to update: "))

        for c in courses_data:
            if c["course_id"] == course_id:
                c["name"] = input("New name: ")
                c["capacity"] = int(input("New capacity: "))
                print("Course updated")
                return

        print("Course not found")
