"""Chat page for the chat application."""

import tkinter as tk
import threading
import time


class ChatPage(tk.Frame):
    """Example page for Application."""

    def __init__(self, parent):
        """Initialise the Example page."""
        # So i can display the messages line by line
        super().__init__()
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.parent = parent
        self.create_widgets()

    def awaitMsg(self):
        """Wait for messages to be returned from the chat server."""
        while True:
            message = self.parent.socket.recv(1024)
            if message != '':
                print("got msg")
                self.handleMessage(message)
            time.sleep(0.05)

    def handleMessage(self, message):
        """Handle the message after it has been received.

        Arguments:
            message - the message to be handled
        """
        self.msg_list.insert(tk.END, message)

    def create_widgets(self):
        """Create the pages widgets."""
        self.title = tk.Label(self,
                              text="Welcome to blipper"
                              )
        self.title.grid(row=0,
                        column=0
                        )

        self.messages_frame = tk.Frame(self)
        self.scrollbar = tk.Scrollbar(self.messages_frame)
        # Following will contain the messages.
        self.msg_list = tk.Listbox(self.messages_frame,
                                   height=15,
                                   width=50,
                                   yscrollcommand=self.scrollbar.set)
        self.msg_list.grid()
        self.messages_frame.grid()
        # Message entry
        tk.Label(self, text="Send a message:").grid()
        self.messageEntry = tk.Entry(self, width=20)
        self.messageEntry.grid()
        self.sendBtn = tk.Button(self, text="Send", command=lambda:
                                 self.sendMessage(self.messageEntry.get()))
        self.sendBtn.grid()
        thread = threading.Thread(target=self.awaitMsg, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()

    def sendMessage(self, message):
        """Send a message to other users.

        Arguments:
            message - the message to be sent
        """
        self.parent.socket.sendall(message.encode("utf8"))
