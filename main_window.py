# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from from_ui import *
import random
import PyQt5.QtWidgets as QtWidgets
from BasicClasses import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
import copy

features = []
view = None
layer = None
viewList = []
nowPointer = -1

# 继承两个类，qwidget类给构造函数，Ui_Form类给setupUi
class Lesson(QtWidgets.QWidget,Ui_Form):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        global view
        view = GISView(GISExtent(GISVertex(0,0),GISVertex(100,100)),self.frameGeometry())

        self.pushButton.clicked.connect(self.showOverview)
        self.pushButton_3.clicked.connect(self.change_map)
        self.pushButton_4.clicked.connect(self.change_map)
        self.pushButton_5.clicked.connect(self.change_map)
        self.pushButton_6.clicked.connect(self.change_map)
        self.pushButton_7.clicked.connect(self.change_map)
        self.pushButton_8.clicked.connect(self.change_map)
        self.pushButton_9.clicked.connect(self.change_map)
        self.pushButton_10.clicked.connect(self.change_map)
        self.pushButton_2.clicked.connect(self.openshp)
        self.updatethemap = False
        self.pushButton_9.setDisabled(True)
        self.pushButton_10.setDisabled(True)

    def openshp(self):
        global layer
        sf = GISShapefile()
        layer = sf.readPoint('/home/benfen/Downloads/ne_110m_populated_places/ne_110m_populated_places.shp')
        layer.bool_drawAttributeOrNot = False
        QMessageBox.information(self,'提示','读取到'+str(layer.FeatureCount())+'个点')

#---------------------------------------------更改地图view----------------------------------------------------------------

    def showOverview(self):
        # 显示整个图像，然后更新地图view，view再更新extent
        try:
            view.UpdateExtent(layer.GISExtent_Extent)
            self.UpdateMap()
        except AttributeError as e:
            print('错误:',e)

    def change_map(self):
        action = None
        sender = self.sender()

        if sender == self.pushButton_4:action = GISMapActions.zoomin
        elif sender == self.pushButton_7:action = GISMapActions.zoomout
        elif sender == self.pushButton_5:action = GISMapActions.moveup
        elif sender == self.pushButton_3:action = GISMapActions.movedown
        elif sender == self.pushButton_8:action = GISMapActions.moveleft
        elif sender == self.pushButton_6:action = GISMapActions.moveright
        elif sender == self.pushButton_9:self.undo()
        elif sender == self.pushButton_10:self.redo()

        if action:
            view.ChangeView(action)
            self.UpdateMap()

    
# ----------------------------------------------用最新的view画图----------------------------------------------------------------------

    # 统一的更新地图函数
    def UpdateMap(self):        
        self.pop_needlessand_add()
        # 作为触发事件的一个触发器
        self.updatethemap = True
        self.update()

    # 图事件
    def paintEvent(self,event):

        if nowPointer > 0:
            self.pushButton_9.setDisabled(False)
        else:
            self.pushButton_9.setDisabled(True)
        if nowPointer < len(viewList)-1:
            self.pushButton_10.setDisabled(False)
        else:
            self.pushButton_10.setDisabled(True)

        if self.updatethemap:
            qp = QPainter()
            qp.begin(self)
            layer.draw(self,qp,view)
            qp.end()
            self.updatethemap = False
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
    
    # 指针永远指向当前地图显示的范围，不论是否为最新的
    def pop_needlessand_add(self):
        global nowPointer,view,viewList
        if nowPointer <len(viewList)-1:
            for i in reversed(range(nowPointer + 1,len(viewList))):
                del viewList[i]
                print(i)
        viewCopy = copy.deepcopy(view)
        viewList.append(viewCopy)
        nowPointer += 1
            
    def undo(self):
        global nowPointer,view
        view = copy.deepcopy(viewList[nowPointer-1])
        nowPointer -=1
        self.updatethemap = True
        self.update()

    def redo(self):
        global nowPointer,view
        view = copy.deepcopy(viewList[nowPointer+1])
        nowPointer +=1
        self.updatethemap = True
        self.update()

    #def mousePressEvent(self,  event):
    #    global features
    #    global view
    #    if self.mouse:
    #        #if self.btn_point.isChecked():
    #        x = event.x()
    #        y = event.y()
    #        id = -1
    #        mouselocation = view.ToMapVertex(QPoint(x,y))
    #        for i in range(len(features)):
    #            # 这里计算距离，改为使用GISspatial类的抽象方法，其子类负责具体实现，最终只要返回一个distance即可
    #            distance = features[i].GISSpatial_spatialpart.Distance(mouselocation)
    #            mindistance = 100000
    #            if distance < mindistance:
    #                mindistance = distance
    #                id = i
    #        if id == -1:
    #            QMessageBox.about(self,'错误',"没有任何空间对象！")  
    #            return
    #        nearestpoint = view.ToScreenPoint(features[id].sptialpart.centroid)
    #        screendistance = abs(nearestpoint.X-x)+abs(nearestpoint.Y-y)
    #        if screendistance > 5:
    #            QMessageBox.about(self,'太远了',"请靠近空间对象点击") 
    #        QMessageBox.about(self,'属性',"属性为： "+features[1][id].getAttribute(0)) 