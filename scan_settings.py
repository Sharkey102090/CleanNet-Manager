import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

SCHEDULE_FILE = "schedule.json"

class ScanSettingsDialog(tk.Toplevel):
    def __init__(self, master=None, preferences=None):
        super().__init__(master)
        self.title("Scan Settings")
        self.preferences = preferences or {}
        self.schedule = self.load_schedule()
        self.create_widgets()
        self.update_idletasks()  # Update the window to fit its contents
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}")

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Scan settings
        self.scan_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scan_frame, text="Scan Settings")

        bold_underline_font = ("Helvetica", 10, "bold", "underline")

        self.clean_recycle_bin_var = tk.BooleanVar(value=self.preferences.get("clean_recycle_bin", True))
        self.clean_recycle_bin_check = ttk.Checkbutton(self.scan_frame, text="Clean Recycle Bin", variable=self.clean_recycle_bin_var)
        self.clean_recycle_bin_check.pack(anchor=tk.W, padx=10, pady=5)

        self.clear_cookies_var = tk.BooleanVar(value=self.preferences.get("clear_cookies", True))
        self.clear_cookies_check = ttk.Checkbutton(self.scan_frame, text="Clear Cookies", variable=self.clear_cookies_var)
        self.clear_cookies_check.pack(anchor=tk.W, padx=10, pady=5)

        self.clear_temp_files_var = tk.BooleanVar(value=self.preferences.get("clear_temp_files", True))
        self.clear_temp_files_check = ttk.Checkbutton(self.scan_frame, text="Clear Temp Files", variable=self.clear_temp_files_var)
        self.clear_temp_files_check.pack(anchor=tk.W, padx=10, pady=5)

        self.clear_internet_history_var = tk.BooleanVar(value=self.preferences.get("clear_internet_history", True))
        self.clear_internet_history_check = ttk.Checkbutton(self.scan_frame, text="Clear Internet History", variable=self.clear_internet_history_var)
        self.clear_internet_history_check.pack(anchor=tk.W, padx=10, pady=5)

        self.update_packages_var = tk.BooleanVar(value=self.preferences.get("update_packages", True))
        self.update_packages_check = ttk.Checkbutton(self.scan_frame, text="Update All Packages", variable=self.update_packages_var)
        self.update_packages_check.pack(anchor=tk.W, padx=10, pady=5)

        self.check_registry_var = tk.BooleanVar(value=self.preferences.get("check_registry", True))
        self.check_registry_check = ttk.Checkbutton(self.scan_frame, text="Check Registry Errors", variable=self.check_registry_var)
        self.check_registry_check.pack(anchor=tk.W, padx=10, pady=5)

        self.sort_downloads_var = tk.BooleanVar(value=self.preferences.get("sort_downloads", True))
        self.sort_downloads_check = ttk.Checkbutton(self.scan_frame, text="Sort Downloads", variable=self.sort_downloads_var)
        self.sort_downloads_check.pack(anchor=tk.W, padx=10, pady=5)

        # Schedule settings
        self.schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.schedule_frame, text="Schedule Settings")

        self.schedule_label = ttk.Label(self.schedule_frame, text="Schedule Automated Scans", font=bold_underline_font)
        self.schedule_label.pack(anchor=tk.W, padx=10, pady=5)

        self.schedule_var = tk.StringVar(value=self.schedule.get("interval", ""))
        self.schedule_options = ["10 mins", "30 mins", "1 hr", "On Startup"]
        self.schedule_menu = ttk.OptionMenu(self.schedule_frame, self.schedule_var, self.schedule_options[0], *self.schedule_options)
        self.schedule_menu.pack(fill=tk.X, padx=10, pady=5)

        self.schedule_button = ttk.Button(self.schedule_frame, text="Set Schedule", command=self.set_schedule)
        self.schedule_button.pack(anchor=tk.W, padx=10, pady=5)

        # Save and Cancel buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_settings)
        self.save_button.pack(side=tk.RIGHT, padx=5)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)

    def set_schedule(self):
        interval = self.schedule_var.get()
        if interval:
            self.schedule["interval"] = interval
            self.save_schedule()
            messagebox.showinfo("Schedule", "Schedule set successfully.")
        else:
            messagebox.showerror("Error", "Please select a valid interval.")

    def save_settings(self):
        self.preferences["clean_recycle_bin"] = self.clean_recycle_bin_var.get()
        self.preferences["clear_cookies"] = self.clear_cookies_var.get()
        self.preferences["clear_temp_files"] = self.clear_temp_files_var.get()
        self.preferences["clear_internet_history"] = self.clear_internet_history_var.get()
        self.preferences["update_packages"] = self.update_packages_var.get()
        self.preferences["check_registry"] = self.check_registry_var.get()
        self.preferences["sort_downloads"] = self.sort_downloads_var.get()
        self.destroy()

    def load_schedule(self):
        if os.path.exists(SCHEDULE_FILE):
            try:
                with open(SCHEDULE_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Failed to decode schedule file: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load schedule: {e}")
        return {}

    def save_schedule(self):
        try:
            with open(SCHEDULE_FILE, 'w') as f:
                json.dump(self.schedule, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save schedule: {e}")
