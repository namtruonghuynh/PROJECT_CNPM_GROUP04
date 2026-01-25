import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

from services.course_service import CourseService
from services.registration_service import RegistrationService
from services.auth_service import AuthService
from services.prerequisite_service import PrerequisiteService
from services.registration_period_service import RegistrationPeriodService
from services.student_service import StudentService
from ui.login_view import LoginView


class StudentView(tk.Frame):
    def __init__(self, root, user):
        super().__init__(root)
        self.root = root
        self.user = user

        self.course_service = CourseService()
        self.registration_service = RegistrationService()

        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_courses()
        self.load_registered_courses()
        self.load_learning_history()

    # UI

    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"Student Dashboard – {self.user['username']}",
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

        # Registration Period Info
        period_info = tk.Frame(self, bg="#ecf0f1", height=40)
        period_info.pack(fill="x", padx=10, pady=5)
        
        period_status, period_text = self.get_period_info()
        period_color = "#27ae60" if "OPEN" in period_status else "#e74c3c"
        
        tk.Label(
            period_info,
            text=f"Registration Period: {period_text}",
            fg=period_color,
            bg="#ecf0f1",
            font=("Arial", 9, "bold")
        ).pack(side="left", padx=15, pady=10)

        # Main Content with Notebook (Tabs)
        content = tk.Frame(self)
        content.pack(fill="both", expand=True, padx=10, pady=10)

        notebook = ttk.Notebook(content)
        notebook.pack(fill="both", expand=True)

        # Tab 1: Course Registration
        registration_tab = tk.Frame(notebook)
        notebook.add(registration_tab, text="Course Registration")
        self.create_registration_tab(registration_tab)

        # Tab 2: Learning History
        history_tab = tk.Frame(notebook)
        notebook.add(history_tab, text="Learning History")
        self.create_learning_history_tab(history_tab)

    def create_registration_tab(self, parent):
        """Tab đăng ký môn học"""
        content = tk.Frame(parent)
        content.pack(fill="both", expand=True, padx=10, pady=10)

        # Left: Available courses
        left = tk.LabelFrame(content, text="Available Courses", font=("Arial", 10, "bold"))
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.course_table = ttk.Treeview(
            left,
            columns=("id", "name", "capacity", "enrolled", "status"),
            show="headings",
            height=15
        )
        self.course_table.heading("id", text="Course ID")
        self.course_table.heading("name", text="Course Name")
        self.course_table.heading("capacity", text="Capacity")
        self.course_table.heading("enrolled", text="Enrolled")
        self.course_table.heading("status", text="Status")
        
        self.course_table.column("id", width=70)
        self.course_table.column("name", width=150)
        self.course_table.column("capacity", width=70)
        self.course_table.column("enrolled", width=70)
        self.course_table.column("status", width=90)

        self.course_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.course_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.course_table.config(yscroll=scrollbar.set)

        button_frame = tk.Frame(left)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(
            button_frame,
            text="Register Course",
            command=self.register_course,
            bg="#27ae60",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_courses,
            bg="#95a5a6",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        # Right: Registered courses
        right = tk.LabelFrame(content, text="My Registered Courses", font=("Arial", 10, "bold"))
        right.pack(side="right", fill="both", expand=True)

        self.registered_table = ttk.Treeview(
            right,
            columns=("id", "name", "grade"),
            show="headings",
            height=15
        )
        self.registered_table.heading("id", text="Course ID")
        self.registered_table.heading("name", text="Course Name")
        self.registered_table.heading("grade", text="Grade")
        
        self.registered_table.column("id", width=80)
        self.registered_table.column("name", width=150)
        self.registered_table.column("grade", width=80)

        self.registered_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar2 = ttk.Scrollbar(right, orient="vertical", command=self.registered_table.yview)
        scrollbar2.pack(side="right", fill="y")
        self.registered_table.config(yscroll=scrollbar2.set)

        button_frame2 = tk.Frame(right)
        button_frame2.pack(fill="x", padx=10, pady=5)
        
        tk.Button(
            button_frame2,
            text="Unregister Course",
            command=self.unregister_course,
            bg="#e74c3c",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame2,
            text="Refresh",
            command=self.load_registered_courses,
            bg="#95a5a6",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

    def create_learning_history_tab(self, parent):
        """Tab lịch sử học tập - các môn đã học và điểm số"""
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = tk.Label(
            frame,
            text="Your Learning History",
            font=("Arial", 12, "bold"),
            fg="#2c3e50"
        )
        title.pack(anchor="w", pady=(0, 10))

        # Table showing completed courses
        columns = ("course_id", "course_name", "grade", "semester")
        self.history_table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=20
        )
        
        self.history_table.heading("course_id", text="Course ID")
        self.history_table.heading("course_name", text="Course Name")
        self.history_table.heading("grade", text="Grade")
        self.history_table.heading("semester", text="Semester")
        
        self.history_table.column("course_id", width=80)
        self.history_table.column("course_name", width=200)
        self.history_table.column("grade", width=100)
        self.history_table.column("semester", width=100)

        self.history_table.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.history_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_table.config(yscroll=scrollbar.set)

        # Button frame
        button_frame = tk.Frame(frame)
        button_frame.pack(fill="x", pady=10)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_learning_history,
            bg="#3498db",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        # Summary info
        summary_frame = tk.Frame(frame, bg="#ecf0f1", relief="sunken", bd=1)
        summary_frame.pack(fill="x", pady=10)

        self.summary_label = tk.Label(
            summary_frame,
            text="",
            font=("Arial", 10),
            bg="#ecf0f1",
            justify="left"
        )
        self.summary_label.pack(anchor="w", padx=10, pady=10)

    # DATA

    def get_period_info(self):
        """Get current registration period info"""
        try:
            with open("data/registration_periods.json", "r", encoding="utf-8") as f:
                periods = json.load(f)
            
            for period in periods:
                start = datetime.fromisoformat(period["start_date"])
                end = datetime.fromisoformat(period["end_date"])
                now = datetime.now()
                
                if start <= now <= end:
                    return "OPEN", f"{period['name']} (Open until {end.strftime('%Y-%m-%d %H:%M')})"
            
            # Find next period
            for period in sorted(periods, key=lambda p: p["start_date"]):
                start = datetime.fromisoformat(period["start_date"])
                if start > datetime.now():
                    return "CLOSED", f"{period['name']} opens {start.strftime('%Y-%m-%d %H:%M')}"
            
            return "CLOSED", "No registration period available"
        except:
            return "UNKNOWN", "Cannot load registration info"

    def is_registration_open(self):
        """Check if registration is open"""
        period_status, _ = self.get_period_info()
        return period_status == "OPEN"

    def check_prerequisite_status(self, course):
        """Check if student can take this course based on prerequisites"""
        # If no prerequisite, can register
        if not course.get("prerequisites") or len(course["prerequisites"]) == 0:
            return "Available", True, ""
        
        # Load academic records
        try:
            with open("data/academic_records.json", "r", encoding="utf-8") as f:
                academic_records = json.load(f)
        except:
            academic_records = []
        
        # Use improved PrerequisiteService
        can_register, message, details = PrerequisiteService.check(
            self.user, 
            course, 
            academic_records
        )
        
        if can_register:
            status = "Eligible"
            detail_lines = []
            for sat in details.get("satisfied", []):
                detail_lines.append(f"✓ Course {sat['course_id']} (grade: {sat['actual_grade']:.1f} >= {sat['min_grade']})")
            detail = "\n".join(detail_lines)
        else:
            status = "Missing Prerequisites"
            detail_lines = []
            for miss in details.get("missing", []):
                if miss['actual_grade'] is not None:
                    detail_lines.append(f"Course {miss['course_id']} (your grade: {miss['actual_grade']:.1f}, need >= {miss['min_grade']})")
                else:
                    detail_lines.append(f"ourse {miss['course_id']} (not completed, need grade >= {miss['min_grade']})")
            detail = "\n".join(detail_lines)
        
        return status, can_register, detail

    def load_courses(self):
        for row in self.course_table.get_children():
            self.course_table.delete(row)

        try:
            with open("data/courses.json", "r", encoding="utf-8") as f:
                courses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        
        for c in courses:
            status, _, _ = self.check_prerequisite_status(c)
            self.course_table.insert(
                "",
                "end",
                values=(
                    c["course_id"], 
                    c["name"], 
                    c.get("capacity", 0), 
                    c.get("current_enrollment", 0),
                    status
                ),
                tags=(c["course_id"],)  # Use course_id as tag for tracking
            )

    def load_registered_courses(self):
        for row in self.registered_table.get_children():
            self.registered_table.delete(row)

        # Load fresh data from JSON files
        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users_data = json.load(f)
            with open("data/courses.json", "r", encoding="utf-8") as f:
                courses_data = json.load(f)
            with open("data/academic_records.json", "r", encoding="utf-8") as f:
                academic_records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        
        # Get registered course IDs from user data
        student_course_ids = []
        for u in users_data:
            if u["id"] == self.user["id"]:
                student_course_ids = u.get("registered_courses", [])
                break
        
        # Create grade lookup from academic records
        grade_lookup = {}  # {course_id: grade}
        for record in academic_records:
            if record.get("student_id") == self.user["id"]:
                grade_lookup[record["course_id"]] = record.get("grade", "N/A")
        
        # Get course details and grades
        for course_id in student_course_ids:
            for c in courses_data:
                if c["course_id"] == course_id:
                    # Get grade from academic records
                    grade = grade_lookup.get(course_id, "N/A")
                    if isinstance(grade, (int, float)):
                        grade_display = f"{grade:.1f}"
                    else:
                        grade_display = str(grade)
                    
                    self.registered_table.insert(
                        "",
                        "end",
                        values=(c["course_id"], c["name"], grade_display)
                    )
                    break

    def load_learning_history(self):
        """Load lịch sử học tập từ academic records"""
        for row in self.history_table.get_children():
            self.history_table.delete(row)

        # Lấy lịch sử học tập từ service
        records = StudentService.get_academic_records(self.user["id"])
        
        # Thêm vào table
        for record in records:
            grade_display = f"{record['grade']:.1f}" if isinstance(record['grade'], (int, float)) else str(record['grade'])
            self.history_table.insert(
                "",
                "end",
                values=(
                    record["course_id"],
                    record["course_name"],
                    grade_display,
                    record["semester"]
                )
            )
        
        # Update summary
        self.update_learning_summary(records)

    def update_learning_summary(self, records):
        """Cập nhật thông tin tóm tắt học tập"""
        if not records:
            summary_text = "No learning history yet."
        else:
            total_courses = len(records)
            grades = [r["grade"] for r in records if isinstance(r["grade"], (int, float))]
            avg_grade = sum(grades) / len(grades) if grades else 0
            
            passed_courses = len([g for g in grades if g >= 5.0])
            
            summary_text = f"Total Courses: {total_courses} | Passed: {passed_courses} | Average Grade: {avg_grade:.2f}"
        
        self.summary_label.config(text=summary_text)

    # ACTIONS

    def register_course(self):
        selected = self.course_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course")
            return

        # Check if registration period is open
        if not self.is_registration_open():
            _, period_text = self.get_period_info()
            messagebox.showwarning("Registration Closed", f"You can only register during open periods.\n\n{period_text}")
            return

        values = self.course_table.item(selected)["values"]
        course_id = values[0]
        course_name = values[1]
        status = values[4]
        
        # Check if course is locked
        if "" in status:
            # Show detailed prerequisite requirements
            try:
                with open("data/courses.json", "r", encoding="utf-8") as f:
                    courses = json.load(f)
                course = next((c for c in courses if c["course_id"] == course_id), None)
                if course:
                    _, _, detail = self.check_prerequisite_status(course)
                    msg = f"You cannot register this course.\n\n{status}\n\nRequired:\n{detail}"
                    messagebox.showwarning("Not Eligible", msg)
                else:
                    messagebox.showwarning("Not Eligible", f"You cannot register this course.\n\n{status}")
            except:
                messagebox.showwarning("Not Eligible", f"You cannot register this course.\n\n{status}")
            return

        result, msg = self.registration_service.register_course(
            self.user,
            course_id
        )

        if result:
            messagebox.showinfo("Success", "Course registered successfully")
            self.load_courses()
            self.load_registered_courses()
        else:
            messagebox.showerror("Error", msg)

    def unregister_course(self):
        selected = self.registered_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course")
            return

        # Check if registration period is open
        if not self.is_registration_open():
            _, period_text = self.get_period_info()
            messagebox.showwarning("Registration Closed", f"You can only unregister during open periods.\n\n{period_text}")
            return

        course_id = self.registered_table.item(selected)["values"][0]
        course_name = self.registered_table.item(selected)["values"][1]

        if messagebox.askyesno("Confirm", f"Unregister '{course_name}'?"):
            result = self.registration_service.drop_course(
                self.user,
                course_id
            )
            if result:
                messagebox.showinfo("Success", "Course unregistered successfully")
                self.load_courses()
                self.load_registered_courses()
            else:
                messagebox.showerror("Error", "Cannot unregister this course")

    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            try:
                AuthService.logout()
                self.root.switch_frame(LoginView)
            except AttributeError:
                messagebox.showerror("Error", "Cannot logout from this window")
