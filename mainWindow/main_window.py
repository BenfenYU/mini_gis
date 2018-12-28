# -*- coding: utf-8 -*-

from .ui import *
import random,os,copy,sys,time,threading
sys.setrecursionlimit(10000000)
from newBasicClass import *

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import Qt,QRect,QPoint,QPointF,QLineF,QRectF,pyqtSignal,QTimer

save_1,save_2,objectSave,screenObject =[], [],[],[]
ZOOMIN = 1
ZOOMOUT = 0

# 继承两个类，qwidget类给构造函数，Ui_Form类给setupUi
class MainWindow(Ui_MainWindow,QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.actionnext = QtWidgets.QAction(self)
        self.actionnext.setObjectName("actionnect")
        self.menuBuffer.addAction(self.actionnext)
        _translate = QtCore.QCoreApplication.translate
        self.actionnext.setText(_translate("MainWindow", "next"))

        self.actionstart_edit.triggered.connect(self.newBuffer)
        self.actionend_edit.triggered.connect(self.endEdit)
        self.actionbuffer.triggered.connect(self.buffer)
        self.actioninit.triggered.connect(self.initWindow)
        self.actionnext.triggered.connect(self.next)
        self.actionlayers.triggered.connect(self.showNames)

        self.drawWindow = DrawWindow(self)
        frameGeometry = self.geometry()
        # --------------------------和后端接轨------------------------
        self.layers = []
        self.nowLayer = -1
        self.viewList = [View(Extent(),self.drawWindow)]
        self.nowView = -1
        self.defaultView = View(Extent(),self.drawWindow)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)        # 窗体总在最前端
        '''
        下面是一些开关
        '''
        self.boolEdit = False
        self.layerDraw = False
        self.click = True
        
        #self.test()
        #self.buffer()

    def newBuffer(self):
        self.bufferWin = BufferWindow(self)

    def startEdit(self):
        self.boolEdit = True
        #mBox.showinfo('提示', '开始编辑。')

    def endEdit(self):
        global objectSave,screenObject\
        ,save_1,save_2
        self.boolEdit = False
        type = self.bufferAttr[0]
        if type == 1:
            layer = Layer(1,objectSave)
        elif type == 3:
            if len(objectSave)>2:
                save_1.append(SoloLine(objectSave))
                save_2.append(SoloLine(objectSave))
            layer = Layer(3,save_1)
        elif type == 5:
            save_1.append(SoloPolygon(objectSave))
            layer = Layer(5,save_1)
        #if not save_2 :
        #    QMessageBox.warning(self,'错误！','请数字化对象后再来！')
        #    return
        
        self.layers.append(layer)
        self.draw()
        objectSave = []
        screenObject = []
        save_1,save_2 = [],[]
        #mBox.showinfo('提示', '编辑结束。')
    
    def next(self):
        self.drawWindow.nextBuffer()
    
    def buffer(self):
        layer = Layer(1,None)
        polygonLayer = Buffer().buffer(layer)
        self.layers.append(polygonLayer)
        self.draw()
        '''
        r = self.bufferAttr[1]
        polygonLayer = Buffer().buffer(self.layer,r)
        polygonLayer.name = self.bufferAttr[2]
        self.layers.append(polygonLayer)
        self.draw()
        '''
    
    def draw(self):
        self.layerDraw = True
        self.drawWindow.updates()

    def openShp(self,filename):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,\
        "QFileDialog.getOpenFileName()", 
        "","ESRI shp (*.shp)", options=options)
        if fileName:
            sf = ReadSHP()
            path = os.path.abspath(filename)
            layer = sf.readshp(path)
            layer.bool_drawAttributeOrNot = False
            self.layers.append(layer)
            #QMessageBox.information(self,'提示','读取到'+str
            #(layer.FeatureCount())+'个点'+'Re为：'+str(Re)+'。Ro为:'+str(Ro))
            # 显示整个图像，然后更新地图view，view再更新extent
            try:
                self.view.UpdateExtent(layer.extent)
                self.update()
            except AttributeError as e:
                print('错误:',e)
        
    def showNames(self):
        pass
    
    @property
    def view(self):
        return self.viewList[self.nowView]
    
    @property
    def layer(self):
        return self.layers[self.nowLayer]
    
    def initWindow(self):
        self.initView()
        self.initLayers()
    
    def initView(self):
        self.viewList = [self.defaultView]
    
    def initLayers(self):
        self.layers = []

    '''
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
        


    
    def showOverview(self):
        # 显示整个图像，然后更新地图view，view再更新extent
        try:
            self.view.UpdateExtent(self.layer.extent)
            self.UpdateMap()
        except AttributeError as e:
            print('错误:',e)

    def paintEvent(self, event):
        # 画缓冲区的圆弧
        #rectt = QRect(50,90,1000,1200)
        #start = 90*16
        #span = 120*16
        if self.draw:
            qp = QPainter()
            #qp.begin(self)
            #qp.setBackground(QBrush(Qt.gray))
            #qp.drawArc(rectt,start,span)
            #qp.end()
            qp.begin(self)
            self.layers[self.nowLayer].draw(self,qp = qp)  
            qp.end()
        
        self.draw = False

    def wheelEvent(self,event):
        delta = event.angleDelta()
        if delta.y()>0:
            self.view.ChangeView(GISMapActions.zoomin)
        else:
            self.view.ChangeView(GISMapActions.zoomout)
        
        self.UpdateMap()

    def openDbf(self):
        if not self.layers:
            QMessageBox.information(self,'提示','请首先加载图层')
            return
        dbfWindow = DbfWindow(layer = self.layers[0])

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
            return index'''

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

class DrawWindow(Ui_Form,QWidget):
    def __init__(self,mainWindow):
        QWidget.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        self.doubleClick = False

        self.drawLine = False

        self.mainW= mainWindow
        self.show()
    
    def updates(self):
        self.update()
    
    def nextBuffer(self):
        type = self.mainW.bufferAttr[0]
        global screenObject,objectSave,save_1,save_2
        if  type != 1 and \
        self.mainW.boolEdit\
        and  objectSave:
            if len(screenObject) == 1:
                QMessageBox.warning(self,'错误！','您现在只提供了一个点！')
                return
                
            if type == 3:
                save_1.append(SoloLine(objectSave))
                save_2.append(SoloLine(screenObject))
            elif type == 5:
                save_1.append(SoloPolygon(objectSave))
                save_2.append(SoloPolygon(screenObject))

            screenObject = []
            objectSave = []

    def mousePressEvent(self, event):
        type = self.mainW.bufferAttr[0]
        if self.mainW.boolEdit:
            global objectSave,screenObject
            x = event.x()
            y = event.y()
            view = self.mainW.defaultView
            mapPoint = view.toMapPoint(SoloPoint(x,y))
            objectSave.append(mapPoint)
            screenObject.append(SoloPoint(x,y))
            if type == 3 and len(screenObject)>1:
                self.drawLine = True

            self.update()
        
    def wheelEvent(self,e):
        lastView = self.mainW.view
        if e.angleDelta().y()>0:
            lastView.changeView(ZOOMIN,e.x(),e.y())
        elif e.angleDelta().y()<0:
            lastView.changeView(ZOOMOUT,e.x(),e.y())
        self.mainW.viewList.append(lastView) 
        self.mainW.layerDraw = True
        self.update()


    
    '''
    def mouseDoubleClickEvent(self,e):
        type = self.mainW.bufferAttr[0]
        if  type != 1 and \
        self.mainW.boolEdit:
            global screenObject,objectSave,save_1,save_2
            if type == 3:
                save_1.append(SoloLine(objectSave))
                save_2.append(SoloLine(screenObject))
            elif type == 5:
                save_1.append(SoloPolygon(objectSave))
                save_2.append(SoloPolygon(screenObject))

            screenObject = []
            objectSave = []
    '''
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        if self.mainW.layerDraw:
            pen = QPen(Qt.red, 1, Qt.SolidLine)
            qp.setPen(pen)
            # 如果不传参数view，那么画的时候就不会进行坐标转换
            self.mainW.layer.draw(qp = qp\
            ,view = self.mainW.view)              
            self.mainW.layerDraw = False
        elif self.mainW.boolEdit:
            pen = QPen(Qt.red, 5, Qt.SolidLine)
            qp.setPen(pen)
            for p in screenObject:
                p.draw(qp)
            type = self.mainW.bufferAttr[0]
            if self.drawLine :
                SoloLine(screenObject).draw(qp)
                self.drawLine = False
            if save_2:
                [o.draw(qp) for o in save_2]
            #if type == 3 or type == 5:
            #    for obj in save_1:
            #        obj.draw(qp)

        qp.end()
    
    def drawAl(self,qp,screenObject):
        screenPoints = [p.pointToQpointF() for p in screenObject]
        [qp.drawLine(QLineF(screenPoints[i],screenPoints[i+1]))
        for i in range(len(screenPoints)-1)]

class BufferWindow(BufferWin,QDialog):
    def __init__(self,mainWindow):
        QDialog.__init__(self)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.finish)
        self.pushButton_2.clicked.connect(self.close)

        self.mainW= mainWindow
        self.show()
    
    def finish(self):
        if self.radioButton.isChecked():
            type = 1
        elif self.radioButton_2.isChecked():
            type = 3
        elif self.radioButton_3.isChecked():
            type = 5
        else:
            QMessageBox.warning(self,"错误","请选择对象类型！")
            return
        
        r = self.lineEdit_2.text()
        if (not r.isdigit()) or int(r)<=0:
            QMessageBox.warning(self,"错误","请输入正数！")
            return
            
        name = self.lineEdit.text()
        if not name:
            QMessageBox.warning(self,"错误","请输入图层名字")
            return
        
        self.mainW.bufferAttr = (type,int(r),name)
        self.mainW.startEdit()
        self.close()
        
