import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "users.json")

def load_users():
    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)
    # Cập nhật users_data global sau khi save
    global users_data
    users_data = load_users()

def reload_users():
    """Reload users_data từ file - dùng sau khi user được tạo/cập nhật"""
    global users_data
    users_data = load_users()
    return users_data


users_data = load_users()


