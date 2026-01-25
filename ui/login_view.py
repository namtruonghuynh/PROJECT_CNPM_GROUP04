import tkinter as tk
from tkinter import messagebox
from services.auth_service import AuthService

class LoginView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Course Registration System - Login")
        self.config(bg="#f0f0f0")

        self.build_ui()

    def build_ui(self):
        # Main container
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True)

        # Card frame
        card = tk.Frame(main_frame, bg="white", relief="raised", bd=2)
        card.pack(pady=50, padx=20)

        # Title
        tk.Label(
            card,
            text="Course Registration System",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=20, padx=20)

        # Username
        tk.Label(card, text="Username", bg="white", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10, 2))
        self.username_entry = tk.Entry(card, font=("Arial", 10), width=30)
        self.username_entry.pack(padx=20, pady=(0, 15), fill="x")

        # Password
        tk.Label(card, text="Password", bg="white", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(0, 2))
        self.password_entry = tk.Entry(card, font=("Arial", 10), show="*", width=30)
        self.password_entry.pack(padx=20, pady=(0, 20), fill="x")

        # Login button
        tk.Button(
            card,
            text="Login",
            command=self.handle_login,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            width=30,
            cursor="hand2"
        ).pack(padx=20, pady=(0, 20))

        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.handle_login())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing data", "Please enter username and password")
            return

        success, user = AuthService.login(username, password)

        if not success:
            messagebox.showerror("Login failed", "Invalid username or password")
            return

        # Login success - navigate to dashboard
        self.root.switch_frame(self.get_dashboard_view(user["role"]), user)

    def get_dashboard_view(self, role):
        if role == "student":
            from ui.student_view import StudentView
            return StudentView
        elif role == "admin":
            from ui.admin_view import AdminView
            return AdminView
        elif role == "lecturer":
            from ui.lecturer_view import LecturerView
            return LecturerView
