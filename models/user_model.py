class User:
    def __init__(self, user_id: int, username: str, password: str,
                 full_name: str, email: str, role: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.role = role  # Student / Lecturer / Administrator

    def login(self) -> bool:
        """FR: Login (User Authentication)"""
        pass

    def logout(self) -> None:
        pass
