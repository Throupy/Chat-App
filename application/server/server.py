"""Server class for chat app."""

import json
import socket
import select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alch import Message, Base


class Server:
    """Server object."""

    HOST = '167.99.194.4'
    PORT = 9000
    HEADERLENGTH = 10
    engine = create_engine("sqlite:///chat_app.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
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

    def getOldMsgs(self):
        """Fetch and seralize messages from DB."""
        messages = self.session.query(Message).order_by(Message.id.desc()).limit(8)
        # Reverse list
        messages = messages[::-1]
        serializedMessages = []
        for msg in messages:
            serializedMessages.append(Message.row2dict(msg))
        data = json.dumps(serializedMessages)
        return data

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
                    data = self.getOldMsgs()
                    clientSock.send(data.encode())
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
                    message = Message(content=msg["data"].decode("utf-8"),
                                      author=user["data"].decode("utf-8"))
                    self.session.add(message)
                    self.session.commit()
                    print("Added message into database")
                    for clientSocket in self.connectedUsers:
                        if clientSocket != notifiedSock:
                            print("Sending to {}".format(
                                                user["data"].decode('utf-8')))
                            clientSocket.send(user['header'] + user['data']
                                              + msg['header'] + msg['data'])
            for notifiedSock in exceptionSocks:
                self.sockets.remove(notifiedSock)
                del self.connectedUsers[notifiedSock]


server = Server()
server.main()
