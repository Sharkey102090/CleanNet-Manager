import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json

PREFERENCES_FILE = "preferences.json"

class PreferencesDialog(tk.Toplevel):
    def __init__(self, master=None, preferences=None):
        super().__init__(master)
        self.title("Preferences")
        self.preferences = preferences or self.load_preferences()
        self.create_widgets()
        self.update_idletasks()  # Update the window to fit its contents
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}")

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Paths preferences
        self.paths_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.paths_frame, text="Paths")

        bold_underline_font = ("Helvetica", 10, "bold", "underline")

        self.downloads_path_label = ttk.Label(self.paths_frame, text="Downloads Path:", font=bold_underline_font)
        self.downloads_path_label.pack(anchor=tk.W, padx=10, pady=5)
        self.downloads_path_entry = ttk.Entry(self.paths_frame)
        self.downloads_path_entry.insert(0, self.preferences.get("downloads_path", os.path.expanduser("~\\Downloads")))
        self.downloads_path_entry.pack(fill=tk.X, padx=10, pady=5)
        self.downloads_path_button = ttk.Button(self.paths_frame, text="Create New File", command=self.create_new_downloads_file)
        self.downloads_path_button.pack(anchor=tk.W, padx=10, pady=5)

        self.documents_path_label = ttk.Label(self.paths_frame, text="Documents Path:", font=bold_underline_font)
        self.documents_path_label.pack(anchor=tk.W, padx=10, pady=5)
        self.documents_path_entry = ttk.Entry(self.paths_frame)
        self.documents_path_entry.insert(0, self.preferences.get("documents_path", os.path.expanduser("~\\Documents")))
        self.documents_path_entry.pack(fill=tk.X, padx=10, pady=5)
        self.documents_path_button = ttk.Button(self.paths_frame, text="Create New File", command=self.create_new_documents_file)
        self.documents_path_button.pack(anchor=tk.W, padx=10, pady=5)

        self.pictures_path_label = ttk.Label(self.paths_frame, text="Pictures Path:", font=bold_underline_font)
        self.pictures_path_label.pack(anchor=tk.W, padx=10, pady=5)
        self.pictures_path_entry = ttk.Entry(self.paths_frame)
        self.pictures_path_entry.insert(0, self.preferences.get("pictures_path", os.path.expanduser("~\\Pictures")))
        self.pictures_path_entry.pack(fill=tk.X, padx=10, pady=5)
        self.pictures_path_button = ttk.Button(self.paths_frame, text="Create New File", command=self.create_new_pictures_file)
        self.pictures_path_button.pack(anchor=tk.W, padx=10, pady=5)

        self.music_path_label = ttk.Label(self.paths_frame, text="Music Path:", font=bold_underline_font)
        self.music_path_label.pack(anchor=tk.W, padx=10, pady=5)
        self.music_path_entry = ttk.Entry(self.paths_frame)
        self.music_path_entry.insert(0, self.preferences.get("music_path", os.path.expanduser("~\\Music")))
        self.music_path_entry.pack(fill=tk.X, padx=10, pady=5)
        self.music_path_button = ttk.Button(self.paths_frame, text="Create New File", command=self.create_new_music_file)
        self.music_path_button.pack(anchor=tk.W, padx=10, pady=5)

        self.videos_path_label = ttk.Label(self.paths_frame, text="Videos Path:", font=bold_underline_font)
        self.videos_path_label.pack(anchor=tk.W, padx=10, pady=5)
        self.videos_path_entry = ttk.Entry(self.paths_frame)
        self.videos_path_entry.insert(0, self.preferences.get("videos_path", os.path.expanduser("~\\Videos")))
        self.videos_path_entry.pack(fill=tk.X, padx=10, pady=5)
        self.videos_path_button = ttk.Button(self.paths_frame, text="Create New File", command=self.create_new_videos_file)
        self.videos_path_button.pack(anchor=tk.W, padx=10, pady=5)

        # Save, Reset, and Cancel buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_preferences)
        self.save_button.pack(side=tk.RIGHT, padx=5)

        self.reset_button = ttk.Button(self.button_frame, text="Reset to Default", command=self.reset_to_default)
        self.reset_button.pack(side=tk.RIGHT, padx=5)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)

    def create_new_downloads_file(self):
        self.create_new_file(self.downloads_path_entry, "Downloads")

    def create_new_documents_file(self):
        self.create_new_file(self.documents_path_entry, "Documents")

    def create_new_pictures_file(self):
        self.create_new_file(self.pictures_path_entry, "Pictures")

    def create_new_music_file(self):
        self.create_new_file(self.music_path_entry, "Music")

    def create_new_videos_file(self):
        self.create_new_file(self.videos_path_entry, "Videos")

    def create_new_file(self, entry, folder_name):
        initial_dir = os.path.expanduser(f"~\\{folder_name}")
        file_path = filedialog.asksaveasfilename(initialdir=initial_dir, defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write("")
                entry.delete(0, tk.END)
                entry.insert(0, file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create file: {e}")
        self.focus_set()

    def save_preferences(self):
        self.preferences["downloads_path"] = self.downloads_path_entry.get()
        self.preferences["documents_path"] = self.documents_path_entry.get()
        self.preferences["pictures_path"] = self.pictures_path_entry.get()
        self.preferences["music_path"] = self.music_path_entry.get()
        self.preferences["videos_path"] = self.videos_path_entry.get()
        try:
            with open(PREFERENCES_FILE, 'w') as f:
                json.dump(self.preferences, f)
            messagebox.showinfo("Preferences", "Preferences saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save preferences: {e}")
        self.destroy()

    def reset_to_default(self):
        self.downloads_path_entry.delete(0, tk.END)
        self.downloads_path_entry.insert(0, os.path.expanduser("~\\Downloads"))
        self.documents_path_entry.delete(0, tk.END)
        self.documents_path_entry.insert(0, os.path.expanduser("~\\Documents"))
        self.pictures_path_entry.delete(0, tk.END)
        self.pictures_path_entry.insert(0, os.path.expanduser("~\\Pictures"))
        self.music_path_entry.delete(0, tk.END)
        self.music_path_entry.insert(0, os.path.expanduser("~\\Music"))
        self.videos_path_entry.delete(0, tk.END)
        self.videos_path_entry.insert(0, os.path.expanduser("~\\Videos"))

    def load_preferences(self):
        if os.path.exists(PREFERENCES_FILE):
            try:
                with open(PREFERENCES_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Failed to decode preferences file: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load preferences: {e}")
        return {}

    def focus_set(self):
        self.lift()
        self.focus_force()