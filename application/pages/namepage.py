"""Main page for the email application."""
import tkinter as tk


class NamePage(tk.Frame):
    """Main page for application."""

    def __init__(self, parent):
        """Initialise Home Page class."""
        super().__init__()
        self.parent = parent
        # self.parent.geometry("200x300")
        self.create_widgets()

    def create_widgets(self):
        """Create the pages widgets."""
        tk.Label(self, text="fuck").grid()
