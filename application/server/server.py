"""Server class for chat app."""

import socket
import select


class Server:
    """Server object."""

    HOST = '127.0.0.1'
    PORT = 9000
    HEADERLENGTH = 10

    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSock.bind((HOST, PORT))
    serverSock.settimeout(3)
    serverSock.listen()
    sockets = [serverSock]
    connectedUsers = {}

    print('Listening for connections on {}:{}...'.format(HOST, PORT))

    def getMsg(self, sock):
        """Recieve a message."""
        try:
            msgHead = sock.recv(self.HEADERLENGTH)
            if not len(msgHead):
                return False
            msgLen = int(msgHead.decode('utf-8').strip())
            return {"header": msgHead, "data": sock.recv(msgLen)}
        except Exception:
            return False

    def main(self):
        """Activate main function."""
        while True:
            readSocks, x, exceptionSocks = select.select(self.sockets, [],
                                                         self.sockets)
            for notifiedSock in readSocks:
                if notifiedSock == self.serverSock:
                    clientSock, clientAddr = self.serverSock.accept()
                    user = self.getMsg(clientSock)
                    if user is False:
                        continue
                    self.sockets.append(clientSock)
                    self.connectedUsers[clientSock] = user
                    print("New connection from {}:{} username: {}".format(
                        *clientAddr, user['data'].decode('utf-8')
                    ))
                # Sending a msg
                else:
                    msg = self.getMsg(notifiedSock)
                    if msg is False:
                        print('Closed connection from: {}'.format(
                            self.connectedUsers[notifiedSock]['data']
                                .decode('utf-8')
                        ))
                        self.sockets.remove(notifiedSock)
                        del self.connectedUsers[notifiedSock]
                        continue
                    user = self.connectedUsers[notifiedSock]
                    print("Got message from {}: {}".format(
                        user["data"].decode('utf-8'), msg["data"]
                        .decode("utf-8")
                    ))
                    # Send to all users
                    for clientSocket in self.connectedUsers:
                        print(clientSocket)
                        if clientSocket != notifiedSock:
                            print("Sending to {}".format(user["data"].decode('utf-8')))
                            clientSocket.send(user['header'] + user['data']
                                              + msg['header'] + msg['data'])
            for notifiedSock in exceptionSocks:
                self.sockets.remove(notifiedSock)
                del self.connectedUsers[notifiedSock]


server = Server()
server.main()
