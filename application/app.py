"""Client app for the chat app."""
import socket
import sys
import errno
import tkinter as tk
from tkinter.simpledialog import askstring


class MainWindow(tk.Frame):
    """Main window class."""

    HOST, PORT = '167.99.194.4', 9000
    USERNAME = None
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))
    clientsocket.setblocking(0)
    HEADERLENGTH = 10

    def __init__(self, parent):
        """Initialize class."""
        super().__init__()
        self.parent = parent
        if self.USERNAME is None:
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
        self.msg_list = tk.Listbox(msgFrame,
                                   height=15,
                                   width=60,
                                   yscrollcommand=scrollbar.set)
        scrollbar.grid(sticky=tk.E)
        self.msg_list.grid(sticky=tk.W)
        self.msg_list.grid()
        msgFrame.grid()

        entry_field = tk.Entry(self, textvariable=myMsg, width=50)
        entry_field.bind("<Return>", self.quit())
        entry_field.grid()
        send_button = tk.Button(self,
                                text="Send",
                                command=lambda:
                                    self.sendMessage(entry_field.get()))
        send_button.grid()

    def sendMessage(self, message):
        """Handle the event in which the user wants to send a message."""
        self.msg_list.insert(tk.END, f"{self.USERNAME} > {message}")
        cs = self.clientsocket
        message = message.encode('utf-8')
        message_header = f"{len(message):<{self.HEADERLENGTH}}".encode('utf-8')
        cs.send(message_header + message)
        cs = self.clientsocket
        print("Wait called")
        try:
            while True:
                usernameHeader = cs.recv(self.HEADERLENGTH)
                if not len(usernameHeader):
                    print("Connection forceably closed by the remote host")
                    sys.exit()
                usernameLen = int(usernameHeader.decode("utf-8").strip())
                username = cs.recv(usernameLen).decode("utf-8")
                message_header = cs.recv(self.HEADERLENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = cs.recv(message_length).decode('utf-8')
                self.msg_list.insert(tk.END, f"{username} > {message}")

        except IOError as e:
            print(str(e))
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            pass

        except Exception as e:
            print(str(e))
            print('Reading error: '.format(str(e)))
            sys.exit()

    def popup(self):
        """Popup and ask for the user's name."""
        name = askstring('Name', 'What is your name?')
        self.USERNAME = name
        name = name.encode("utf-8")
        username_header = f"{len(name):<{self.HEADERLENGTH}}".encode('utf-8')
        self.clientsocket.send(username_header + name)
        self.create_widgets()


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
