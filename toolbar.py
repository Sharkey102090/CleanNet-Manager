import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel, Label, Text, Scrollbar
import webbrowser
import subprocess
from preferences import PreferencesDialog
from scan_settings import ScanSettingsDialog  # Import the ScanSettingsDialog
from main_menu1 import MainMenu  # Update import statement

class Toolbar(tk.Menu):
    def __init__(self, master=None, main_menu=None):
        super().__init__(master)
        self.master = master
        self.main_menu = main_menu
        self.create_widgets()

    def create_widgets(self):
        # File menu
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(self, tearoff=0)
        edit_menu.add_command(label="Preferences", command=self.show_preferences)
        edit_menu.add_command(label="Settings", command=self.show_scan_settings)  # Add Settings option
        self.add_cascade(label="Edit", menu=edit_menu)

        # View menu
        view_menu = tk.Menu(self, tearoff=0)
        view_menu.add_command(label="Toggle Fullscreen", command=self.toggle_fullscreen)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.add_cascade(label="View", menu=view_menu)

        # Tools menu
        tools_menu = tk.Menu(self, tearoff=0)
        scans_menu = tk.Menu(tools_menu, tearoff=0)
        scans_menu.add_command(label="Run All Cleaning Tasks", command=self.main_menu.run_all_tasks)
        scans_menu.add_command(label="Run All Software Tasks", command=self.main_menu.run_all_software_tasks)
        scans_menu.add_command(label="Run All Network Tests", command=self.main_menu.run_all_network_tests)
        tools_menu.add_cascade(label="Scans", menu=scans_menu)
        self.add_cascade(label="Tools", menu=tools_menu)

        # Help menu
        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Contact Information", command=self.show_contact_info)
        self.add_cascade(label="Help", menu=help_menu)

    def show_about(self):
        about_window = Toplevel(self.master)
        about_window.title("About CleanNet Manager")
        about_window.geometry("500x300")

        about_text = (
            "CleanNet Manager\n\n"
            "CleanNet Manager is a comprehensive tool designed to help you maintain and optimize your computer. "
            "With a variety of features, it ensures your system stays clean and efficient. The key functionalities include:\n\n"
            "- Cleaning the recycle bin\n"
            "- Clearing cookies\n"
            "- Removing temporary files\n"
            "- Clearing internet history\n"
            "- Updating installed packages\n"
            "- Checking and correcting registry errors\n"
            "- Sorting downloads\n\n"
            "For more information, please contact support in the Contact Information."
        )

        text_widget = Text(about_window, wrap=tk.WORD, padx=10, pady=10, font=("Helvetica", 10))
        text_widget.insert(tk.END, about_text)
        text_widget.tag_configure("link", foreground="blue", underline=True)
        text_widget.tag_bind("link", "<Button-1>", lambda e: self.show_contact_info())
        text_widget.insert(tk.END, "\n\nContact Information", "link")
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(about_window, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_contact_info(self):
        contact_window = Toplevel(self.master)
        contact_window.title("Contact Information")
        contact_window.geometry("300x150")

        maker_label = Label(contact_window, text="Maker: Adam Schanuth", font=("Helvetica", 10))
        maker_label.pack(pady=5)

        email_label = Label(contact_window, text="Email: mrschanuth@outlook.com", font=("Helvetica", 10), fg="blue", cursor="hand2")
        email_label.pack(pady=5)
        email_label.bind("<Button-1>", lambda e: webbrowser.open("mailto:mrschanuth@outlook.com"))

        phone_label = Label(contact_window, text="Phone: 816-565-1302", font=("Helvetica", 10))
        phone_label.pack(pady=5)

    def show_preferences(self):
        PreferencesDialog(self.master)

    def show_scan_settings(self):
        ScanSettingsDialog(self.master, preferences=self.main_menu.preferences)  # Open ScanSettingsDialog

    def toggle_fullscreen(self):
        self.master.attributes("-fullscreen", not self.master.attributes("-fullscreen"))

    def toggle_dark_mode(self):
        self.master.event_generate("<<ToggleDarkMode>>")
