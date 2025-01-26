import cx_Freeze
import sys
import os

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

# Define the include_files list
include_files = [
    "main_menu1.py", "main_menu2.py", "toolbar.py", "task.py", "settings.py", "preferences.py", "gui.py"
]

# Ensure the files exist
missing_files = [file for file in include_files if not os.path.exists(file)]
if missing_files:
    print(f"Warning: Cannot find file(s): {', '.join(missing_files)}")
    include_files = [file for file in include_files if file not in missing_files]

executables = [cx_Freeze.Executable("main.py", base=base, target_name="CleanNet_Manager_EXE")]

cx_Freeze.setup(
    name="CleanNet Manager",
    options={
        "build_exe": {
            "packages": ["tkinter", "os", "subprocess", "threading", "json", "shutil", "logging"],
            "include_files": include_files,
            "build_exe": "C:/Users/mrsch/Documents/Programming/Python (1)/CleanNet Manager/build"
        },
        "bdist_msi": {
            "upgrade_code": "{12345678-1234-1234-1234-123456789012}",
            "add_to_path": False,
            "initial_target_dir": r"[ProgramFilesFolder]\CleanNet Manager"
        }
    },
    version="1.0",
    description="A comprehensive tool to maintain and optimize your computer.",
    executables=executables
)
