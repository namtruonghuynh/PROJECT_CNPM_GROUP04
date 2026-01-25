import tkinter as tk
from ui.login_view import LoginView

class CourseRegistrationGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Course Registration System")
        self.geometry("1000x600")
        self.resizable(True, True)

        self.current_frame = None
        self.show_login()

    def show_login(self):
        self.switch_frame(LoginView)

    def switch_frame(self, frame_class, *args, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)
