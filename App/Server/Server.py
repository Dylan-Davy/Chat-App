import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtNetwork as qtn
from Server.ServerThread import ServerThread

class ServerSocket(qtn.QTcpServer):
    port = 7777
    threads = []
    send_message = qtc.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.listen(qtn.QHostAddress.Any, self.port)
    
    def incomingConnection(self, descriptor):
        server_thread = ServerThread(descriptor)
        server_thread.moveToThread(server_thread)
        self.threads.append(server_thread)
        server_thread.start()

        self.send_message.connect(server_thread.sendMessage)

        server_thread.client_disconnected.connect(self.clientDisconnected)
        server_thread.message_recieved.connect(self.sendMessage)

    def sendMessage(self, list):
        for item in self.threads:
            if item.username == list[1]:
                self.send_message.emit(list)

    def clientDisconnected(self, client):
        for list in self.threads:
            if list == client:
                self.threads.remove(list)

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    server = ServerSocket()

    sys.exit(app.exec_())