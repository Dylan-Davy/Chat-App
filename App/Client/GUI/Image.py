# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Image.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_imageMessage(object):
    def setupUi(self, imageMessage):
        imageMessage.setObjectName("imageMessage")
        imageMessage.resize(200, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(imageMessage.sizePolicy().hasHeightForWidth())
        imageMessage.setSizePolicy(sizePolicy)
        imageMessage.setMaximumSize(QtCore.QSize(16777215, 150))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(imageMessage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(imageMessage)
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
        self.time = QtWidgets.QLabel(imageMessage)
        self.time.setMaximumSize(QtCore.QSize(16777215, 15))
        self.time.setObjectName("time")
        self.verticalLayout_2.addWidget(self.time)

        self.retranslateUi(imageMessage)
        QtCore.QMetaObject.connectSlotsByName(imageMessage)

    def retranslateUi(self, imageMessage):
        _translate = QtCore.QCoreApplication.translate
        imageMessage.setWindowTitle(_translate("imageMessage", "Form"))
        self.ImageLabel.setText(_translate("imageMessage", "TextLabel"))
        self.time.setText(_translate("imageMessage", "TextLabel"))
