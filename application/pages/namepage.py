"""Chat page for the chat application."""

import tkinter as tk


class NamePage(tk.Frame):
    """Chat page for Application."""

    def __init__(self, parent):
        """Initialise the Example page."""
        # So i can display the messages line by line
        super().__init__()
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.parent = parent
        self.parent.geometry("300x100")
        self.create_widgets()

    def create_widgets(self):
        """Create the pages widgets."""
        tk.Label(self, text="Choose a username", font=("roboto", 24)).grid()
        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.grid()
        self.proceedBtn = tk.Button(self,
                                    text="Proceed",
                                    command=lambda:
                                    self.proceed(self.usernameEntry.get())
                                    )
        self.proceedBtn.grid()

    def proceed(self, username):
        """Contact the main application with the username."""
        self.parent.establishConnection()
