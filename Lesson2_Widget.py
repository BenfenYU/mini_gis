# -*- coding: utf-8 -*-

import sys,random
import PyQt5.QtWidgets as QtWidgets
from BasicClasses import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *

# 存储加入的空间和属性特征
# points_feature = []
# lines_feature = []
features = []
view = None

class Lesson2_Widget(QtWidgets.QWidget):

    def __init__(self):
        
        super().__init__()
        self.initUI()
        # 用来反应事件是否被触发，反射？
        self.flag = False
        self.mouse = False
        self.random_draw = False

    def initUI(self):   
        
        global view
        # 定义标签、等待输入的文本框和按钮 
        self.X_label = QtWidgets.QLabel('X',self)
        self.Y_label = QtWidgets.QLabel('Y')
        self.A_label = QtWidgets.QLabel('属性',self)
        self.X_text = QtWidgets.QLineEdit()
        self.Y_text = QtWidgets.QLineEdit()
        self.A_text = QtWidgets.QLineEdit()
        self.pushButton = QtWidgets.QPushButton('添加空间对象')
        self.pushButton.clicked.connect(self.update_byhand)
        self.labelMousePos = QtWidgets.QLabel();
        self.labelMousePos.setText(self.tr(""))
        self.label1 = QtWidgets.QLabel('minx')
        self.label2 = QtWidgets.QLabel('miny')
        self.label3 = QtWidgets.QLabel('maxx')
        self.label4 = QtWidgets.QLabel('maxy')
        #self.X_text2 = QtWidgets.QLineEdit()
        #self.Y_text2 = QtWidgets.QLineEdit()
        #self.X_text2.setVisible(False)
        #self.Y_text2.setVisible(False)
        self.btn_random = QtWidgets.QPushButton('随机添加点')
        self.update_btn = QtWidgets.QPushButton('更新地图')
        self.text1 = QtWidgets.QLineEdit()
        self.text2 = QtWidgets.QLineEdit()
        self.text3 = QtWidgets.QLineEdit()
        self.text4 = QtWidgets.QLineEdit()
        # 添加选择按钮
        #self.btn_point =  QRadioButton('点')
        #self.btn_line = QRadioButton('线')
        #self.btn_point.setChecked(True)
        #self.btn_point.clicked.connect(self.pointorline)
        #self.btn_line.clicked.connect(self.pointorline)
        self.btn_random.clicked.connect(self.update_byhand)
        self.update_btn.clicked.connect(self.update_map)
        # 布局
        grid = QtWidgets.QGridLayout()
        # 设置部件间距
        grid.setSpacing(10)
        grid.addWidget(self.X_label, 1, 0)
        grid.addWidget(self.X_text, 2, 0)
        grid.addWidget(self.Y_label, 1, 1)
        grid.addWidget(self.Y_text, 2, 1)
        grid.addWidget(self.A_label, 1, 2)
        grid.addWidget(self.A_text, 2,2)
        grid.addWidget(self.label1, 3, 0)
        grid.addWidget(self.label2, 3, 1)
        grid.addWidget(self.label3, 3, 2)
        grid.addWidget(self.label4, 3, 3)

        #grid.addWidget(self.X_text2, 3, 0)
        #grid.addWidget(self.Y_text2, 3, 1)

        #grid.addWidget(self.btn_point,3,3)
        #grid.addWidget(self.btn_line,3,4)
        grid.addWidget(self.pushButton,2,3)
        grid.addWidget(self.labelMousePos,9,0)
        # grid.addWidget(self.btn_random,1,3,2,2)
        grid.addWidget(self.update_btn,1,3)
        grid.addWidget(self.text1,4,0)
        grid.addWidget(self.text2,4,1)
        grid.addWidget(self.text3,4,2)
        grid.addWidget(self.text4,4,3)
        # 占位label
        self.position_label = QtWidgets.QLabel()
        grid.addWidget(self.position_label,5,0,5,5)
        self.setLayout(grid) 
        self.resize(800,600)
        # 打开鼠标跟踪
        self.setMouseTracking(True)
        view = GISView(GISExtent(GISVertex(0,0),GISVertex(100,100)),self.frameGeometry())

        self.show()

    #def random_paint(self,view):
    #    global points_feature
    #    qp = QPainter()
    #    for i in range(100):
    #        x = random.randint(1,100)
    #        y = random.randint(1,100)
    #        temp_vertex = GISVertex(x,y)
    #        temp_point = GISPoint(temp_vertex)
    #        features.append(temp_point)
    #        #for feature in features[0]:
    #        # 这个begin函数的参数为QWidget类的实例
    #        qp.begin(self)
    #        # 原来self也可以当参数用，本类的实例作为参数传递
    #        #onepoint.draw(qwidget_obj = self,qp = qp)
    #        features[i].draw(self, qp,view)
    #        qp.end()
            
    
    # 响应qradiobutton的点击
    #def pointorline(self):
    #    if self.btn_point.isChecked():
    #        self.X_text2.setVisible(False)
    #        self.Y_text2.setVisible(False)
    #    elif self.btn_line.isChecked():
    #        self.X_text2.setVisible(True)
    #        self.Y_text2.setVisible(True)

    # 手动设置更新     
    def update_byhand(self):
        
        self.flag = True
        self.random_draw = True
        self.update()

    # 画图事件
    def paintEvent(self,event):
        global features
        global view
        #if self.random_draw:
        #    self.random_paint(view)
        # 如果事件被触发，开始画图
        if self.flag:
            # 画点
            #if self.btn_point.isChecked():
            #self.random_paint()
            qp = QPainter()
            x = int('0'+(self.X_text.text()))
            y = int('0'+(self.Y_text.text()))
            a = self.A_text.text()
            onevertex = GISVertex(x,y)
            onepoint = GISPoint(onevertex)
            text = self.A_text.text()
            oneattribute = GISAttribute()
            oneattribute.AddValue(text)
            onefeature = GISFeature(onepoint,oneattribute)
            features.append(onefeature)
            for feature in features:
                # 这个begin函数的参数为QWidget类的实例
                qp.begin(self)
                # 原来self也可以当参数用，本类的实例作为参数传递
                #onepoint.draw(qwidget_obj = self,qp = qp)
                feature.draw(self, qp,view,True,0)
                qp.end()
            self.mouse = True
            self.flag = False
            # 画线
            #if self.btn_line.isChecked():
            #    qp = QPainter()
            #    x1 = int('0'+(self.X_text.text()))
            #    y1 = int('0'+(self.Y_text.text()))
            #    x2 = int('0'+(self.X_text2.text()))
            #    y2 = int('0'+(self.Y_text2.text()))                
            #    a = self.A_text.text()
            #    onevertex = GISVertex(x1,y1)
            #    twovertex = GISVertex(x2,y2)
            #    oneline = GISLine([onevertex,twovertex])
            #    text = self.A_text.text()
            #    oneattribute = GISAttribute()
            #    oneattribute.AddValue(text)
            #    onefeature = GISFeature(oneline,oneattribute)
            #    features[1].append(onefeature)
            #    for feature in features[1]:
            #        # 这个begin函数的参数为QWidget类的实例
            #        qp.begin(self)
            #        # 原来self也可以当参数用，本类的实例作为参数传递
            #        #onepoint.draw(qwidget_obj = self,qp = qp)
            #        feature.drawLine(self, qp,True,0)
            #        qp.end()
            #    self.mouse = True
            #    self.flag = False

    def mousePressEvent(self,  event):
        global features
        global view
        if self.mouse:
            #if self.btn_point.isChecked():
            x = event.x()
            y = event.y()
            id = -1
            mouselocation = view.ToMapVertex(QPoint(x,y))
            for i in range(len(features)):
                # 这里计算距离，改为使用GISspatial类的抽象方法，其子类负责具体实现，最终只要返回一个distance即可
                distance = features[i].GISSpatial_spatialpart.Distance(mouselocation)
                mindistance = 100000
                if distance < mindistance:
                    mindistance = distance
                    id = i
            if id == -1:
                QMessageBox.about(self,'错误',"没有任何空间对象！")  
                return
            nearestpoint = view.ToScreenPoint(features[id].sptialpart.centroid)
            screendistance = abs(nearestpoint.X-x)+abs(nearestpoint.Y-y)
            if screendistance > 5:
                QMessageBox.about(self,'太远了',"请靠近空间对象点击") 
            QMessageBox.about(self,'属性',"属性为： "+features[1][id].getAttribute(0)) 

            #if self.btn_line.isChecked():
            #    x = event.x()
            #    y = event.y()
            #    id = -1
            #    mouseclickvertex = GISVertex(x,y)
            #    for i in range(len(features[1])):
            #        # 这里计算距离，改为使用GISspatial类的抽象方法，其子类负责具体实现，最终只要返回一个distance即可
            #        distance = features[1][i].GISSpatial_spatialpart.Distance(mouseclickvertex)
            #        mindistance = 10
            #        if distance < mindistance:
            #            mindistance = distance
            #            id = i
            #    if mindistance >10 or id == -1:
            #        QMessageBox.about(self,'属性',"没有空间对象或者点击位置不准确！")  
            #    else:
            #        QMessageBox.about(self,'属性',"属性为： "+features[1][id].getAttribute(0))

    def mouseMoveEvent(self, e):
        x = e.pos().x()
        y = e.pos().y()
        text = "x: {0},  y: {1}".format(x, y)
        self.labelMousePos.setText(text)

    def update_map(self):
        global feaatures
        global view
        minx = int( self.text1.text())
        miny = int( self.text2.text())
        maxx = int( self.text3.text())
        maxy = int( self.text4.text())
        # 更新view
        view.Update(GISExtent(GISVertex(minx,miny),GISVertex(maxx,maxy)),self.frameGeometry())
        self.flag = True
        self.update()
