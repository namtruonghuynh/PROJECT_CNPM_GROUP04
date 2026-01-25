import json
import os

class BaseService:
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_data(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
