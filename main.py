# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from mainWindow import *
from mainWindow.main_window import *
from newBasicClass import *

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Lesson = MainWindow()
    Lesson.show()
    try:
        sys.exit(app.exec_())
    except BaseException as e:
        print(e)
        pass