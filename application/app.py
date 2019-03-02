"""Client for the chat application."""
import socket
import tkinter as tk
from pages.chatpage import ChatPage
from pages.namepage import NamePage


class Application(tk.Tk):
    """Application class inheriting from tk.Tk."""

    HOST, PORT = "167.99.194.4", 9000
    USERNAME = None

    def __init__(self):
        """Initialise the Application class."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        super().__init__()
        if self.establishConnection():
            self.create_pages()
        else:
            return

    def establishConnection(self):
        """Establish a connection with the chat server."""
        response = self.socket.recv(1024)
        # 200 = OK
        if response.decode() == "200":
            print("Connection established")
            return True
        return False

    def create_pages(self):
        """Create the pages used inside the application."""
        self.pages = {}

        self.pages[ChatPage] = ChatPage(self)
        self.pages[NamePage] = NamePage(self)

        self.change_page(NamePage)

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
