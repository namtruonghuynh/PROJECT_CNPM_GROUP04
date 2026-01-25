import json

class NotificationService:

    @staticmethod
    def notify(user, message):
        with open("data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)

        for u in users:
            if u["id"] == user["id"]:
                u.setdefault("notifications", []).append(message)

        with open("data/users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def view_notifications(user):
        print("\n--- NOTIFICATIONS ---")
        for n in user.get("notifications", []):
            print("-", n)
