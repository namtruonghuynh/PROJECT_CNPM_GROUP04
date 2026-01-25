import tkinter as tk



class StudentRegisteredView:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.root.title("Registered Courses")
        self.root.geometry("700x400")

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="This view is deprecated. Use StudentView instead.").pack()
