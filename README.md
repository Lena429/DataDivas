# DataDivas

DataDivas is a desktop Python app that helps the ECCS chair map students to capstone projects using student-ranked project preferences.

## What it does

- Accepts a list of projects with capacities from 4 to 6 students per project.
- Accepts student preference rankings for those projects.
- Computes a capacity-aware assignment that seeks to honor each student's top choices.
- Provides a desktop GUI with results and CSV export.

## Features

- Standard-library Python implementation with no third-party dependencies.
- Tkinter desktop interface that runs on Windows and most standard Python installations.
- Robust validation and reusable assignment logic in `datadivas/assignment.py`.
- Unit tests under `tests/test_assignment.py`.

## Getting started

1. Install Python 3.9+ if needed.
2. Open a terminal in this repository.
3. Run the app:

```bash
python main.py
```

## Usage

1. Enter project capacities in the left panel using `Project Name,capacity` lines.
   - Capacities must be set between 4 and 6 inclusive.
2. Enter student rankings using `Student Name: Project 1, Project 2, ...` lines.
3. Optionally import project or student data from CSV using the provided buttons.
   - Projects CSV should include headers like `Project` and `Capacity`.
   - Students CSV should include headers like `Student` and `Rankings`.
4. Click `Run Assignment`.
5. Review the assignment results grouped by project.
6. Export to CSV if desired—results will list each student with their assigned project.

## Example Output

```
Project Apollo: Alice, Diana
Project Atlas: Ben, Frank
Project Beacon: Carmen
Unassigned: Eve
```

## Testing

Run the unit tests with:

```bash
python -m unittest discover -s tests
```

## File layout

- `main.py` — application entry point that launches the GUI.
- `datadivas/gui.py` — desktop interface implementation.
- `datadivas/assignment.py` — assignment and validation logic.
- `tests/test_assignment.py` — test coverage for parsing and assignment behavior.
- `ROBOTS.md` — AI/automation guidance.

## Design notes

- The algorithm honors student rankings and project capacity.
- Students may remain unassigned when project capacity is insufficient.
- The app can be extended with additional project constraints or group sizing rules.
