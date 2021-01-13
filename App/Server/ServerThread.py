import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtNetwork as qtn
from PyQt5 import QtSql as qts
import psycopg2

class ServerThread(qtc.QThread):
    client_disconnected = qtc.pyqtSignal(qtc.QObject)
    message_recieved = qtc.pyqtSignal(list)
    processing = False
    image = qtc.QByteArray()

    def __init__(self, descriptor):
        super().__init__()
        self.descriptor = descriptor

    def run(self):
        self.connection = qtn.QTcpSocket()
        self.connection.setSocketDescriptor(self.descriptor)

        self.connection.readyRead.connect(self.processDatastream)
        self.connection.disconnected.connect(self.disconnect)

        self.database = psycopg2.connect(
            host = "localhost",
            database = "Chat",
            user = "postgres",
            password = "9653",
            port = "5432"
        )

        self.cur = self.database.cursor()

        self.exec()

    def processDatastream(self):
        case = -1
        stream = -1

        if not self.processing:
            stream = qtc.QDataStream(self.connection)
            case = stream.readInt()
        
        if case == 0:
            username = stream.readQString()
            password = stream.readQString()

            self.cur.execute(f"SELECT COUNT(username) FROM \"Users\" WHERE username = '{username}' AND password = '{password}'")

            count = self.cur.fetchone()[0]

            request = qtc.QByteArray()
            stream = qtc.QDataStream(request, qtc.QIODevice.WriteOnly)
            stream.writeInt(0)

            if count == 1:
                stream.writeQString("Logged in")

                self.username = username

                self.cur.execute(f"SELECT * FROM \"Messages\" WHERE reciever = '{username}' OR sender = '{username}'")

                list = []

                for record in self.cur:
                    list.append(record[0] + ":;:" + record[1] + ":;:" + record[2] + ":;:" + record[3])

                stream.writeQStringList(list)
            else:
                stream.writeQString("Login failed")

            self.connection.write(request)

        elif case == 1:
            username = stream.readQString()
            password = stream.readQString()
            
            self.cur.execute(f"SELECT COUNT(username) FROM \"Users\" WHERE username = '{username}'")

            count = self.cur.fetchone()[0]

            request = qtc.QByteArray()
            stream = qtc.QDataStream(request, qtc.QIODevice.WriteOnly)
            stream.writeInt(1)

            if count == 0 and len(username) > 0 and len(password) > 0:
                self.cur.execute(f"INSERT INTO \"Users\" VALUES ('{username}', '{password}')")
                stream.writeQString("Registered successfully")
            elif count != 0:
                stream.writeQString("User already exists")
            else:
                stream.writeQString("Registration failed")

            self.connection.write(request)

        elif case == 2:
            sender = stream.readQString()
            reciever = stream.readQString()
            message = stream.readQString()
            time = stream.readQString()

            self.cur.execute(f"INSERT INTO \"Messages\" VALUES ('{sender}', '{reciever}', '{message}', '{time}')")

            self.message_recieved.emit([sender, reciever, message, time])

        elif case == 3:
            new_contact = stream.readQString()

            self.cur.execute(f"SELECT COUNT(username) FROM \"Users\" WHERE username = '{new_contact}'")

            count = self.cur.fetchone()[0]

            request = qtc.QByteArray()
            stream = qtc.QDataStream(request, qtc.QIODevice.WriteOnly)
            stream.writeInt(2)
            
            if count == 1:
                stream.writeBool(True)
            else:
                stream.writeBool(False)
            
            self.connection.write(request)

        elif case == 4:
            self.image_size = stream.readInt()
            self.image_sender = stream.readQString()
            self.image_reciever = stream.readQString()
            self.image_time = stream.readQString()
            self.processing = True

        else:
            self.image.append(self.connection.readAll())
            
            if self.image.size() == self.image_size:
                my_image = qtg.QImage()

                self.image_sender = ""
                self.image_reciever = ""
                self.image_time = ""
                self.processing = False

        self.database.commit()
        self.connection.flush()

    def sendMessage(self, list):
        if self.username == list[1]:
            request = qtc.QByteArray()
            stream = qtc.QDataStream(request, qtc.QIODevice.WriteOnly)
            stream.writeInt(3)
            stream.writeQStringList(list)

            self.connection.write(request)
            self.connection.flush()

    def sendImage(self):
        pass

    def disconnect(self):
        self.username = ""
        self.password = ""
        self.quit()
        self.client_disconnected.emit(self)