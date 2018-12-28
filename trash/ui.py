# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/benfen/untitled1/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(200,40 )
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0,200, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuBuffer = QtWidgets.QMenu(self.menuBar)
        self.menuBuffer.setObjectName("menuBuffer")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionstart_edit = QtWidgets.QAction(MainWindow)
        self.actionstart_edit.setObjectName("actionstart_edit")
        self.actionend_edit = QtWidgets.QAction(MainWindow)
        self.actionend_edit.setObjectName("actionend_edit")
        self.actionbuffer = QtWidgets.QAction(MainWindow)
        self.actionbuffer.setObjectName("actionbuffer")
        self.actionopen_shp = QtWidgets.QAction(MainWindow)
        self.actionopen_shp.setObjectName("actionopen_shp")

        self.menuBuffer.addAction(self.actionstart_edit)
        self.menuBuffer.addAction(self.actionend_edit)
        self.menuBuffer.addAction(self.actionbuffer)
        self.menuFile.addAction(self.actionopen_shp)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuBuffer.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuBuffer.setTitle(_translate("MainWindow", "Buffer"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionstart_edit.setText(_translate("MainWindow", "start edit"))
        self.actionend_edit.setText(_translate("MainWindow", "end edit"))
        self.actionbuffer.setText(_translate("MainWindow", "buffer"))
        self.actionopen_shp.setText(_translate("MainWindow", "open shp"))

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1346, 608)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Form)
        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))