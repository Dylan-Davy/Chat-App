# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Image.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_message(object):
    def setupUi(self, message):
        message.setObjectName("message")
        message.resize(200, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(message.sizePolicy().hasHeightForWidth())
        message.setSizePolicy(sizePolicy)
        message.setMaximumSize(QtCore.QSize(16777215, 150))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(message)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(message)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 180, 109))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ImageLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ImageLabel.setObjectName("ImageLabel")
        self.verticalLayout.addWidget(self.ImageLabel)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.time = QtWidgets.QLabel(message)
        self.time.setMaximumSize(QtCore.QSize(16777215, 15))
        self.time.setObjectName("time")
        self.verticalLayout_2.addWidget(self.time)

        self.retranslateUi(message)
        QtCore.QMetaObject.connectSlotsByName(message)

    def retranslateUi(self, message):
        _translate = QtCore.QCoreApplication.translate
        message.setWindowTitle(_translate("message", "Form"))
        self.ImageLabel.setText(_translate("message", "TextLabel"))
        self.time.setText(_translate("message", "TextLabel"))
