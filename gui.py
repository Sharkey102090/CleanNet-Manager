import tkinter as tk
from main_menu1 import MainMenu  # Update import statement
from toolbar import Toolbar
import settings  # Add the settings import

# ...existing code...

class CleanNetManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CleanNet Manager")
        self.root.geometry("1100x600")  # Set the initial size of the window (width x height)
        self.main_menu = MainMenu(master=self.root)
        self.toolbar = Toolbar(master=self.root, main_menu=self.main_menu)
        self.root.config(menu=self.toolbar)
        self.dark_mode = False
        self.root.bind("<<ToggleDarkMode>>", self.toggle_dark_mode)

    def toggle_dark_mode(self, event=None):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.root.tk_setPalette(background="#1e1e1e", foreground="#cfcfcf", activeBackground="#3e3e3e", activeForeground="#cfcfcf")
            self.main_menu.configure(bg="#1e1e1e", fg="#cfcfcf")
            self.toolbar.configure(bg="#1e1e1e", fg="#cfcfcf")
            self.update_button_styles("#3e3e3e", "#cfcfcf")
        else:
            self.root.tk_setPalette(background="#f0f0f0", foreground="#000000", activeBackground="#e0e0e0", activeForeground="#000000")
            self.main_menu.configure(bg="#f0f0f0", fg="#000000")
            self.toolbar.configure(bg="#f0f0f0", fg="#000000")
            self.update_button_styles("#d9d9d9", "#000000")

    def update_button_styles(self, active_bg, fg):
        for widget in self.main_menu.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(activebackground=active_bg, foreground=fg)

    def run(self):
        self.main_menu.mainloop()
