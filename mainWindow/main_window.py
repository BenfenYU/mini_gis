# -*- coding: utf-8 -*-

from .fromUi import *
import random,os,copy,sys
from basicClass import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import Qt,QRect,QPoint,QPointF,QLineF,QRectF

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
        self.frameGeometryF = QRectF(self.graphicsView.frameGeometry())
        global view
        view = GISView(GISExtent(GISVertex(0,0),GISVertex(100,100)),self.frameGeometryF)

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

        self.scene = QtWidgets.QGraphicsScene(self.frameGeometryF)
        self.graphicsView.setScene(self.scene)


    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", 
        "","ESRI shp (*.shp)", options=options)
        if fileName:
            self.openshp(fileName)

    def openshp(self,filename):
        global layer
        sf = GISShapefile()
        path = os.path.abspath(filename)
        layer = sf.readshp(path)
        layer.bool_drawAttributeOrNot = False
        print('读图完毕，开始画图')
        self.showOverview()
        #QMessageBox.information(self,'提示','读取到'+str(layer.FeatureCount())+'个点'+'Re为：'+str(Re)+'。Ro为:'+str(Ro))

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
        # self.updatethemap = True
        self.paint()

    # 图事件
    def paint(self):

        if nowPointer > 0:
            self.pushButton_9.setDisabled(False)
        else:
            self.pushButton_9.setDisabled(True)
        if nowPointer < len(viewList)-1:
            self.pushButton_10.setDisabled(False)
        else:
            self.pushButton_10.setDisabled(True)

        self.scene.clear()
        qp = QPainter()
        layer.draw(self,qp,view)
            
    
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
        self.paint()

    def redo(self):
        global nowPointer,view
        view = copy.deepcopy(viewList[nowPointer+1])
        nowPointer +=1
        self.updatethemap = True
        self.paint()

    def openDbf(self):
        if not layer:
            QMessageBox.information(self,'提示','请首先加载图层')
            return
        
        fieldKind = layer.getAttriColum()
        # 存储有多少个属性
        columnName = []
        for fieldkind in fieldKind:
            columnName.append(fieldkind[0])

        # 存储有多少条记录
        featureNum = layer.FeatureCount()
        features = layer.getFeature()

        self.dbfWin = QWidget()
        self.dbfWin.dbfTable = QTableWidget()
        self.dbfWin.dbfTable.setRowCount(featureNum)
        self.dbfWin.dbfTable.setColumnCount(len(columnName)+1)
        self.dbfWin.setGeometry(self.frameGeometry())
        self.dbfWin.setWindowTitle(layer.name+'的属性表')


        # 循环给窗体表格赋值
        for n in range(0,len(columnName)):
            item = QTableWidgetItem(columnName[n])
            self.dbfWin.dbfTable.setItem(0,n,item)

        for m in range(0,len(features)):
            # print(m)
            for n in range(0,len(columnName)):
                newItem = QTableWidgetItem(str(features[m].getAttribute(n)))  
                self.dbfWin.dbfTable.setItem(m+1, n, newItem)  
        self.dbfWin.dbfTable.move(0,0)

        self.dbfWin.layout = QVBoxLayout() 
        self.dbfWin.layout.addWidget(self.dbfWin.dbfTable)  
        self.dbfWin.setLayout(self.dbfWin.layout)
        
        self.dbfWin.show()
        