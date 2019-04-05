"""Client app for the chat app."""
import tkinter as tk
from pages.mainpage import MainWindow


class Application(tk.Tk):
    """Application class inheriting from tk.Tk."""

    def __init__(self):
        """Initialise the Application class."""
        super().__init__()
        self.create_pages()
        self.protocol("WM_DELETE_WINDOW", self.quit())

    def create_pages(self):
        """Create the pages used inside the application."""
        self.pages = {}

        self.pages[MainWindow] = MainWindow(self)
        self.change_page(MainWindow)

    def change_page(self, new_page):
        """
        Change the currently displayed page.

        Arguments:
            newFrame -- The frame to change to
        """
        # Remove anything currently placed on the screen
        for page in self.grid_slaves():
            if page.grid_info()["column"] == 0:
                page.grid_forget()
        # Place our new page onto the screen
        self.pages[new_page].grid(row=0, column=0)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
