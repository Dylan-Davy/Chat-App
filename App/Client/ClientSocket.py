import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtNetwork as qtn

class ClientSocket(qtc.QObject):
    port = 7777
    server_ip = "localhost"
    established = False
    processing = False
    image = qtc.QByteArray()
    login_outcome = qtc.pyqtSignal(str, list)
    register_outcome = qtc.pyqtSignal(str)
    add_contact_outcome = qtc.pyqtSignal(bool)
    recieved_message = qtc.pyqtSignal(list)
    server_connection_failed = qtc.pyqtSignal(str)

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

        if not self.socket.waitForConnected(5000):
            self.server_connection_failed.emit("Server connection timed out. Please check your internet and the server status.")

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
    
    def sendImage(self, sender, reciever, image, time):
        image_array = qtc.QByteArray()
        buffer = qtc.QBuffer(image_array)
        buffer.open(qtc.QIODevice.WriteOnly)
        image.save(buffer, "JPG", quality=100)

        request = qtc.QByteArray()
        stream = qtc.QDataStream(request, qtc.QIODevice.WriteOnly)
        stream.writeInt(4)
        stream.writeInt(image_array.size())
        stream.writeQString(sender)
        stream.writeQString(reciever)
        stream.writeQString(time)

        self.socket.write(request)
        self.socket.flush()
        self.socket.write(image_array)
        self.socket.flush()

    def processDatastream(self):
        case = -1
        stream = -1

        if not self.processing:
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

        elif case == 4:
            self.image_size = stream.readInt()
            self.image_sender = stream.readQString()
            self.image_reciever = stream.readQString()
            self.image_time = stream.readQString()
            self.processing = True

        else:
            self.image.append(self.socket.readAll())
            
            if self.image.size() == self.image_size:
                image = qtg.QImage()
                image.loadFromData(self.image)
                self.recieved_message.emit([self.image_sender, self.image_reciever, image, self.image_time])
                self.image_sender = ""
                self.image_reciever = ""
                self.image_time = ""
                self.image_size = 0
                self.image = qtc.QByteArray()
                self.processing = False

    def disconnect(self):
        self.socket.disconnectFromHost()
        self.established = False
