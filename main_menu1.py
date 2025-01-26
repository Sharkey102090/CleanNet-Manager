import tkinter as tk
from tkinter import ttk
from task import clean_recycle_bin, clear_cookies, clear_temp_files, clear_internet_history, update_all_packages, check_registry_errors, sort_downloads
from settings import RECYCLE_BIN_PATH  # Import the path from settings
import threading
import subprocess
from main_menu2 import MainMenuPart2
import json
import os
import time

SCHEDULE_FILE = "schedule.json"

class MainMenu(tk.Frame):
    def __init__(self, master=None, preferences=None):
        super().__init__(master)
        self.master = master
        self.preferences = preferences or {
            "clean_recycle_bin": True,
            "clear_cookies": True,
            "clear_temp_files": True,
            "clear_internet_history": True
        }
        self.part2 = MainMenuPart2(self)  # Initialize MainMenuPart2
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_schedule()
        self.start_scheduled_scans()

    def create_widgets(self):
        # Progress bar and label
        self.progress_var = tk.DoubleVar()
        self.progress_frame = tk.Frame(self)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, side=tk.LEFT, expand=True)

        self.progress_label = tk.Label(self.progress_frame, text="0%")
        self.progress_label.pack(side=tk.RIGHT)

        # Countdown timer label
        self.countdown_label = tk.Label(self, text="Next scan in: --:--:--", font=("Helvetica", 12))
        self.countdown_label.pack(pady=10)

        # Cleaning section
        self.cleaning_frame = tk.Frame(self)
        self.cleaning_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.N)
        self.clean_label = tk.Label(self.cleaning_frame, text="Cleaning", font=("Helvetica", 12, "bold", "underline"))
        self.clean_label.pack(anchor=tk.W, padx=10, pady=5)

        button_options = {
            "relief": tk.RAISED,
            "bd": 2,
            "activebackground": "#d9d9d9"
        }

        if self.preferences.get("clean_recycle_bin"):
            self.clean_button = tk.Button(self.cleaning_frame, text="Clean Recycle Bin", command=lambda: self.start_task("Clean Recycle Bin", clean_recycle_bin), **button_options)
            self.clean_button.pack(anchor=tk.W, padx=10, pady=5)

        if self.preferences.get("clear_cookies"):
            self.cookies_button = tk.Button(self.cleaning_frame, text="Clear Cookies", command=lambda: self.start_task("Clear Cookies", clear_cookies), **button_options)
            self.cookies_button.pack(anchor=tk.W, padx=10, pady=5)

        if self.preferences.get("clear_temp_files"):
            self.temp_files_button = tk.Button(self.cleaning_frame, text="Clear Temp Files", command=lambda: self.start_task("Clear Temp Files", clear_temp_files), **button_options)
            self.temp_files_button.pack(anchor=tk.W, padx=10, pady=5)

        if self.preferences.get("clear_internet_history"):
            self.clear_history_button = tk.Button(self.cleaning_frame, text="Clear Internet History", command=lambda: self.start_task("Clear Internet History", clear_internet_history), **button_options)
            self.clear_history_button.pack(anchor=tk.W, padx=10, pady=5)

        self.sort_downloads_button = tk.Button(self.cleaning_frame, text="Sort Downloads", command=lambda: self.start_task("Sort Downloads", sort_downloads), **button_options)
        self.sort_downloads_button.pack(anchor=tk.W, padx=10, pady=5)

        # Adding space before Software section
        tk.Label(self.cleaning_frame, text="").pack()
        tk.Label(self.cleaning_frame, text="").pack()

        # Software section
        self.software_label = tk.Label(self.cleaning_frame, text="Software", font=("Helvetica", 12, "bold", "underline"))
        self.software_label.pack(anchor=tk.W, padx=10, pady=5)

        self.update_packages_button = tk.Button(self.cleaning_frame, text="Update All Packages", command=lambda: self.start_task("Update All Packages", update_all_packages), **button_options)
        self.update_packages_button.pack(anchor=tk.W, padx=10, pady=5)

        self.check_registry_button = tk.Button(self.cleaning_frame, text="Check Registry Errors", command=lambda: self.start_task("Check Registry Errors", check_registry_errors), **button_options)
        self.check_registry_button.pack(anchor=tk.W, padx=10, pady=5)

        # Run All Scans button
        self.run_all_scans_button = tk.Button(self.cleaning_frame, text="Run All Scans", command=self.run_all_scans, **button_options)
        self.run_all_scans_button.pack(anchor=tk.W, padx=10, pady=10)

        # Task summary box with scrollbar
        self.task_summary_frame = tk.Frame(self)
        self.task_summary_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.task_summary_scrollbar = tk.Scrollbar(self.task_summary_frame)
        self.task_summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_summary = tk.Text(self.task_summary_frame, height=15, width=40, yscrollcommand=self.task_summary_scrollbar.set)
        self.task_summary.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.task_summary_scrollbar.config(command=self.task_summary.yview)
        self.task_summary.config(state=tk.DISABLED)

        # Clear button frame
        self.clear_button_frame = tk.Frame(self)
        self.clear_button_frame.pack(pady=10)
        self.clear_button = tk.Button(self.clear_button_frame, text="Clear", command=self.clear_task_summary)
        self.clear_button.pack()

        # Networking section
        self.networking_frame = tk.Frame(self)
        self.networking_frame.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.N)

        self.networking_label = tk.Label(self.networking_frame, text="Networking", font=("Helvetica", 12, "bold", "underline"))
        self.networking_label.pack(anchor=tk.E, padx=10, pady=5)

        self.ping_test_button = tk.Button(self.networking_frame, text="Ping Test to Google", command=self.part2.ping_test, **button_options)
        self.ping_test_button.pack(anchor=tk.E, padx=10, pady=5)

        self.ipconfig_all_button = tk.Button(self.networking_frame, text="IPConfig /all", command=self.part2.ipconfig_all, **button_options)
        self.ipconfig_all_button.pack(anchor=tk.E, padx=10, pady=5)

        self.ipconfig_release_button = tk.Button(self.networking_frame, text="IPConfig /release", command=self.part2.ipconfig_release, **button_options)
        self.ipconfig_release_button.pack(anchor=tk.E, padx=10, pady=5)

        self.ipconfig_renew_button = tk.Button(self.networking_frame, text="IPConfig /renew", command=self.part2.ipconfig_renew, **button_options)
        self.ipconfig_renew_button.pack(anchor=tk.E, padx=10, pady=5)

        self.run_all_tests_button = tk.Button(self.networking_frame, text="Run All Tests", command=self.run_all_network_tests, **button_options)
        self.run_all_tests_button.pack(anchor=tk.E, padx=10, pady=10)

        # Adding space before "More to Come"
        tk.Label(self.networking_frame, text="").pack()
        tk.Label(self.networking_frame, text="").pack()

        self.more_to_come_label = tk.Label(self.networking_frame, text="More to Come", font=("Helvetica", 12, "bold", "underline"))
        self.more_to_come_label.pack(anchor=tk.E, padx=10, pady=5)

    def start_task(self, task_name, task_func):
        threading.Thread(target=self.run_task, args=(task_name, task_func)).start()

    def run_task(self, task_name, task_func):
        self.progress_var.set(0)
        self.update_task_summary(f"Starting task: {task_name}\n")
        try:
            task_func()
            self.progress_var.set(100)
            self.progress_label.config(text="100%")
            self.update_task_summary(f"Task completed: {task_name}\n")
        except Exception as e:
            self.update_task_summary(f"Error in task {task_name}: {str(e)}\n")

    def run_all_tasks(self):
        threading.Thread(target=self.run_task_sequence).start()

    def run_task_sequence(self):
        tasks = []
        if self.preferences.get("clean_recycle_bin"):
            tasks.append(("Clean Recycle Bin", clean_recycle_bin))
        if self.preferences.get("clear_cookies"):
            tasks.append(("Clear Cookies", clear_cookies))
        if self.preferences.get("clear_temp_files"):
            tasks.append(("Clear Temp Files", clear_temp_files))
        if self.preferences.get("clear_internet_history"):
            tasks.append(("Clear Internet History", clear_internet_history))
        tasks.append(("Sort Downloads", sort_downloads))

        total_tasks = len(tasks)
        self.progress_var.set(0)
        self.task_summary.config(state=tk.NORMAL)
        self.task_summary.delete('1.0', tk.END)
        self.task_summary.config(state=tk.DISABLED)
        for index, (task_name, task) in enumerate(tasks):
            self.update_task_summary(f"Starting task: {task_name}\n")
            try:
                task()
                self.progress_var.set((index + 1) / total_tasks * 100)
                self.progress_label.config(text=f"{int(self.progress_var.get())}%")
                self.update_task_summary(f"Task completed: {task_name}\n")
            except Exception as e:
                self.update_task_summary(f"Error in task {task_name}: {str(e)}\n")
            self.master.update_idletasks()
        self.update_task_summary("All cleaning tasks completed.\n")

    def run_all_software_tasks(self):
        threading.Thread(target=self.run_software_task_sequence).start()

    def run_software_task_sequence(self):
        tasks = [("Update All Packages", update_all_packages), ("Check Registry Errors", check_registry_errors)]
        total_tasks = len(tasks)
        self.progress_var.set(0)
        self.task_summary.config(state=tk.NORMAL)
        self.task_summary.delete('1.0', tk.END)
        self.task_summary.config(state=tk.DISABLED)
        for index, (task_name, task) in enumerate(tasks):
            self.update_task_summary(f"Starting task: {task_name}\n")
            try:
                task()
                self.progress_var.set((index + 1) / total_tasks * 100)
                self.progress_label.config(text=f"{int(self.progress_var.get())}%")
                self.update_task_summary(f"Task completed: {task_name}\n")
            except Exception as e:
                self.update_task_summary(f"Error in task {task_name}: {str(e)}\n")
            self.master.update_idletasks()
        self.update_task_summary("All software tasks completed.\n")

    def run_all_network_tests(self):
        threading.Thread(target=self.run_network_test_sequence).start()

    def run_network_test_sequence(self):
        tests = [("Ping Test to Google", self.part2.ping_test), ("IPConfig /all", self.part2.ipconfig_all), ("IPConfig /release", self.part2.ipconfig_release), ("IPConfig /renew", self.part2.ipconfig_renew)]
        total_tests = len(tests)
        self.progress_var.set(0)
        self.task_summary.config(state=tk.NORMAL)
        self.task_summary.delete('1.0', tk.END)
        self.task_summary.config(state=tk.DISABLED)
        for index, (test_name, test) in enumerate(tests):
            self.update_task_summary(f"Starting test: {test_name}\n")
            try:
                test()
                self.progress_var.set((index + 1) / total_tests * 100)
                self.progress_label.config(text=f"{int(self.progress_var.get())}%")
                self.update_task_summary(f"Test completed: {test_name}\n")
            except Exception as e:
                self.update_task_summary(f"Error in test {test_name}: {str(e)}\n")
            self.master.update_idletasks()
        self.update_task_summary("All network tests completed.\n")

    def run_all_scans(self):
        threading.Thread(target=self.run_all_scans_sequence).start()

    def run_all_scans_sequence(self):
        self.run_task_sequence()
        self.run_software_task_sequence()
        self.run_network_test_sequence()

    def update_task_summary(self, message):
        self.task_summary.config(state=tk.NORMAL)
        self.task_summary.insert(tk.END, message)
        self.task_summary.config(state=tk.DISABLED)

    def clear_task_summary(self):
        self.task_summary.config(state=tk.NORMAL)
        self.task_summary.delete('1.0', tk.END)
        self.task_summary.config(state=tk.DISABLED)

    def load_schedule(self):
        if os.path.exists(SCHEDULE_FILE):
            with open(SCHEDULE_FILE, "r") as file:
                self.schedule = json.load(file)
        else:
            self.schedule = {}

    def save_schedule(self):
        with open(SCHEDULE_FILE, "w") as file:
            json.dump(self.schedule, file)

    def start_scheduled_scans(self):
        threading.Thread(target=self.run_scheduled_scans).start()
        self.update_countdown_label()

    def run_scheduled_scans(self):
        while True:
            current_time = time.strftime("%H:%M")
            interval = self.schedule.get("interval", "")
            if interval == "10 mins":
                self.run_scheduled_task(10)
            elif interval == "30 mins":
                self.run_scheduled_task(30)
            elif interval == "1 hr":
                self.run_scheduled_task(60)
            elif interval == "On Startup":
                self.run_scheduled_task_on_startup()
            time.sleep(1)

    def run_scheduled_task(self, minutes):
        last_run_file = "last_run.json"
        last_run_time = self.load_last_run_time(last_run_file)
        current_time = time.time()
        if current_time - last_run_time >= minutes * 60:
            self.run_selected_scans()
            self.save_last_run_time(last_run_file, current_time)

    def run_scheduled_task_on_startup(self):
        startup_file = "startup_run.json"
        if not os.path.exists(startup_file):
            self.run_selected_scans()
            with open(startup_file, "w") as file:
                file.write("")

    def run_selected_scans(self):
        tasks = []
        if self.preferences.get("clean_recycle_bin"):
            tasks.append(("Clean Recycle Bin", clean_recycle_bin))
        if self.preferences.get("clear_cookies"):
            tasks.append(("Clear Cookies", clear_cookies))
        if self.preferences.get("clear_temp_files"):
            tasks.append(("Clear Temp Files", clear_temp_files))
        if self.preferences.get("clear_internet_history"):
            tasks.append(("Clear Internet History", clear_internet_history))
        if self.preferences.get("update_packages"):
            tasks.append(("Update All Packages", update_all_packages))
        if self.preferences.get("check_registry"):
            tasks.append(("Check Registry Errors", check_registry_errors))
        if self.preferences.get("sort_downloads"):
            tasks.append(("Sort Downloads", sort_downloads))

        total_tasks = len(tasks)
        self.progress_var.set(0)
        self.task_summary.config(state=tk.NORMAL)
        self.task_summary.delete('1.0', tk.END)
        self.task_summary.config(state=tk.DISABLED)
        for index, (task_name, task) in enumerate(tasks):
            self.update_task_summary(f"Starting task: {task_name}\n")
            try:
                task()
                self.progress_var.set((index + 1) / total_tasks * 100)
                self.progress_label.config(text=f"{int(self.progress_var.get())}%")
                self.update_task_summary(f"Task completed: {task_name}\n")
            except Exception as e:
                self.update_task_summary(f"Error in task {task_name}: {str(e)}\n")
            self.master.update_idletasks()
        self.update_task_summary("All selected tasks completed.\n")

    def load_last_run_time(self, last_run_file):
        if os.path.exists(last_run_file):
            with open(last_run_file, "r") as file:
                return float(file.read())
        return 0

    def save_last_run_time(self, last_run_file, current_time):
        with open(last_run_file, "w") as file:
            file.write(str(current_time))

    def update_countdown_label(self):
        interval = self.schedule.get("interval", "")
        last_run_file = "last_run.json"
        last_run_time = self.load_last_run_time(last_run_file)
        current_time = time.time()
        if interval == "10 mins":
            next_run_time = last_run_time + 10 * 60
        elif interval == "30 mins":
            next_run_time = last_run_time + 30 * 60
        elif interval == "1 hr":
            next_run_time = last_run_time + 60 * 60
        else:
            next_run_time = current_time

        time_remaining = max(0, next_run_time - current_time)
        hours, remainder = divmod(time_remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.countdown_label.config(text=f"Next scan in: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
        self.master.after(1000, self.update_countdown_label)  # Schedule the next update
