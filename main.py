from datadivas.assignment import (
    parse_projects,
    parse_student_rankings,
    assign_students_to_projects,
    build_report,
    AssignmentError,
)


def main() -> None:
    """Read project and student data from files, perform assignment, and print report."""
    try:
        # Read project input from text file
        with open("projects.txt", "r") as f:
            project_text = f.read()
        
        # Read student rankings from text file
        with open("students.txt", "r") as f:
            student_text = f.read()
        
        # Parse the input data
        projects = parse_projects(project_text)
        students = parse_student_rankings(student_text)
        
        # Call the assignment function
        assignments = assign_students_to_projects(students, projects)
        
        # Print the formatted report
        report = build_report(assignments)
        print(report)
        
    except FileNotFoundError as e:
        print(f"Error: Could not find input file - {e}")
    except AssignmentError as e:
        print(f"Assignment Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
