# -*- coding: utf-8 -*-

from .fromUi import *
import random,os,copy,sys
sys.setrecursionlimit(10000)
from basicClass.layer import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import Qt,QRect,QPoint,QPointF,QLineF,QRectF,pyqtSignal
from tools import *


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
        self.layer = None
        self.nowPointer = len(self.viewList)-1
        self.drawLine = False
        self.features = []
        frameGeometry = self.geometry()
        self.view = GISView(GISExtent(GISVertex(0,0),GISVertex(100,100)),\
        frameGeometry)
        #self.backGround = None
        #self.setBack = False

        self.pushButton.clicked.connect(self.showOverview)
        #self.pushButton_3.clicked.connect(self.change_map)
        #self.pushButton_4.clicked.connect(self.change_map)
        #self.pushButton_5.clicked.connect(self.change_map)
        #self.pushButton_6.clicked.connect(self.change_map)
        #self.pushButton_7.clicked.connect(self.change_map)
        #self.pushButton_8.clicked.connect(self.change_map)
        self.pushButton_9.clicked.connect(self.change_map)
        self.pushButton_10.clicked.connect(self.change_map)
        self.pushButton_11.clicked.connect(self.openDbf)
        self.pushButton_2.clicked.connect(self.openFileNameDialog)
        self.pushButton_9.setDisabled(True)
        self.pushButton_10.setDisabled(True)
        self.pushButton_12.clicked.connect(self.kMean)
        self.pushButton_13.clicked.connect(self.dbScan)

    def kMean(self):
        try:
            kMeanObj = KMeans(self.layer, 5, 200,self.view)
            classIndex,classResult,returnValue = kMeanObj.startK()
            QMessageBox.information(self,'result','Kmean计算完成。')
        except BaseException as e:
            QMessageBox.information(self,'wrong',str(e))
        
        self.paint()

    def dbScan(self):
        try:
            dbObj = DBScan(self.layer,view = self.view,r =200 ,minPts = 4)
            returnValue = dbObj.findKernal()
            if returnValue == 0:
                QMessageBox.information(self,'result','DBScan聚类：没有找到核心点！')
            else:
                QMessageBox.information(self,'result','DBScan计算完成')
        except BaseException as e:
            print(e)
        
        self.paint()

    def paintEvent(self, event):
        # 画缓冲区的圆弧
        #rectt = QRect(50,90,1000,1200)
        #start = 90*16
        #span = 120*16
        if self.drawLine:
            qp = QPainter()
            #qp.begin(self)
            #qp.setBackground(QBrush(Qt.gray))
            #qp.drawArc(rectt,start,span)
            #qp.end()
            self.layer.draw(self,self.view,qp = qp)  
        
        self.drawLine = False

    def wheelEvent(self,event):
        delta = event.angleDelta()
        if delta.y()>0:
            self.view.ChangeView(GISMapActions.zoomin)
        else:
            self.view.ChangeView(GISMapActions.zoomout)
        
        self.UpdateMap()


    # 双击显示其属性表
    def mouseDoubleClickEvent(self,e):
        vertex = GISVertex(e.screenPos().x()-5,e.screenPos().y()-71)
        x = vertex.getX()
        y = vertex.getY()

        if self.layers :
            vertex = self.screenToMap(self.view,vertex)
            if self.click:
                index = self.clickSelect(vertex)
                dbf = DbfWindow(self.layer,index = index)
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

    #def __transfer(self,X,Y):
    #    x = X-self.canvasFrameGeometryF.x()
    #    y = Y - self.canvasFrameGeometryF.y()
    #    
    #    return x,y
        
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

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,\
        "QFileDialog.getOpenFileName()", 
        "","ESRI shp (*.shp)", options=options)
        if fileName:
            self.openshp(fileName)

    def openshp(self,filename):
        sf = ReadSHP()
        path = os.path.abspath(filename)
        self.layer = sf.readshp(path)
        self.layer.bool_drawAttributeOrNot = False
        self.layers.append(layer)
        self.showOverview()
        # QMessageBox.information(self,'提示','读取到'+str
        # (layer.FeatureCount())+'个点'+'Re为：'+str(Re)+'。Ro为:'+str(Ro))

    def showOverview(self):
        # 显示整个图像，然后更新地图view，view再更新extent
        try:
            self.view.UpdateExtent(self.layer.GISExtent_Extent)
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

    def openDbf(self):
        if not self.layers:
            QMessageBox.information(self,'提示','请首先加载图层')
            return
        dbfWindow = DbfWindow(layer = self.layers[0])

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