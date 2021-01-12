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
            w.statusBar().showMessage(self.username + ": " + login_outcome)
            w.username = w.ui.UsernameEntry.text()
            w.home(list)
        else:
            w.statusBar().showMessage(login_outcome)

    def sendMessage(self):
        if not w.ui.textEdit.toPlainText() == "":
            message = w.ui.textEdit.toPlainText()
            w.ui.ChatScrollVbox.addWidget(ChatMessage(True, message, str(datetime.now())))
            self.send_message.emit(self.username, w.message_partner, message, str(datetime.now()))
            w.partner_list[w.message_partner] = message
            w.ui.textEdit.setText("")

            w.message_list.append([self.username, w.message_partner, message, str(datetime.now())])

            w.ui.ChatScroll.verticalScrollBar().setValue(w.ui.ChatScroll.verticalScrollBar().maximum())

    def recieveMessage(self, list):
        w.message_list.append([list[0], list[1], list[2], list[3]])

        if list[0] == w.message_partner or list[1] == w.message_partner:
            w.ui.ChatScrollVbox.addWidget(ChatMessage(False, list[2], list[3]))
            w.ui.ChatScroll.verticalScrollBar().setValue(w.ui.ChatScroll.verticalScrollBar().maximum())
        else:
            new_chat_bool = True

            if w.ui.stackedWidget.currentIndex() == 1:
                for widget in reversed(range(w.ui.HomeScrollVbox.count())): 
                    chat = w.ui.HomeScrollVbox.itemAt(widget).widget()

                    if chat.ui.Name.text() == list[0]:
                        chat.ui.LastMessage.setText(list[2])
                        new_chat_bool = False
            
                if new_chat_bool:
                    widget = ChatItem([list[0], list[2]])
                    widget.clicked_signal.connect(w.chat)
                    w.ui.HomeScrollVbox.addWidget(widget)

        w.partner_list[list[0]] = list[2]

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

    def register(self):
        self.register_signal.emit(w.ui.UsernameEntry.text(), w.ui.PasswordEntry.text(), 1)

    def logout(self):
        self.logout_signal.emit()
        self.username = ""
        w.logout()
        w.statusBar().showMessage("Logged out")

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()

    client = Client()
    w.show()

    sys.exit(app.exec_())
