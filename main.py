# coding : utf-8

from Lesson2_Widget import *
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Lesson2_Widget()
    sys.exit(app.exec_())