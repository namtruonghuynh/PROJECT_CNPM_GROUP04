import json


class PrerequisiteService:

    @staticmethod
    def check(student, course, academic_records=None):
        """
        Check if student can take this course based on prerequisites
        
        Args:
            student: dict with 'id' or 'student_id' field
            course: dict with 'prerequisites' field
            academic_records: list of academic records with student_id, course_id, grade
            
        Returns:
            tuple (bool, str, dict) - (can_register, message, details)
        """
        # Load academic records if not provided
        if academic_records is None:
            try:
                with open("data/academic_records.json", "r", encoding="utf-8") as f:
                    academic_records = json.load(f)
            except:
                academic_records = []
        
        # Get student ID from various field names
        student_id = student.get("student_id") or student.get("id")
        
        # Case 1: No prerequisite
        if not course.get("prerequisites") or len(course.get("prerequisites", [])) == 0:
            return True, "No prerequisite required", {"satisfied": [], "missing": []}
        
        prerequisites = course["prerequisites"]
        satisfied = []
        missing = []
        
        # Check each prerequisite
        for prereq in prerequisites:
            # Parse prerequisite format
            if isinstance(prereq, dict):
                prereq_course_id = prereq.get("course_id")
                min_grade = prereq.get("min_grade", 5.0)
            else:
                # Legacy format: just course ID
                prereq_course_id = prereq
                min_grade = 5.0
            
            # Find matching academic record
            completed_grade = None
            for record in academic_records:
                record_student_id = record.get("student_id")
                record_course_id = record.get("course_id")
                record_grade = record.get("grade", 0)
                
                # Debug info
                # print(f"Comparing: record_student_id={record_student_id}, student_id={student_id}, "
                #       f"record_course_id={record_course_id}, prereq_course_id={prereq_course_id}")
                
                if (record_student_id == student_id and 
                    record_course_id == prereq_course_id):
                    completed_grade = record_grade
                    break
            
            # Check if prerequisite is satisfied
            if completed_grade is not None and completed_grade >= min_grade:
                satisfied.append({
                    "course_id": prereq_course_id,
                    "min_grade": min_grade,
                    "actual_grade": completed_grade,
                    "status": "✅"
                })
            else:
                missing.append({
                    "course_id": prereq_course_id,
                    "min_grade": min_grade,
                    "actual_grade": completed_grade,
                    "status": "❌"
                })
        
        details = {"satisfied": satisfied, "missing": missing}
        
        if missing:
            missing_text = ", ".join([f"Course {m['course_id']} (grade >= {m['min_grade']})" for m in missing])
            return False, f"Missing prerequisites: {missing_text}", details
        
        return True, "All prerequisites satisfied", details
