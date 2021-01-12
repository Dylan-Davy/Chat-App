import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from Client.GUI.Main import MainWindow
from Client.GUI.Main import ChatMessage
from Client.GUI.Main import ChatItem
from Client.ClientSocket import ClientSocket
from datetime import datetime

class Client(qtc.QObject):
    login_signal = qtc.pyqtSignal(str, str, int)
    register_signal = qtc.pyqtSignal(str, str, int)
    logout_signal = qtc.pyqtSignal()
    add_contact = qtc.pyqtSignal(str)
    send_message = qtc.pyqtSignal(str, str, str, str)

    def __init__(self):
        super().__init__()
        
        self.socket_thread = qtc.QThread()
        self.socket = ClientSocket()
        self.socket.moveToThread(self.socket_thread)
        self.socket_thread.start()
        
        self.socket.login_outcome.connect(self.loginOutcome)
        self.socket.register_outcome.connect(self.registerOutcome)
        self.socket.add_contact_outcome.connect(self.addContactOutcome)
        self.socket.recieved_message.connect(self.recieveMessage)
        self.socket.server_connection_failed.connect(self.connectionFailed)

        self.send_message.connect(self.socket.sendMessage)
        self.login_signal.connect(self.socket.login)
        self.register_signal.connect(self.socket.login)
        self.logout_signal.connect(self.socket.disconnect)
        self.add_contact.connect(self.socket.addContact)
        
        w.ui.LoginButton.clicked.connect(self.login)
        w.ui.RegisterButton.clicked.connect(self.register)
        w.ui.newMessageButton.clicked.connect(self.addContact)
        w.ui.actionBack.triggered.connect(self.backButton)
        w.ui.sendButton.clicked.connect(self.sendMessage)
        w.ui.ChatScroll.verticalScrollBar().rangeChanged.connect(lambda : w.ui.ChatScroll.verticalScrollBar().setValue(w.ui.ChatScroll.verticalScrollBar().maximum()))

    def backButton(self):
        if w.ui.stackedWidget.currentIndex() == 0:
            w.close()
        elif w.ui.stackedWidget.currentIndex() == 1:
            self.logout()
        elif w.ui.stackedWidget.currentIndex() == 2:
            w.home([])

    def loginOutcome(self, login_outcome, list):
        if login_outcome == "Logged in":
            self.username = w.ui.UsernameEntry.text()
        
        w.loginOutcome(login_outcome, list)

    def sendMessage(self):
        if not w.ui.textEdit.toPlainText() == "":
            message = w.ui.textEdit.toPlainText()
            time = str(datetime.now())
            self.send_message.emit(self.username, w.message_partner, message, time)
            
            w.sendMessage(message, time)

    def recieveMessage(self, list):
        w.recieveMessage(list)

    def registerOutcome(self, register_outcome):
        w.statusBar().showMessage(register_outcome)

    def addContact(self):
        if not self.username == w.ui.newMessageText.text():
            self.add_contact.emit(w.ui.newMessageText.text())

    def addContactOutcome(self, add_contact_success):
        if add_contact_success:
            w.statusBar().showMessage(self.username + ": " + w.ui.newMessageText.text() + " added as a new contact")
            w.chat(w.ui.newMessageText.text())
        else:
            w.statusBar().showMessage(self.username + ": " + "This contact does not exist")

    def login(self):
        self.login_signal.emit(w.ui.UsernameEntry.text(), w.ui.PasswordEntry.text(), 0)
        w.login()

    def register(self):
        self.register_signal.emit(w.ui.UsernameEntry.text(), w.ui.PasswordEntry.text(), 1)
        self.statusBar().showMessage(f"Attempting to register as {self.ui.UsernameEntry.text()}")

    def logout(self):
        self.logout_signal.emit()
        self.username = ""
        w.logout()
        w.statusBar().showMessage("Logged out")
    
    def connectionFailed(self, message):
        w.connectionFailed(message)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()

    client = Client()
    w.show()

    sys.exit(app.exec_())
