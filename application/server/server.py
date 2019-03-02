"""Server for the chat application."""

import socket
import threading
import pickle


class Server:
    """Server class."""

    CURRENTLY_CONNECTED_USERS = []

    def __init__(self):
        """Initialise the class."""
        self.HOST = '167.99.194.4'
        self.PORT = 9000
        self.setup()

    def setup(self):
        """Set up the server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen(3)
            self.awaitConn(s)

    def clientThread(self, conn):
        """Thread for the client."""
        while True:
            data = conn.recv(2048)
            print("got ", data)
            if not data:
                break
            for conn in self.CURRENTLY_CONNECTED_USERS:
                conn.sendall(data)

    def awaitConn(self, s):
        """Await connections."""
        while True:
            conn, addr = s.accept()
            self.CURRENTLY_CONNECTED_USERS.append(conn)
            print("Connection from", addr)
            conn.sendall(b"200")
            try:
                threading.Thread(target=self.clientThread,
                                 args=(conn,)).start()
            except Exception:
                print("[!]Thread could not start!")

        s.close()


server = Server()
