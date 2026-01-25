import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

from services.lecturer_service import LecturerService
from services.auth_service import AuthService
from ui.login_view import LoginView


class LecturerView(tk.Frame):
    def __init__(self, root, user):
        super().__init__(root)
        self.root = root
        self.user = user

        self.lecturer_service = LecturerService()
        
        self.course_table = None
        self.student_table = None

        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_courses()
        self.load_students()

    # UI

    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"Lecturer Dashboard – {self.user['username']}",
            fg="white",
            bg="#2c3e50",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=20, pady=10)

        tk.Button(
            header,
            text="Logout",
            command=self.logout,
            bg="#e74c3c",
            fg="white",
            width=10,
            cursor="hand2"
        ).pack(side="right", padx=20, pady=10)

        # Main Content
        content = tk.Frame(self)
        content.pack(fill="both", expand=True, padx=10, pady=10)

        # Notebook (Tabs)
        notebook = ttk.Notebook(content)
        notebook.pack(fill="both", expand=True)

        # Tab 1: My Courses
        courses_tab = tk.Frame(notebook)
        notebook.add(courses_tab, text="My Courses")
        self.create_courses_tab(courses_tab)

        # Tab 2: Students in Course
        students_tab = tk.Frame(notebook)
        notebook.add(students_tab, text="Students")
        self.create_students_tab(students_tab)

    def create_courses_tab(self, parent):
        # Courses list
        left = tk.LabelFrame(parent, text="My Courses", font=("Arial", 10, "bold"))
        left.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        self.course_table = ttk.Treeview(
            left,
            columns=("id", "name", "capacity", "enrolled"),
            show="headings",
            height=15
        )
        self.course_table.heading("id", text="Course ID")
        self.course_table.heading("name", text="Course Name")
        self.course_table.heading("capacity", text="Capacity")
        self.course_table.heading("enrolled", text="Enrolled")

        self.course_table.column("id", width=80)
        self.course_table.column("name", width=150)
        self.course_table.column("capacity", width=80)
        self.course_table.column("enrolled", width=80)

        self.course_table.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.course_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.course_table.config(yscroll=scrollbar.set)

        # Bind selection change to load students
        self.course_table.bind("<<TreeviewSelect>>", self.on_course_select)

        button_frame = tk.Frame(left)
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_courses,
            bg="#95a5a6",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

    def create_students_tab(self, parent):
        # Students list
        left = tk.LabelFrame(parent, text="Students", font=("Arial", 10, "bold"))
        left.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        self.student_table = ttk.Treeview(
            left,
            columns=("id", "student_id", "name", "grade", "status"),
            show="headings",
            height=15
        )
        self.student_table.heading("id", text="Reg ID")
        self.student_table.heading("student_id", text="Student ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("grade", text="Grade")
        self.student_table.heading("status", text="Status")

        self.student_table.column("id", width=60)
        self.student_table.column("student_id", width=80)
        self.student_table.column("name", width=120)
        self.student_table.column("grade", width=60)
        self.student_table.column("status", width=80)

        self.student_table.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.student_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.student_table.config(yscroll=scrollbar.set)

        button_frame = tk.Frame(left)
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(
            button_frame,
            text="Enter Grade",
            command=self.enter_grade,
            bg="#27ae60",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_students,
            bg="#95a5a6",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

    # DATA 

    def load_courses(self):
        for row in self.course_table.get_children():
            self.course_table.delete(row)

        # Load fresh data from JSON file
        import json
        try:
            with open("data/courses.json", "r", encoding="utf-8") as f:
                courses_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        
        # Filter courses assigned to this lecturer
        for c in courses_data:
            if c.get("lecturer_id") == self.user["id"]:
                enrolled = c.get("current_enrollment", 0)
                self.course_table.insert(
                    "",
                    "end",
                    values=(c["course_id"], c["name"], c["capacity"], enrolled)
                )

    def load_students(self):
        for row in self.student_table.get_children():
            self.student_table.delete(row)

        selected = self.course_table.focus()
        if not selected:
            return

        course_id = self.course_table.item(selected)["values"][0]
        
        # Load fresh data from JSON file
        import json
        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        
        for u in users_data:
            if u["role"] == "student" and course_id in u.get("registered_courses", []):
                self.student_table.insert(
                    "",
                    "end",
                    values=(
                        u.get("id", ""),
                        f"STU{u.get('id', '')}",
                        u.get("username", ""),
                        u.get("grade", "N/A"),
                        "Enrolled"
                    )
                )

    # ACTIONS

    def on_course_select(self, _):
        self.load_students()

    def enter_grade(self):
        selected = self.student_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student")
            return

        student_data = self.student_table.item(selected)["values"]
        registration_id = student_data[0]
        student_name = student_data[2]

        window = tk.Toplevel(self.root)
        window.title("Enter Grade")
        window.geometry("300x200")
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text=f"Student: {student_name}",
            font=("Arial", 10, "bold")
        ).pack(pady=10)

        tk.Label(window, text="Grade (0-10)", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10, 0))
        grade_entry = tk.Entry(window, width=30)
        grade_entry.pack(padx=20, pady=(0, 10), fill="x")

        tk.Label(window, text="Comments", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(0, 0))
        comments_entry = tk.Text(window, width=25, height=3)
        comments_entry.pack(padx=20, pady=(0, 10), fill="x")

        def save():
            try:
                grade = float(grade_entry.get().strip())
                if grade < 0 or grade > 10:
                    messagebox.showerror("Error", "Grade must be between 0 and 10")
                    return

                comments = comments_entry.get("1.0", "end-1c")

                # Load academic records
                try:
                    with open("data/academic_records.json", "r", encoding="utf-8") as f:
                        academic_records = json.load(f)
                except:
                    academic_records = []
                
                # Get student and course info
                student_id = None
                course_id = None
                with open("data/users.json", "r", encoding="utf-8") as f:
                    users_data = json.load(f)
                for u in users_data:
                    if u["id"] == int(registration_id):
                        student_id = u["id"]
                        break
                
                # Find course ID from selected row
                selected_row = self.student_table.focus()
                if selected_row:
                    values = self.student_table.item(selected_row)["values"]
                    course_id = values[0] if len(values) > 0 else None
                
                if not student_id or not course_id:
                    # Find from students in current course
                    with open("data/courses.json", "r", encoding="utf-8") as f:
                        courses = json.load(f)
                    for c in courses:
                        if c.get("lecturer_id") == self.user["id"]:
                            course_id = c["course_id"]
                            break
                
                # Update or create academic record
                found = False
                for record in academic_records:
                    if (record.get("student_id") == student_id and 
                        record.get("course_id") == course_id):
                        record["grade"] = grade
                        record["comments"] = comments
                        record["updated_at"] = datetime.now().isoformat()
                        found = True
                        break
                
                if not found:
                    # Create new record
                    new_id = max([r.get("record_id", 0) for r in academic_records], default=0) + 1
                    new_record = {
                        "record_id": new_id,
                        "student_id": student_id,
                        "course_id": course_id,
                        "grade": grade,
                        "comments": comments,
                        "created_at": datetime.now().isoformat()
                    }
                    academic_records.append(new_record)
                
                # Save academic records
                with open("data/academic_records.json", "w", encoding="utf-8") as f:
                    json.dump(academic_records, f, indent=4, ensure_ascii=False)

                messagebox.showinfo("Success", "Grade entered successfully")
                window.destroy()
                self.load_students()
            except ValueError:
                messagebox.showerror("Error", "Grade must be a valid number between 0-10")

        tk.Button(window, text="Save", command=save, bg="#27ae60", fg="white", width=20).pack(pady=10)

    # LOGOUT

    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            try:
                AuthService.logout()
                self.root.switch_frame(LoginView)
            except AttributeError:
                messagebox.showerror("Error", "Cannot logout from this window")
