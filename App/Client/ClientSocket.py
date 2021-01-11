import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtNetwork as qtn

class ClientSocket(qtc.QObject):
    port = 7777
    server_ip = "localhost"
    established = False
    login_outcome = qtc.pyqtSignal(str, list)
    register_outcome = qtc.pyqtSignal(str)
    add_contact_outcome = qtc.pyqtSignal(bool)
    recieved_message = qtc.pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def login(self, username, password, case):
        self.case = case

        self.username = username
        self.password = password

        if self.established == True:
            if self.socket.state() == qtn.QAbstractSocket.UnconnectedState:
                self.socket = qtn.QTcpSocket()
                self.socket.connectToHost(self.server_ip, self.port)
            else:
                self.sendLoginDetails()
        else:
            self.socket = qtn.QTcpSocket()
            self.established = True
            self.socket.connectToHost(self.server_ip, self.port)

            self.socket.readyRead.connect(self.processDatastream)
            self.socket.connected.connect(self.sendLoginDetails)

    def sendLoginDetails(self):
        request = qtc.QByteArray()
        stream = qtc.QDataStream(request, qtc.QIODevice.WriteOnly)
        stream.writeInt(self.case)
        stream.writeQString(self.username)
        stream.writeQString(self.password)
        self.socket.write(request)
        self.socket.flush()

    def sendMessage(self, sender, reciever, message, time):
        request = qtc.QByteArray()
        stream = qtc.QDataStream(request, qtc.QIODevice.WriteOnly)
        stream.writeInt(2)
        stream.writeQString(sender)
        stream.writeQString(reciever)
        stream.writeQString(message)
        stream.writeQString(time)
        self.socket.write(request)
        self.socket.flush()

    def addContact(self, new_contact):
        request = qtc.QByteArray()
        stream = qtc.QDataStream(request, qtc.QIODevice.WriteOnly)
        stream.writeInt(3)
        stream.writeQString(new_contact)
        self.socket.write(request)
        self.socket.flush()

    def processDatastream(self):
        stream = qtc.QDataStream(self.socket)
        case = stream.readInt()

        if case == 0:
            login_outcome = stream.readQString()
            list = []

            if login_outcome == "Logged in":
                list = stream.readQStringList()

            self.login_outcome.emit(login_outcome, list)

        elif case == 1:
            register_outcome = stream.readQString()
            self.register_outcome.emit(register_outcome)

        elif case == 2:
            add_contact_success = stream.readBool()
            self.add_contact_outcome.emit(add_contact_success)

        elif case == 3:
            list = stream.readQStringList()
            self.recieved_message.emit(list)

    def disconnect(self):
        self.socket.disconnectFromHost()
        self.established = False
