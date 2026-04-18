import csv
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from .assignment import AssignmentError, assign_students_to_projects, build_report, parse_projects, parse_student_rankings

SAMPLE_PROJECTS = """Project Apollo,4
Project Atlas,4
Project Beacon,5
Project Cypress,4
"""

SAMPLE_STUDENTS = """Alice: Project Apollo, Project Atlas, Project Beacon
Ben: Project Atlas, Project Cypress, Project Apollo
Carmen: Project Beacon, Project Apollo, Project Atlas
Diana: Project Cypress, Project Atlas, Project Apollo
"""

STYLE_BG = "#111111"
STYLE_PANEL = "#1A1A1A"
STYLE_ACCENT = "#FF9500"
STYLE_TEXT = "#FFFFFF"
STYLE_INPUT_BG = "#FFFFFF"
STYLE_INPUT_FG = "#000000"


def _choose_header_key(field_names, candidates):
    normalized = {name.strip().lower(): name for name in field_names if name}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    return None


class CapstoneMapperApp:
    """Tkinter desktop application for project assignment mapping."""

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.last_assignments: Dict[str, str | None] = {}
        master.title("Capstone Placement App")
        master.geometry("980x760")
        master.configure(bg=STYLE_BG)

        header = tk.Label(
            master,
            text="Capstone Placement App",
            font=("Segoe UI", 20, "bold"),
            bg=STYLE_BG,
            fg=STYLE_TEXT,
        )
        header.pack(padx=16, pady=(12, 6))

        subtitle = tk.Label(
            master,
            text="Use ranked student preferences and project capacities to generate team placement suggestions.",
            font=("Segoe UI", 10),
            bg=STYLE_BG,
            fg="#DDDDDD",
        )
        subtitle.pack(padx=16, pady=(0, 16))

        frame = tk.Frame(master, bg=STYLE_BG)
        frame.pack(fill="both", expand=True, padx=16, pady=6)

        left = tk.Frame(frame, bg=STYLE_PANEL, bd=0, relief="flat")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=2)

        right = tk.Frame(frame, bg=STYLE_PANEL, bd=0, relief="flat")
        right.pack(side="right", fill="both", expand=True, pady=2)

        self._build_input_panel(left)
        self._build_output_panel(right)

    def _build_input_panel(self, container: tk.Frame) -> None:
        label = tk.Label(
            container,
            text="Project Capacities",
            font=("Segoe UI", 12, "bold"),
            bg=STYLE_PANEL,
            fg=STYLE_ACCENT,
        )
        label.pack(anchor="w", padx=12, pady=(12, 6))

        self.projects_text = scrolledtext.ScrolledText(
            container,
            wrap="word",
            height=10,
            bg=STYLE_INPUT_BG,
            fg=STYLE_INPUT_FG,
            font=("Segoe UI", 10),
            relief="flat",
            padx=8,
            pady=8,
        )
        self.projects_text.pack(fill="both", expand=True, padx=12)
        self.projects_text.insert("1.0", SAMPLE_PROJECTS)

        loader_frame = tk.Frame(container, bg=STYLE_PANEL)
        loader_frame.pack(fill="x", padx=12, pady=(8, 0))

        project_import_button = tk.Button(
            loader_frame,
            text="Import Projects CSV",
            command=self.load_projects_csv,
            bg=STYLE_ACCENT,
            fg=STYLE_TEXT,
            activebackground="#FFB340",
            relief="flat",
            padx=10,
            pady=6,
        )
        project_import_button.pack(side="left", padx=(0, 6))

        tk.Label(
            container,
            text="Student Rankings",
            font=("Segoe UI", 12, "bold"),
            bg=STYLE_PANEL,
            fg=STYLE_ACCENT,
        ).pack(anchor="w", padx=12, pady=(16, 6))

        self.students_text = scrolledtext.ScrolledText(
            container,
            wrap="word",
            height=12,
            bg=STYLE_INPUT_BG,
            fg=STYLE_INPUT_FG,
            font=("Segoe UI", 10),
            relief="flat",
            padx=8,
            pady=8,
        )
        self.students_text.pack(fill="both", expand=True, padx=12)
        self.students_text.insert("1.0", SAMPLE_STUDENTS)

        student_import_frame = tk.Frame(container, bg=STYLE_PANEL)
        student_import_frame.pack(fill="x", padx=12, pady=(8, 0))

        student_import_button = tk.Button(
            student_import_frame,
            text="Import Students CSV",
            command=self.load_students_csv,
            bg=STYLE_ACCENT,
            fg=STYLE_TEXT,
            activebackground="#FFB340",
            relief="flat",
            padx=10,
            pady=6,
        )
        student_import_button.pack(side="left")

        button_frame = tk.Frame(container, bg=STYLE_PANEL)
        button_frame.pack(fill="x", padx=12, pady=14)

        assign_button = tk.Button(
            button_frame,
            text="Run Assignment",
            command=self.run_assignment,
            bg=STYLE_ACCENT,
            fg=STYLE_TEXT,
            activebackground="#FFB340",
            width=16,
            relief="flat",
            padx=10,
            pady=8,
        )
        assign_button.pack(side="left", padx=(0, 8))

        clear_button = tk.Button(
            button_frame,
            text="Clear Output",
            command=self.clear_output,
            bg="#333333",
            fg=STYLE_TEXT,
            activebackground="#4D4D4D",
            width=14,
            relief="flat",
            padx=10,
            pady=8,
        )
        clear_button.pack(side="left", padx=(0, 8))

        save_button = tk.Button(
            button_frame,
            text="Save CSV",
            command=self.save_csv,
            bg="#333333",
            fg=STYLE_TEXT,
            activebackground="#4D4D4D",
            width=12,
            relief="flat",
            padx=10,
            pady=8,
        )
        save_button.pack(side="left")

    def _build_output_panel(self, container: tk.Frame) -> None:
        label = tk.Label(
            container,
            text="Assignment Results",
            font=("Segoe UI", 12, "bold"),
            bg=STYLE_PANEL,
            fg=STYLE_ACCENT,
        )
        label.pack(anchor="w", padx=12, pady=(12, 6))

        self.output_text = scrolledtext.ScrolledText(
            container,
            wrap="word",
            height=34,
            bg="#121212",
            fg=STYLE_TEXT,
            font=("Segoe UI", 10),
            relief="flat",
            padx=8,
            pady=8,
            state="disabled",
        )
        self.output_text.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def set_output(self, content: str) -> None:
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, content)
        self.output_text.config(state="disabled")

    def clear_output(self) -> None:
        self.set_output("")

    def _load_csv_file(self, title: str) -> list[dict[str, str]]:
        path = filedialog.askopenfilename(
            title=title,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            return []

        try:
            with open(path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                if reader.fieldnames is None:
                    raise AssignmentError("CSV file must contain a header row.")
                return [row for row in reader if any(value.strip() for value in row.values() if value)]
        except OSError as error:
            raise AssignmentError(f"Could not read CSV file: {error}")

    def load_projects_csv(self) -> None:
        try:
            rows = self._load_csv_file("Import project capacities from CSV")
            if not rows:
                return
            field_names = rows[0].keys()
            project_key = _choose_header_key(field_names, ["project", "project name", "name"])
            capacity_key = _choose_header_key(field_names, ["capacity", "group size", "size"])
            if not project_key or not capacity_key:
                raise AssignmentError("Projects CSV requires headers like 'Project' and 'Capacity'.")

            lines = []
            for row in rows:
                project = row.get(project_key, "").strip()
                capacity = row.get(capacity_key, "").strip()
                if not project:
                    continue
                lines.append(f"{project},{capacity}")
            self.projects_text.delete("1.0", tk.END)
            self.projects_text.insert("1.0", "\n".join(lines))
        except AssignmentError as error:
            messagebox.showerror("Import Error", str(error))

    def load_students_csv(self) -> None:
        try:
            rows = self._load_csv_file("Import student rankings from CSV")
            if not rows:
                return
            field_names = rows[0].keys()
            student_key = _choose_header_key(field_names, ["student", "student name", "name"])
            ranking_key = _choose_header_key(field_names, ["rankings", "preferences", "choices"])
            if not student_key or not ranking_key:
                raise AssignmentError("Students CSV requires headers like 'Student' and 'Rankings'.")

            lines = []
            for row in rows:
                student = row.get(student_key, "").strip()
                ranking = row.get(ranking_key, "").strip()
                if not student:
                    continue
                lines.append(f"{student}: {ranking}")
            self.students_text.delete("1.0", tk.END)
            self.students_text.insert("1.0", "\n".join(lines))
        except AssignmentError as error:
            messagebox.showerror("Import Error", str(error))

    def run_assignment(self) -> None:
        project_text = self.projects_text.get("1.0", tk.END)
        student_text = self.students_text.get("1.0", tk.END)
        try:
            projects = parse_projects(project_text)
            students = parse_student_rankings(student_text)
            assignments = assign_students_to_projects(students, projects)
            self.last_assignments = assignments
            report = build_report(assignments)
            self.set_output(report)
        except AssignmentError as error:
            messagebox.showerror("Input Error", str(error))
        except Exception as error:
            messagebox.showerror("Unexpected Error", str(error))

    def save_csv(self) -> None:
        if not self.last_assignments:
            messagebox.showwarning("No Output", "Run the assignment before saving a CSV file.")
            return
        path = filedialog.asksaveasfilename(
            title="Save assignment results",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Student", "Assigned Project"])
                for student in sorted(self.last_assignments.keys()):
                    project = self.last_assignments[student]
                    writer.writerow([student, project or "Unassigned"])
            messagebox.showinfo("Saved", f"Assignment results saved to {path}")
        except OSError as error:
            messagebox.showerror("Save Error", str(error))
