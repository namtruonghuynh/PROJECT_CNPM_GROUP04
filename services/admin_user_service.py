from data.users import users_data

class AdminUserService:

    @staticmethod
    def manage_users():
        print("\n--- USER LIST ---")
        for u in users_data:
            print(f"{u['user_id']} | {u['username']} | {u['role']}")
