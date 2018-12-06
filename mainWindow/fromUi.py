# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow/Lesson.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1346, 608)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(0, 10, 619, 33))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.pushButton_9 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_3.addWidget(self.pushButton_9)
        self.pushButton_10 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_3.addWidget(self.pushButton_10)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.pushButton_11 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout_3.addWidget(self.pushButton_11)
        self.pushButton_13 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_13.setObjectName("pushButton_13")
        self.horizontalLayout_3.addWidget(self.pushButton_13)
        self.pushButton_12 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_12.setObjectName("pushButton_12")
        self.horizontalLayout_3.addWidget(self.pushButton_12)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "zoom to layer"))
        self.pushButton_9.setText(_translate("Form", "向前"))
        self.pushButton_10.setText(_translate("Form", "向后"))
        self.pushButton_2.setText(_translate("Form", "open shp"))
        self.pushButton_11.setText(_translate("Form", "open db"))
        self.pushButton_13.setText(_translate("Form", "dbScan"))
        self.pushButton_12.setText(_translate("Form", "k-mean"))

