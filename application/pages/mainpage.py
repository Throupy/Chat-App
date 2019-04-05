"""Main page for chat app."""
import socket
import sys
import time
import threading
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
        threading.Thread(target=self.waitForMessage).start()
        if self.USERNAME is None:
            self.popup()
        else:
            self.create_widgets()

    def create_widgets(self):
        """Create widgets."""
        self.parent.geometry("400x600")
        msgFrame = tk.Frame(self)
        self.myMsg = tk.StringVar()
        self.myMsg.set("Type your messages here")
        scrollbar = tk.Scrollbar(msgFrame)
        self.msg_list = tk.Listbox(msgFrame,
                                   height=15,
                                   width=60,
                                   yscrollcommand=scrollbar.set)
        scrollbar.grid(sticky=tk.E)
        self.msg_list.grid(sticky=tk.W)
        self.msg_list.grid()
        msgFrame.grid()

        entry_field = tk.Entry(self, textvariable=self.myMsg, width=50)
        entry_field.bind("<Return>", self.quit())
        entry_field.grid()
        send_button = tk.Button(self,
                                text="Send",
                                command=lambda:
                                    self.sendMessage(entry_field.get()))
        send_button.grid()

    def waitForMessage(self):
        """Wait for messages."""
        cs = self.clientsocket
        while True:
            try:
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
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                pass

            except Exception as e:
                print('Reading error: '.format(str(e)))
                sys.exit()

        time.sleep(0.1)

    def sendMessage(self, message):
        """Handle the event in which the user wants to send a message."""
        if len(message) < 1:
            return
        self.msg_list.insert(tk.END, f"{self.USERNAME} > {message}")
        message = message.encode('utf-8')
        message_header = f"{len(message):<{self.HEADERLENGTH}}".encode('utf-8')
        self.clientsocket.send(message_header + message)
        self.myMsg.set("")

    def popup(self):
        """Popup and ask for the user's name."""
        name = askstring('Name', 'What is your name?')
        if len(name) < 1:
            name = "Anonymous"
        self.USERNAME = name
        name = name.encode("utf-8")
        username_header = f"{len(name):<{self.HEADERLENGTH}}".encode('utf-8')
        self.clientsocket.send(username_header + name)
        self.create_widgets()
