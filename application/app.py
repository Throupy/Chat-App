"""Client app for the chat app."""
import socket
import tkinter as tk
from tkinter.simpledialog import askstring


class MainWindow(tk.Frame):
    """Main window class."""

    def __init__(self, parent):
        """Initialize class."""
        super().__init__()
        self.parent = parent
        if parent.USERNAME is None:
            self.popup()
        else:
            self.create_widgets()

    def create_widgets(self):
        """Create widgets."""
        self.parent.geometry("400x600")
        msgFrame = tk.Frame(self)
        myMsg = tk.StringVar()
        myMsg.set("Type your messages here")
        scrollbar = tk.Scrollbar(msgFrame)
        msg_list = tk.Listbox(msgFrame,
                              height=15,
                              width=60,
                              yscrollcommand=scrollbar.set)
        scrollbar.grid(sticky=tk.E)
        msg_list.grid(sticky=tk.W)
        msg_list.grid()
        msgFrame.grid()

        entry_field = tk.Entry(self, textvariable=myMsg, width=50)
        entry_field.bind("<Return>", self.quit())
        entry_field.grid()
        send_button = tk.Button(self, text="Send")
        send_button.grid()

    def popup(self):
        """Popup and ask for the user's name."""
        name = askstring('Name', 'What is your name?')
        self.parent.USERNAME = name
        self.create_widgets()


class Application(tk.Tk):
    """Application class inheriting from tk.Tk."""

    HOST, PORT = "167.99.194.4", 9000
    USERNAME = None
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((HOST, PORT))
    socket.setblocking(False)

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
