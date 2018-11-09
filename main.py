# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from main_window import *

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Lesson = Lesson()
    Lesson.show()
    try:
        sys.exit(app.exec_())
    except BaseException as e:
        print(e)
        pass