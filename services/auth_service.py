from data.users import load_users

class AuthService:
    current_user = None

    @staticmethod
    def login(username, password):
        # Load users từ file mỗi lần đăng nhập để đảm bảo dữ liệu là mới nhất
        users_data = load_users()
        for user in users_data:
            if user["username"] == username and user["password"] == password:
                AuthService.current_user = user
                return True, user
        return False, None

    @staticmethod
    def logout():
        AuthService.current_user = None
