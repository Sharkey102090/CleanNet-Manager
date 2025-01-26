import sys
import os
from cx_Freeze import setup, Executable

# Print the current working directory for debugging
print("Current working directory:", os.getcwd())

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "packages": ["os", "tkinter", "subprocess", "threading", "json", "shutil", "logging"],
    "include_files": ["main_menu1.py", "main_menu2.py", "toolbar.py", "task.py", "settings.py", "preferences.py", "gui.py"]
}

# Base is set to "Win32GUI" to avoid the console window appearing.
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="CleanNet Manager",
    version="1.0",
    description="A comprehensive tool to maintain and optimize your computer.",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="CleanNetManager.exe")]
)
