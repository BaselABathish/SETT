import json
import tkinter as tk
from tkinter import ttk
import keyboard
import threading
import pyperclip
import time

with open('items.json', 'r') as f:
    items = json.load(f)


class QuickSelector:
    def __init__(self):
        self.root = None
        self.selected_item = None
        self.current_path = []  # Track navigation path
        self.current_data = items  # Current level data

    def create_window(self):
        if self.root is not None:
            self.root.destroy()

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.geometry('300x400+500+200')
        self.root.attributes('-alpha', 0.95)

        # Navigation label
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(fill='x', padx=10, pady=(10, 0))

        self.nav_label = ttk.Label(nav_frame, text=" > ".join(self.current_path) if self.current_path else "Root")
        self.nav_label.pack(side='left')

        # Back button if not at root
        if self.current_path:
            back_btn = ttk.Button(nav_frame, text="←", width=3, command=self.go_back)
            back_btn.pack(side='right')

        # Search entry
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill='x', padx=10, pady=10)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(fill='x')
        search_entry.focus()

        # Bind search
        self.search_var.trace('w', self.filter_list)

        # Listbox
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill='both', expand=True, padx=10, pady=10)

        # Load items for current level
        self.load_current_level_items()

        # Bind events
        self.listbox.bind('<Double-Button-1>', self.handle_selection)
        self.listbox.bind('<Return>', self.handle_selection)
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        search_entry.bind('<Escape>', lambda e: self.root.destroy())
        self.root.bind('<BackSpace>', lambda e: self.go_back())

        self.filter_list()

    def load_current_level_items(self):
        """Load items for the current navigation level"""
        self.listbox.delete(0, tk.END)

        # Navigate to current level in data
        current_level = items
        for key in self.current_path:
            current_level = current_level[key]

        self.current_data = current_level

        # Add items to listbox
        for key in current_level.keys():
            self.listbox.insert(tk.END, key)

        if self.listbox.size() > 0:
            self.listbox.selection_set(0)

    def filter_list(self, *args):
        search_term = self.search_var.get().lower()
        self.listbox.delete(0, tk.END)

        for key in self.current_data.keys():
            if search_term in key.lower():
                self.listbox.insert(tk.END, key)

        if self.listbox.size() > 0:
            self.listbox.selection_set(0)

    def handle_selection(self, event=None):
        selection = self.listbox.curselection()
        if selection:
            selected_key = self.listbox.get(selection[0])
            selected_value = self.current_data[selected_key]

            # If it's a dictionary, navigate deeper
            if isinstance(selected_value, dict):
                self.current_path.append(selected_key)
                self.create_window()  # Refresh window with new level
            else:
                # It's a final value, type it directly
                self.selected_item = str(selected_value)
                self.root.destroy()
                self.root = None
                self.type_content(self.selected_item)

    def type_content(self, content):
        """Type the content directly instead of copying to clipboard"""
        # Small delay to ensure window is closed and focus is returned
        time.sleep(0.1)
        # Write the content directly as keyboard input
        keyboard.write(content)

    def go_back(self):
        """Go back to previous level"""
        if self.current_path:
            self.current_path.pop()
            self.create_window()  # Refresh window with previous level

    def show(self):
        self.create_window()
        try:
            self.root.mainloop()
        except:
            pass


def start_selector():
    selector = QuickSelector()
    selector.show()


# Register hotkey
keyboard.add_hotkey('ctrl+space', start_selector)

print("Press Ctrl+Space to open selector. Press ESC to close.")
keyboard.wait()


