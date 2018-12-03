import sys,PyQt5
from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
    
        self.initUI()
    
    def initUI(self):      
    
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Draw Bezier')
        self.show()
    
    def paintEvent(self, event):
    
    
        startPoint = QtCore.QPointF(0, 0)
        controlPoint1 = QtCore.QPointF(100, 50)
        controlPoint2 = QtCore.QPointF(200, 100)
        endPoint = QtCore.QPointF(300, 300) 
    
        cubicPath = QtGui.QPainterPath(startPoint)
        cubicPath.cubicTo(controlPoint1, controlPoint2, endPoint)
    
    
        painter = QtGui.QPainter(self)
        painter.begin(self)
        painter.drawPath(cubicPath)
        painter.end()
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Lesson = Example()
    Lesson.show()
    try:
        sys.exit(app.exec_())
    except BaseException as e:
        print(e)
        pass