"""Client app for the chat app."""
import socket
import tkinter as tk


class AskForUsername(tk.Frame):
    """Asks for username."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.top = tk.Toplevel(parent)
        userNameLabel = tk.Label(self.top, text="Enter your username")
        userNameLabel.pack()
        self.userNameEntry = tk.Entry(self.top)
        self.userNameEntry.pack()
        submit = tk.Button(self.top, text="Submit", command=lambda:
            self.cleanup())
        submit.pack()

    def cleanup(self):
        value = self.userNameEntry.get()
        self.parent.USERNAME = value
        self.top.destroy()
        self.parent.change_page(MainWindow)


class MainWindow(tk.Frame):
    """Main window class."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.create_widgets()
        if parent.USERNAME is None:
            self.popup()

    def create_widgets(self):
        l = tk.Label(self, text="Main Window")
        l.grid()

    def popup(self):
        self.window = AskForUsername(self.parent)
        self.parent.wait_window(self.window.top)

    def entryValue(self):
        return self.window.value



class Application(tk.Tk):
    """Application class inheriting from tk.Tk."""

    HOST, PORT = "167.99.194.4", 9000
    USERNAME = None
    # socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket.connect((HOST, PORT))
    # socket.setblocking(False)

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
