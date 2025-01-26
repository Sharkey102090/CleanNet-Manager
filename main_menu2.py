import subprocess
import ctypes

class MainMenu:
    def __init__(self):
        self.task_summary = ""

    def update_task_summary(self, message):
        self.task_summary += message

class MainMenuPart2:
    def __init__(self, main_menu):
        self.main_menu = main_menu

    def ping_test(self):
        self.main_menu.update_task_summary("Running ping test to Google...\n")
        try:
            result = subprocess.run(["ping", "google.com"], capture_output=True, text=True)
            self.main_menu.update_task_summary(result.stdout + "\n")
        except Exception as e:
            self.main_menu.update_task_summary(f"Error during ping test: {str(e)}\n")
        self.main_menu.update_task_summary("Ping test to Google completed.\n")

    def ipconfig_all(self):
        self.main_menu.update_task_summary("Running IPConfig /all...\n")
        try:
            result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True)
            self.main_menu.update_task_summary(result.stdout + "\n")
        except Exception as e:
            self.main_menu.update_task_summary(f"Error during IPConfig /all: {str(e)}\n")
        self.main_menu.update_task_summary("IPConfig /all completed.\n")

    def ipconfig_release(self):
        self.main_menu.update_task_summary("Running IPConfig /release...\n")
        try:
            result = subprocess.run(["ipconfig", "/release"], capture_output=True, text=True)
            self.main_menu.update_task_summary(result.stdout + "\n")
        except Exception as e:
            self.main_menu.update_task_summary(f"Error during IPConfig /release: {str(e)}\n")
        self.main_menu.update_task_summary("IPConfig /release completed.\n")

    def ipconfig_renew(self):
        self.main_menu.update_task_summary("Running IPConfig /renew...\n")
        try:
            result = subprocess.run(["ipconfig", "/renew"], capture_output=True, text=True)
            self.main_menu.update_task_summary(result.stdout + "\n")
        except Exception as e:
            self.main_menu.update_task_summary(f"Error during IPConfig /renew: {str(e)}\n")
        self.main_menu.update_task_summary("IPConfig /renew completed.\n")
