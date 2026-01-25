import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from services.admin_course_service import AdminCourseService
from services.admin_user_service import AdminUserService
from services.auth_service import AuthService
from services.registration_period_service import RegistrationPeriodService
from ui.login_view import LoginView


class AdminView(tk.Frame):
    def __init__(self, root, user):
        super().__init__(root)
        self.root = root
        self.user = user

        self.course_service = AdminCourseService()
        self.user_service = AdminUserService()
        self.registration_period_service = RegistrationPeriodService()
        
        self.course_table = None
        self.user_table = None
        self.period_table = None

        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_courses()
        self.load_users()

    # UI

    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"Admin Dashboard – {self.user['username']}",
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

        # Tab 1: Courses Management
        courses_tab = tk.Frame(notebook)
        notebook.add(courses_tab, text="Manage Courses")
        self.create_courses_tab(courses_tab)

        # Tab 2: Users Management
        users_tab = tk.Frame(notebook)
        notebook.add(users_tab, text="Manage Users")
        self.create_users_tab(users_tab)

        # Tab 3: Registration Period Management
        period_tab = tk.Frame(notebook)
        notebook.add(period_tab, text="Registration Period")
        self.create_period_tab(period_tab)
        self.load_periods()

    def create_courses_tab(self, parent):
        # Left: Course list
        left = tk.LabelFrame(parent, text="Courses", font=("Arial", 10, "bold"))
        left.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        self.course_table = ttk.Treeview(
            left,
            columns=("id", "name", "lecturer", "capacity"),
            show="headings",
            height=15
        )
        self.course_table.heading("id", text="Course ID")
        self.course_table.heading("name", text="Name")
        self.course_table.heading("lecturer", text="Lecturer")
        self.course_table.heading("capacity", text="Capacity")

        self.course_table.column("id", width=80)
        self.course_table.column("name", width=150)
        self.course_table.column("lecturer", width=100)
        self.course_table.column("capacity", width=80)

        self.course_table.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.course_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.course_table.config(yscroll=scrollbar.set)

        button_frame = tk.Frame(left)
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(
            button_frame,
            text="Add Course",
            command=self.add_course,
            bg="#27ae60",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Edit Course",
            command=self.edit_course,
            bg="#f39c12",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Delete Course",
            command=self.delete_course,
            bg="#e74c3c",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Assign Lecturer",
            command=self.assign_lecturer,
            bg="#9b59b6",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Unassign Lecturer",
            command=self.unassign_lecturer,
            bg="#e67e22",
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

    def create_users_tab(self, parent):
        # Users list
        left = tk.LabelFrame(parent, text="Users", font=("Arial", 10, "bold"))
        left.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        self.user_table = ttk.Treeview(
            left,
            columns=("id", "username", "role", "email"),
            show="headings",
            height=15
        )
        self.user_table.heading("id", text="User ID")
        self.user_table.heading("username", text="Username")
        self.user_table.heading("role", text="Role")
        self.user_table.heading("email", text="Email")

        self.user_table.column("id", width=80)
        self.user_table.column("username", width=120)
        self.user_table.column("role", width=80)
        self.user_table.column("email", width=150)

        self.user_table.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.user_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.user_table.config(yscroll=scrollbar.set)

        button_frame = tk.Frame(left)
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(
            button_frame,
            text="Add User",
            command=self.add_user,
            bg="#27ae60",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Edit User",
            command=self.edit_user,
            bg="#f39c12",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Delete User",
            command=self.delete_user,
            bg="#e74c3c",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_users,
            bg="#95a5a6",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

    def create_period_tab(self, parent):
        # Period list
        left = tk.LabelFrame(parent, text="Registration Periods", font=("Arial", 10, "bold"))
        left.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        self.period_table = ttk.Treeview(
            left,
            columns=("id", "name", "start_date", "end_date", "status"),
            show="headings",
            height=15
        )
        self.period_table.heading("id", text="Period ID")
        self.period_table.heading("name", text="Name")
        self.period_table.heading("start_date", text="Start Date")
        self.period_table.heading("end_date", text="End Date")
        self.period_table.heading("status", text="Status")

        self.period_table.column("id", width=60)
        self.period_table.column("name", width=120)
        self.period_table.column("start_date", width=130)
        self.period_table.column("end_date", width=130)
        self.period_table.column("status", width=80)

        self.period_table.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.period_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.period_table.config(yscroll=scrollbar.set)

        button_frame = tk.Frame(left)
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(
            button_frame,
            text="Add Period",
            command=self.add_period,
            bg="#27ae60",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Edit Period",
            command=self.edit_period,
            bg="#f39c12",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Delete Period",
            command=self.delete_period,
            bg="#e74c3c",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_periods,
            bg="#95a5a6",
            fg="white",
            cursor="hand2"
        ).pack(side="left", padx=5)

    # DATA

    def load_courses(self):
        for row in self.course_table.get_children():
            self.course_table.delete(row)

        import json
        try:
            with open("data/courses.json", "r", encoding="utf-8") as f:
                courses = json.load(f)
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        
        # Create lecturer name mapping
        lecturer_map = {}
        for u in users:
            if u.get("role") == "lecturer":
                lecturer_map[u["id"]] = u["username"]
        
        for c in courses:
            lecturer_id = c.get("lecturer_id")
            lecturer_name = lecturer_map.get(lecturer_id, "Unassigned") if lecturer_id else "Unassigned"
            self.course_table.insert(
                "",
                "end",
                values=(c["course_id"], c["name"], lecturer_name, c["capacity"])
            )

    def load_users(self):
        for row in self.user_table.get_children():
            self.user_table.delete(row)

        import json
        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        
        for u in users:
            self.user_table.insert(
                "",
                "end",
                values=(u["id"], u["username"], u["role"], u.get("email", ""))
            )

    def load_periods(self):
        for row in self.period_table.get_children():
            self.period_table.delete(row)

        periods = RegistrationPeriodService.get_all_periods()
        
        for p in periods:
            start = datetime.fromisoformat(p["start_date"])
            end = datetime.fromisoformat(p["end_date"])
            now = datetime.now()
            
            if start <= now <= end:
                status = "OPEN"
            elif now < start:
                status = "COMING"
            else:
                status = "CLOSED"
            
            self.period_table.insert(
                "",
                "end",
                values=(p["period_id"], p["name"], p["start_date"], p["end_date"], status)
            )

    # COURSE ACTIONS

    def add_course(self):
        window = tk.Toplevel(self.root)
        window.title("Add Course")
        window.geometry("300x250")
        window.transient(self.root)
        window.grab_set()

        tk.Label(window, text="Course ID", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10, 0))
        course_id_entry = tk.Entry(window, width=30)
        course_id_entry.pack(padx=20, pady=(0, 10), fill="x")

        tk.Label(window, text="Course Name", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(0, 0))
        name_entry = tk.Entry(window, width=30)
        name_entry.pack(padx=20, pady=(0, 10), fill="x")

        tk.Label(window, text="Capacity", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(0, 0))
        capacity_entry = tk.Entry(window, width=30)
        capacity_entry.pack(padx=20, pady=(0, 10), fill="x")

        def save():
            try:
                course_id = course_id_entry.get().strip()
                name = name_entry.get().strip()
                capacity = int(capacity_entry.get().strip())

                if not course_id or not name or capacity <= 0:
                    messagebox.showwarning("Validation", "Please fill all fields correctly")
                    return

                import json
                with open("data/courses.json", "r", encoding="utf-8") as f:
                    courses_data = json.load(f)
                
                course = {
                    "course_id": int(course_id),
                    "name": name,
                    "capacity": capacity,
                    "current_enrollment": 0,
                    "lecturer_id": None
                }
                courses_data.append(course)
                
                with open("data/courses.json", "w", encoding="utf-8") as f:
                    json.dump(courses_data, f, indent=4)

                messagebox.showinfo("Success", "Course added successfully")
                window.destroy()
                self.load_courses()
            except ValueError:
                messagebox.showerror("Error", "Course ID and Capacity must be numbers")

        tk.Button(window, text="Save", command=save, bg="#27ae60", fg="white", width=20).pack(pady=20)

    def edit_course(self):
        selected = self.course_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course")
            return

        values = self.course_table.item(selected)["values"]
        course_id = values[0]

        window = tk.Toplevel(self.root)
        window.title("Edit Course")
        window.geometry("300x250")
        window.transient(self.root)
        window.grab_set()

        tk.Label(window, text="Course Name", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10, 0))
        name_entry = tk.Entry(window, width=30)
        name_entry.insert(0, values[1])
        name_entry.pack(padx=20, pady=(0, 10), fill="x")

        tk.Label(window, text="Capacity", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(0, 0))
        capacity_entry = tk.Entry(window, width=30)
        capacity_entry.insert(0, str(values[3]))
        capacity_entry.pack(padx=20, pady=(0, 10), fill="x")

        def save():
            try:
                name = name_entry.get().strip()
                capacity = int(capacity_entry.get().strip())

                if not name or capacity <= 0:
                    messagebox.showwarning("Validation", "Please fill all fields correctly")
                    return

                import json
                with open("data/courses.json", "r", encoding="utf-8") as f:
                    courses_data = json.load(f)
                
                for c in courses_data:
                    if c["course_id"] == course_id:
                        c["name"] = name
                        c["capacity"] = capacity
                        break
                
                with open("data/courses.json", "w", encoding="utf-8") as f:
                    json.dump(courses_data, f, indent=4)

                messagebox.showinfo("Success", "Course updated successfully")
                window.destroy()
                self.load_courses()
            except ValueError:
                messagebox.showerror("Error", "Capacity must be a number")

        tk.Button(window, text="Save", command=save, bg="#27ae60", fg="white", width=20).pack(pady=20)

    def delete_course(self):
        selected = self.course_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this course?"):
            course_id = self.course_table.item(selected)["values"][0]
            import json
            with open("data/courses.json", "r", encoding="utf-8") as f:
                courses_data = json.load(f)
            
            for c in courses_data:
                if c["course_id"] == course_id:
                    courses_data.remove(c)
                    break
            
            with open("data/courses.json", "w", encoding="utf-8") as f:
                json.dump(courses_data, f, indent=4)
            
            messagebox.showinfo("Success", "Course deleted successfully")
            self.load_courses()

    def assign_lecturer(self):
        selected = self.course_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course")
            return

        values = self.course_table.item(selected)["values"]
        course_id = values[0]
        course_name = values[1]

        window = tk.Toplevel(self.root)
        window.title("Assign Lecturer")
        window.geometry("400x300")
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text=f"Course: {course_name}",
            font=("Arial", 11, "bold")
        ).pack(pady=10)

        tk.Label(window, text="Select Lecturer", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10, 0))

        # Get all lecturers from JSON
        import json
        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users_data = json.load(f)
        except:
            messagebox.showerror("Error", "Cannot load lecturers")
            return
        
        lecturers = [u for u in users_data if u.get("role") == "lecturer"]
        lecturer_names = {u["username"]: u["id"] for u in lecturers}

        lecturer_var = tk.StringVar()
        lecturer_combo = ttk.Combobox(
            window,
            textvariable=lecturer_var,
            values=list(lecturer_names.keys()),
            width=30,
            state="readonly"
        )
        lecturer_combo.pack(padx=20, pady=(0, 20), fill="x")

        def assign():
            lecturer_username = lecturer_var.get()
            if not lecturer_username:
                messagebox.showwarning("Validation", "Please select a lecturer")
                return

            lecturer_id = lecturer_names[lecturer_username]

            # Update course with lecturer_id
            try:
                with open("data/courses.json", "r", encoding="utf-8") as f:
                    courses_data = json.load(f)
                
                for c in courses_data:
                    if c["course_id"] == course_id:
                        c["lecturer_id"] = lecturer_id
                        break

                with open("data/courses.json", "w", encoding="utf-8") as f:
                    json.dump(courses_data, f, indent=4, ensure_ascii=False)

                messagebox.showinfo("Success", f"Lecturer '{lecturer_username}' assigned successfully")
                window.destroy()
                self.load_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Cannot assign lecturer: {str(e)}")

        tk.Button(window, text="Assign", command=assign, bg="#27ae60", fg="white", width=20).pack(pady=10)

    def unassign_lecturer(self):
        selected = self.course_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course")
            return

        values = self.course_table.item(selected)["values"]
        course_id = values[0]
        course_name = values[1]
        current_lecturer = values[2]

        if current_lecturer == "Unassigned":
            messagebox.showinfo("Info", "This course has no lecturer assigned")
            return

        if messagebox.askyesno("Confirm", f"Remove lecturer '{current_lecturer}' from '{course_name}'?"):
            import json
            try:
                with open("data/courses.json", "r", encoding="utf-8") as f:
                    courses_data = json.load(f)
                
                for c in courses_data:
                    if c["course_id"] == course_id:
                        c["lecturer_id"] = None
                        break
                
                with open("data/courses.json", "w", encoding="utf-8") as f:
                    json.dump(courses_data, f, indent=4, ensure_ascii=False)
                
                messagebox.showinfo("Success", f"Lecturer removed from '{course_name}'")
                self.load_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Cannot remove lecturer: {str(e)}")

    # USER ACTIONS

    def add_user(self):
        window = tk.Toplevel(self.root)
        window.title("Add User")
        window.geometry("300x300")
        window.transient(self.root)
        window.grab_set()

        tk.Label(window, text="Username", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10, 0))
        username_entry = tk.Entry(window, width=30)
        username_entry.pack(padx=20, pady=(0, 10), fill="x")

        tk.Label(window, text="Password", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(0, 0))
        password_entry = tk.Entry(window, show="*", width=30)
        password_entry.pack(padx=20, pady=(0, 10), fill="x")

        tk.Label(window, text="Role", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(0, 0))
        role_var = tk.StringVar(value="student")
        role_combo = ttk.Combobox(window, textvariable=role_var, values=["student", "lecturer", "admin"], width=28, state="readonly")
        role_combo.pack(padx=20, pady=(0, 10), fill="x")

        tk.Label(window, text="Email", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(0, 0))
        email_entry = tk.Entry(window, width=30)
        email_entry.pack(padx=20, pady=(0, 10), fill="x")

        def save():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role = role_var.get()
            email = email_entry.get().strip()

            if not username or not password or not role:
                messagebox.showwarning("Validation", "Please fill all required fields")
                return

            import json
            from services.id_generator_service import IDGeneratorService
            
            try:
                with open("data/users.json", "r", encoding="utf-8") as f:
                    users_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                messagebox.showerror("Error", f"Cannot read users.json: {str(e)}")
                return
            
            # Check if username already exists
            for u in users_data:
                if u["username"] == username:
                    messagebox.showwarning("Validation", "Username already exists")
                    return
            
            # Sinh ID mới dựa trên role
            new_id = IDGeneratorService.get_next_id(role)
            
            user = {
                "id": new_id,
                "username": username,
                "password": password,
                "role": role,
                "email": email if email else "",
                "registered_courses": []
            }
            users_data.append(user)
            
            try:
                with open("data/users.json", "w", encoding="utf-8") as f:
                    json.dump(users_data, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Success", f"User added successfully (ID: {new_id})")
                window.destroy()
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save user: {str(e)}")

        tk.Button(window, text="Save", command=save, bg="#27ae60", fg="white", width=20).pack(pady=20)

    def edit_user(self):
        selected = self.user_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user")
            return

        values = self.user_table.item(selected)["values"]
        user_id = values[0]
        role = values[2]
        email = values[3]

        window = tk.Toplevel(self.root)
        window.title("Edit User")
        window.geometry("300x250")
        window.transient(self.root)
        window.grab_set()

        tk.Label(window, text="Role", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10, 0))
        role_var = tk.StringVar(value=role)
        role_combo = ttk.Combobox(window, textvariable=role_var, values=["student", "lecturer", "admin"], width=28, state="readonly")
        role_combo.pack(padx=20, pady=(0, 10), fill="x")

        tk.Label(window, text="Email", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(0, 0))
        email_entry = tk.Entry(window, width=30)
        email_entry.insert(0, email)
        email_entry.pack(padx=20, pady=(0, 10), fill="x")

        def save():
            new_role = role_var.get()
            new_email = email_entry.get().strip()

            import json
            try:
                with open("data/users.json", "r", encoding="utf-8") as f:
                    users_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                messagebox.showerror("Error", f"Cannot read users.json: {str(e)}")
                return
            
            for u in users_data:
                if u["id"] == user_id:
                    u["role"] = new_role
                    u["email"] = new_email if new_email else ""
                    break
            
            try:
                with open("data/users.json", "w", encoding="utf-8") as f:
                    json.dump(users_data, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Success", "User updated successfully")
                window.destroy()
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save user: {str(e)}")

        tk.Button(window, text="Save", command=save, bg="#27ae60", fg="white", width=20).pack(pady=20)

    def delete_user(self):
        selected = self.user_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            user_id = self.user_table.item(selected)["values"][0]
            import json
            try:
                with open("data/users.json", "r", encoding="utf-8") as f:
                    users_data = json.load(f)
                
                users_data = [u for u in users_data if u["id"] != user_id]
                
                with open("data/users.json", "w", encoding="utf-8") as f:
                    json.dump(users_data, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Success", "User deleted successfully")
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error", f"Cannot delete user: {str(e)}")

    # LOGOUT

    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            try:
                AuthService.logout()
                self.root.switch_frame(LoginView)
            except AttributeError:
                messagebox.showerror("Error", "Cannot logout from this window")

    # REGISTRATION PERIOD ACTIONS

    def add_period(self):
        window = tk.Toplevel(self.root)
        window.title("Add Registration Period")
        window.geometry("450x500")
        window.transient(self.root)
        window.grab_set()

        tk.Label(window, text="Period Name", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        name_entry = tk.Entry(window, width=40)
        name_entry.pack(padx=20, pady=(0, 15), fill="x")

        # Start Date
        tk.Label(window, text="Start Date & Time", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(0, 5))
        start_frame = tk.Frame(window)
        start_frame.pack(padx=20, pady=(0, 15), fill="x")

        tk.Label(start_frame, text="YYYY-MM-DD", font=("Arial", 9)).pack(side="left", padx=(0, 5))
        start_date_entry = tk.Entry(start_frame, width=15)
        start_date_entry.pack(side="left", padx=(0, 10))

        tk.Label(start_frame, text="HH:MM:SS", font=("Arial", 9)).pack(side="left", padx=(0, 5))
        start_time_entry = tk.Entry(start_frame, width=15)
        start_time_entry.pack(side="left")

        # End Date
        tk.Label(window, text="End Date & Time", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(0, 5))
        end_frame = tk.Frame(window)
        end_frame.pack(padx=20, pady=(0, 20), fill="x")

        tk.Label(end_frame, text="YYYY-MM-DD", font=("Arial", 9)).pack(side="left", padx=(0, 5))
        end_date_entry = tk.Entry(end_frame, width=15)
        end_date_entry.pack(side="left", padx=(0, 10))

        tk.Label(end_frame, text="HH:MM:SS", font=("Arial", 9)).pack(side="left", padx=(0, 5))
        end_time_entry = tk.Entry(end_frame, width=15)
        end_time_entry.pack(side="left")

        # Insert default values
        today = datetime.now()
        start_date_entry.insert(0, today.strftime("%Y-%m-%d"))
        start_time_entry.insert(0, "00:00:00")
        end_date_entry.insert(0, (today).strftime("%Y-%m-%d"))
        end_time_entry.insert(0, "23:59:59")

        # Info frame
        info_frame = tk.LabelFrame(window, text="Quick Actions", font=("Arial", 9))
        info_frame.pack(padx=20, pady=(0, 15), fill="x")

        quick_buttons = tk.Frame(info_frame)
        quick_buttons.pack(fill="x", padx=10, pady=10)

        def set_today():
            today = datetime.now()
            start_date_entry.delete(0, tk.END)
            start_date_entry.insert(0, today.strftime("%Y-%m-%d"))
            start_time_entry.delete(0, tk.END)
            start_time_entry.insert(0, "00:00:00")
            end_date_entry.delete(0, tk.END)
            end_date_entry.insert(0, today.strftime("%Y-%m-%d"))
            end_time_entry.delete(0, tk.END)
            end_time_entry.insert(0, "23:59:59")

        def set_this_month():
            today = datetime.now()
            first_day = today.replace(day=1)
            if today.month == 12:
                last_day = today.replace(year=today.year+1, month=1, day=1)
            else:
                last_day = today.replace(month=today.month+1, day=1)
            last_day = last_day.replace(day=1) - __import__('datetime').timedelta(days=1)
            
            start_date_entry.delete(0, tk.END)
            start_date_entry.insert(0, first_day.strftime("%Y-%m-%d"))
            start_time_entry.delete(0, tk.END)
            start_time_entry.insert(0, "00:00:00")
            end_date_entry.delete(0, tk.END)
            end_date_entry.insert(0, last_day.strftime("%Y-%m-%d"))
            end_time_entry.delete(0, tk.END)
            end_time_entry.insert(0, "23:59:59")

        tk.Button(quick_buttons, text="Today", command=set_today, bg="#3498db", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(quick_buttons, text="This Month", command=set_this_month, bg="#3498db", fg="white", width=15).pack(side="left", padx=5)

        def save():
            name = name_entry.get().strip()
            start_date_str = start_date_entry.get().strip()
            start_time_str = start_time_entry.get().strip()
            end_date_str = end_date_entry.get().strip()
            end_time_str = end_time_entry.get().strip()

            if not name or not start_date_str or not start_time_str or not end_date_str or not end_time_str:
                messagebox.showwarning("Validation", "Please fill all fields")
                return

            try:
                start_date = f"{start_date_str}T{start_time_str}"
                end_date = f"{end_date_str}T{end_time_str}"
                
                # Validate date format
                datetime.fromisoformat(start_date)
                datetime.fromisoformat(end_date)
            except ValueError:
                messagebox.showerror("Error", "Invalid date/time format")
                return

            success, msg = RegistrationPeriodService.add_period(name, start_date, end_date)
            if success:
                messagebox.showinfo("Success", msg)
                window.destroy()
                self.load_periods()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(window, text="Save", command=save, bg="#27ae60", fg="white", width=40, font=("Arial", 10, "bold")).pack(pady=20)


    def edit_period(self):
        selected = self.period_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a period")
            return

        values = self.period_table.item(selected)["values"]
        period_id = values[0]

        window = tk.Toplevel(self.root)
        window.title("Edit Registration Period")
        window.geometry("450x500")
        window.transient(self.root)
        window.grab_set()

        tk.Label(window, text="Period Name", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        name_entry = tk.Entry(window, width=40)
        name_entry.insert(0, values[1])
        name_entry.pack(padx=20, pady=(0, 15), fill="x")

        # Start Date
        tk.Label(window, text="Start Date & Time", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(0, 5))
        start_frame = tk.Frame(window)
        start_frame.pack(padx=20, pady=(0, 15), fill="x")

        tk.Label(start_frame, text="YYYY-MM-DD", font=("Arial", 9)).pack(side="left", padx=(0, 5))
        start_date_entry = tk.Entry(start_frame, width=15)
        start_date_entry.pack(side="left", padx=(0, 10))
        start_date_entry.insert(0, values[2][:10])

        tk.Label(start_frame, text="HH:MM:SS", font=("Arial", 9)).pack(side="left", padx=(0, 5))
        start_time_entry = tk.Entry(start_frame, width=15)
        start_time_entry.pack(side="left")
        start_time_entry.insert(0, values[2][11:19])

        # End Date
        tk.Label(window, text="End Date & Time", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(0, 5))
        end_frame = tk.Frame(window)
        end_frame.pack(padx=20, pady=(0, 20), fill="x")

        tk.Label(end_frame, text="YYYY-MM-DD", font=("Arial", 9)).pack(side="left", padx=(0, 5))
        end_date_entry = tk.Entry(end_frame, width=15)
        end_date_entry.pack(side="left", padx=(0, 10))
        end_date_entry.insert(0, values[3][:10])

        tk.Label(end_frame, text="HH:MM:SS", font=("Arial", 9)).pack(side="left", padx=(0, 5))
        end_time_entry = tk.Entry(end_frame, width=15)
        end_time_entry.pack(side="left")
        end_time_entry.insert(0, values[3][11:19])

        def save():
            name = name_entry.get().strip()
            start_date_str = start_date_entry.get().strip()
            start_time_str = start_time_entry.get().strip()
            end_date_str = end_date_entry.get().strip()
            end_time_str = end_time_entry.get().strip()

            if not name or not start_date_str or not start_time_str or not end_date_str or not end_time_str:
                messagebox.showwarning("Validation", "Please fill all fields")
                return

            try:
                start_date = f"{start_date_str}T{start_time_str}"
                end_date = f"{end_date_str}T{end_time_str}"
                
                # Validate date format
                datetime.fromisoformat(start_date)
                datetime.fromisoformat(end_date)
            except ValueError:
                messagebox.showerror("Error", "Invalid date/time format")
                return

            success, msg = RegistrationPeriodService.update_period(period_id, name, start_date, end_date)
            if success:
                messagebox.showinfo("Success", msg)
                window.destroy()
                self.load_periods()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(window, text="Save", command=save, bg="#27ae60", fg="white", width=40, font=("Arial", 10, "bold")).pack(pady=20)

    def delete_period(self):
        selected = self.period_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a period")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this period?"):
            period_id = self.period_table.item(selected)["values"][0]
            success, msg = RegistrationPeriodService.delete_period(period_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.load_periods()
            else:
                messagebox.showerror("Error", msg)
