from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from Client.GUI.MainWindow import Ui_MainWindow
from Client.GUI.Chat import Ui_Chat
from Client.GUI.Message import Ui_message
from Client.Assets.Style import qss

class MainWindow(qtw.QMainWindow):
    message_list = []
    partner_list = {}
    message_partner = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        style_file = qss
        self.ui.centralwidget.setStyleSheet(style_file)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.statusBar().showMessage("Logged out")

    def login(self):
        self.statusBar().showMessage(f"Attempting to login as {self.ui.UsernameEntry.text()}...")
        self.ui.LoginButton.setEnabled(False)
        self.ui.RegisterButton.setEnabled(False)

    def loginOutcome(self, login_outcome, list):
        if login_outcome == "Logged in":
            self.username = self.ui.UsernameEntry.text()
            self.statusBar().showMessage(self.username + ": " + login_outcome)
            self.home(list)
        else:
            self.statusBar().showMessage(login_outcome)
        
        self.ui.LoginButton.setEnabled(True)
        self.ui.RegisterButton.setEnabled(True)

    def connectionFailed(self, message):
        self.statusBar().showMessage(message)
        self.ui.LoginButton.setEnabled(True)
        self.ui.RegisterButton.setEnabled(True)

    def sendMessage(self, message, time):
        self.ui.ChatScrollVbox.addWidget(ChatMessage(True, message, time))
        self.partner_list[self.message_partner] = message
        self.ui.textEdit.setText("")

        self.message_list.append([self.username, self.message_partner, message, time])

        self.ui.ChatScroll.verticalScrollBar().setValue(self.ui.ChatScroll.verticalScrollBar().maximum())

    def recieveMessage(self, list):
        self.message_list.append([list[0], list[1], list[2], list[3]])

        if list[0] == self.message_partner or list[1] == self.message_partner:
            self.ui.ChatScrollVbox.addWidget(ChatMessage(False, list[2], list[3]))
            self.ui.ChatScroll.verticalScrollBar().setValue(self.ui.ChatScroll.verticalScrollBar().maximum())
        else:
            new_chat_bool = True

            if self.ui.stackedWidget.currentIndex() == 1:
                for widget in reversed(range(self.ui.HomeScrollVbox.count())): 
                    chat = self.ui.HomeScrollVbox.itemAt(widget).widget()

                    if chat.ui.Name.text() == list[0]:
                        chat.ui.LastMessage.setText(list[2])
                        new_chat_bool = False
            
                if new_chat_bool:
                    widget = ChatItem([list[0], list[2]])
                    widget.clicked_signal.connect(self.chat)
                    self.ui.HomeScrollVbox.addWidget(widget)

        self.partner_list[list[0]] = list[2]

    def home(self, list):
        if not len(list) == 0:
            for item in list:
                x = item.split(":;:")
                self.message_list.append(x)

                if not self.username == x[0]:
                    self.partner_list[x[0]] = x[2]
                else:
                    self.partner_list[x[1]] = x[2]

        if self.ui.stackedWidget.currentIndex() == 2:
            for widget in reversed(range(self.ui.ChatScrollVbox.count())): 
                self.ui.ChatScrollVbox.itemAt(widget).widget().setParent(None)

            self.ui.ChatScrollVbox.deleteLater()

        self.ui.HomeScrollVbox = qtw.QVBoxLayout()
        self.ui.HomeScrollVbox.setAlignment(qtc.Qt.AlignTop)
        self.ui.HomeScrollWidget.setLayout(self.ui.HomeScrollVbox)

        if len(self.partner_list) > 0:
            for item in self.partner_list.items():
                chat = ChatItem(item)
                self.ui.HomeScrollVbox.addWidget(chat)
                chat.clicked_signal.connect(self.chat)

        self.ui.HomeScrollArea.setWidget(self.ui.HomeScrollWidget)

        self.message_partner = ""
        
        self.ui.stackedWidget.setCurrentIndex(1)

    def logout(self):
        self.ui.stackedWidget.setCurrentIndex(0)

        self.username = ""

        for widget in reversed(range(self.ui.HomeScrollVbox.count())): 
            self.ui.HomeScrollVbox.itemAt(widget).widget().setParent(None)

        self.ui.UsernameEntry.setText("")
        self.ui.PasswordEntry.setText("")

        self.message_list = []
        self.partner_list = {}
        
        self.ui.HomeScrollVbox.deleteLater()

    def chat(self, id):        
        self.ui.newMessageText.setText("")

        self.message_partner = id

        self.ui.MessagePartnerLabel.setText(self.message_partner)

        self.ui.ChatScrollVbox = qtw.QVBoxLayout()
        self.ui.scrollAreaWidgetContents_3.setLayout(self.ui.ChatScrollVbox)

        for message in self.message_list:
            if message[0] == self.message_partner or message[1] == self.message_partner:
                own_message = False
                
                if message[0] == self.username:
                    own_message = True

                self.ui.ChatScrollVbox.addWidget(ChatMessage(own_message, message[2], message[3]))

        for widget in reversed(range(self.ui.HomeScrollVbox.count())): 
            self.ui.HomeScrollVbox.itemAt(widget).widget().setParent(None)

        self.ui.HomeScrollVbox.deleteLater()

        self.ui.ChatScroll.verticalScrollBar().setValue(self.ui.ChatScroll.verticalScrollBar().maximum())
        
        self.ui.stackedWidget.setCurrentIndex(2)

class ChatItem(qtw.QWidget):
    clicked_signal = qtc.pyqtSignal(str)

    def __init__(self, list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Chat()
        self.ui.setupUi(self)
        self.ui.Name.setText(list[0])
        self.ui.LastMessage.setText(list[1])
    
    def mouseReleaseEvent(self, event: qtg.QMouseEvent):
        self.clicked_signal.emit(self.ui.Name.text())
        super().mouseReleaseEvent(event)

class ChatMessage(qtw.QWidget):
    def __init__(self, sender, message, time, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_message()
        self.ui.setupUi(self)

        if not sender:
            self.ui.messageLabel.setStyleSheet("background-color:purple;")

        self.ui.messageLabel.setText(message)
        self.ui.time.setText(time)