# -*- coding: utf-8 -*-

from .fromUi import *
import random,os,copy,sys
from basicClass import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import Qt,QRect,QPoint,QPointF,QLineF,QRectF,pyqtSignal

layer = None

# 继承两个类，qwidget类给构造函数，Ui_Form类给setupUi
class MainWindow(QtWidgets.QWidget,Ui_Form):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        # 当前界面所有layer，以及需要显示的layer的索引
        self.layers = []
        self.nowLayer = [0]
        self.click = True
        self.viewList = []
        self.__layer = None
        self.nowPointer = len(self.viewList)-1
        self.drawLine = False
        self.features = []
        frameGeometry = self.geometry()
        self.view = GISView(GISExtent(GISVertex(0,0),GISVertex(100,100)),\
        frameGeometry)

        self.pushButton.clicked.connect(self.showOverview)
        self.pushButton_3.clicked.connect(self.change_map)
        self.pushButton_4.clicked.connect(self.change_map)
        self.pushButton_5.clicked.connect(self.change_map)
        self.pushButton_6.clicked.connect(self.change_map)
        self.pushButton_7.clicked.connect(self.change_map)
        self.pushButton_8.clicked.connect(self.change_map)
        self.pushButton_9.clicked.connect(self.change_map)
        self.pushButton_10.clicked.connect(self.change_map)
        self.pushButton_11.clicked.connect(self.openDbf)
        self.pushButton_2.clicked.connect(self.openFileNameDialog)
        self.pushButton_9.setDisabled(True)
        self.pushButton_10.setDisabled(True)
        
    
    def clickSelect(self,vertex):
        minIndex = None
        # 当前显示的图层中计算距离
        for index in self.nowLayer:
            # 计算距离并找到最小值
            distancelist = self.layers[index].distance(vertex)
            minValue = min(distancelist)
            minIndex = distancelist.index(minValue)
            print(vertex.x,vertex.y)
            print(minValue,minIndex)
            self.layers[index].draw(self,self.view,\
            featureIndex = minIndex,color = Qt.green)  
            
            return index
    

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,\
        "QFileDialog.getOpenFileName()", 
        "","ESRI shp (*.shp)", options=options)
        if fileName:
            self.openshp(fileName)

    def openshp(self,filename):
        sf = GISShapefile()
        path = os.path.abspath(filename)
        layer = sf.readshp(path)
        layer.bool_drawAttributeOrNot = False
        self.layers.append(layer)
        print('读图完毕，开始画图')
        self.showOverview(layer)
        #QMessageBox.information(self,'提示','读取到'+str(layer.FeatureCount())+'个点'+'Re为：'+str(Re)+'。Ro为:'+str(Ro))



    def openDbf(self):
        if not self.layers:
            QMessageBox.information(self,'提示','请首先加载图层')
            return
        dbfWindow = DbfWindow(layer = self.layers[0])
        

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
            self.view.ChangeView(action)
            self.UpdateMap()

    def paintEvent(self, event):
            if self.drawLine:
                qp = QPainter()
                
                self.__layer.draw(self,self.view,qp = qp)
                

    # 双击显示其属性表
    def mouseDoubleClickEvent(self,e):
        vertex = GISVertex(e.screenPos().x()-5,e.screenPos().y()-71)
        x = vertex.getX()
        y = vertex.getY()

        if self.layers :
            vertex = self.screenToMap(self.view,vertex)
            if self.click:
                index = self.clickSelect(vertex)
                dbf = DbfWindow(self.__layer,index = index)
                dbf.show()
                #print(vertex.ge    color = Qt.red,thickness = 5)
        else:
            print(x,y)

            return        
    
    # (5, 71, 1340, 620)
    def mousePressEvent(self,e): 
        # 这里要修改一下，因为鼠标的坐标是在canvas里的，所以必须要先换算成相对整个
        # 屏幕的坐标，再换算为地图坐标。
        vertex = GISVertex(e.screenPos().x()-5,e.screenPos().y()-71)
        x = vertex.getX()
        y = vertex.getY()

        if self.layers :
            vertex = self.screenToMap(self.view,vertex)
            if self.click:
                self.clickSelect(vertex)
                #print(vertex.ge    color = Qt.red,thickness = 5)
        else:
            print(x,y)

            return
    
    def screenToMap(self,view,vertex):
        return view.toMapVertex(vertex)

    def getLayer(self):
        return self.__layer

    #def __transfer(self,X,Y):
    #    x = X-self.canvasFrameGeometryF.x()
    #    y = Y - self.canvasFrameGeometryF.y()
    #    
    #    return x,y

    def showOverview(self,layer):
        # 显示整个图像，然后更新地图view，view再更新extent
        try:
            self.__layer = layer
            self.view.UpdateExtent(self.__layer.GISExtent_Extent)
            self.UpdateMap()
        except AttributeError as e:
            print('错误:',e)
    

    # 统一的更新地图函数
    def UpdateMap(self):        
        self.pop_needlessand_add()
        # 作为触发事件的一个触发器
        # self.updatethemap = True
        self.paint()

    # 图事件
    def paint(self):

        if self.nowPointer > 0:
            self.pushButton_9.setDisabled(False)
        else:
            self.pushButton_9.setDisabled(True)
        if self.nowPointer < len(self.viewList)-1:
            self.pushButton_10.setDisabled(False)
        else:
            self.pushButton_10.setDisabled(True)

        #self.clear()
        self.drawLine = True
        self.update()
            
    
    # 指针永远指向当前地图显示的范围，不论是否为最新的
    def pop_needlessand_add(self):
        if self.nowPointer <len(self.viewList)-1:
            for i in reversed(range(self.nowPointer + 1,len(self.viewList))):
                del viewList[i]
                print(i)
        viewCopy = copy.deepcopy(self.view)
        self.viewList.append(viewCopy)
        self.nowPointer += 1
            
    def undo(self):
        self.view = copy.deepcopy(self.viewList[self.nowPointer-1])
        self.nowPointer -=1
        self.updatethemap = True
        self.paint()

    def redo(self):
        self.view = copy.deepcopy(self.viewList[self.nowPointer+1])
        self.nowPointer +=1
        self.updatethemap = True
        self.paint()

class DbfWindow(QDialog):
    # index用来辨识输入的是整个图层还是图层的某个要素
    def __init__(self,layer = None,index = None,\
    frameGeometry = (5, 71, 1340, 620)):
        super().__init__()
        self.initDbf(layer,index,frameGeometry)        
        self.show()

    def initDbf(self,layer,index,geo):
        

        self.dbfTable = QTableWidget()
        self.setGeometry(geo[0],geo[1],geo[2],geo[3])

        # 根据index是否为none来执行不同的函数
        if not index:
            features,columnName = self.__getFieldFromLayer(layer)
            self.setWindowTitle(layer.name+'的属性表')
            self.dbfTable.setRowCount(len(features))
        else :
            feature,columnName = self.__getFieldFromFeature(layer,index)
            self.dbfTable.setRowCount(1)
        
        #循环给表格的第一行赋值
        for n in range(0,len(columnName)):
            item = QTableWidgetItem(columnName[n])
            self.dbfTable.setItem(0,n,item)

        if not index:
            for m in range(0,len(features)):
                # print(m)
                for n in range(0,len(columnName)):
                    newItem = QTableWidgetItem(str(features[m].getAttribute(n)))  
                    self.dbfTable.setItem(m+1, n, newItem)  
        else:
            for n in range(0,len(columnName)):
                newItem = QTableWidgetItem(str(feature.getAttribute(n)))  
                self.dbfTable.setItem(index, n, newItem) 
        
        self.dbfTable.setColumnCount(len(columnName)+1)  
        self.dbfTable.move(0,0)
        self.layout = QVBoxLayout() 
        self.layout.addWidget(self.dbfTable)  
        self.setLayout(self.layout)

        return


    def __getFieldFromLayer(self,layer):
        fieldKind = layer.getAttriColum()
        # 存储有多少个属性
        columnName = []
        for fieldkind in fieldKind:
            columnName.append(fieldkind[0])
        # 存储有多少条记录
        featureNum = layer.FeatureCount()
        features = layer.getFeature()
        return features,columnName
    
    def __getFieldFromFeature(self,layer,index):
        feature = layer.getFeature()[index]
        fieldKind = layer.getAttriColum()
        # 存储有多少个属性
        columnName = []
        for fieldkind in fieldKind:
            columnName.append(fieldkind[0])

        return feature,columnName