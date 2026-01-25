import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "courses.json")

def load_courses():
    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_courses(courses):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(courses, f, indent=2)

courses_data = load_courses()
