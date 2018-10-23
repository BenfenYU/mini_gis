# coding : utf-8
import math,shapefile,copy,os
from PyQt5.QtCore import Qt,QRect,QPoint,QPointF,QLineF
from abc import ABCMeta, abstractmethod
from PyQt5.QtGui import QPainter, QPen
from enum import Enum

# ----------------------------------------------------------

class SHAPETYPE(Enum):
    point = 1
    line = 3
    polygon = 5

class GISMapActions(Enum):
    zoomin = 1
    zoomout = 2
    moveup = 3
    movedown = 4
    moveleft = 5
    moveright = 6
    preone = 7
    nextone = 8

#-----------------------------------------------------------

class GISLayer:
    def __init__(self,name,SHAPETYPE_ShapeType,GISExtent_Extent):
        self.name = name
        self.shapeType = SHAPETYPE_ShapeType
        self.GISExtent_Extent = GISExtent_Extent
        self.bool_DrawAttributeOrNot = False
        self.labelIndex = 0
        self.__GISFeature_Features = []
    
    def draw(self,qwidget_obj,qp,GISView_view):
        # 每个都画了
        for i in range(len(self.__GISFeature_Features)):
            self.__GISFeature_Features[i].draw(qwidget_obj,qp,GISView_view,self.bool_DrawAttributeOrNot,self.labelIndex)
    
    def AddFeature(self,GISFeature_feature):
        self.__GISFeature_Features.append(GISFeature_feature)
    
    def FeatureCount(self):
        return len(self.__GISFeature_Features)


# ---------------------------------------------------------

class GISFeature:
    def __init__(self,GISSpatial_spatialpart,GISAttribute_attribute):
        self.GISSpatial_spatialpart = GISSpatial_spatialpart
        self.GISAttribute_attribute = GISAttribute_attribute

    def draw(self,qwidget_obj,qp,GISView_view,bool_DrawAttributeOrNot,index):
        self.GISSpatial_spatialpart.draw(qwidget_obj,qp,GISView_view)
        if bool_DrawAttributeOrNot:
            self.GISAttribute_attribute.draw(qwidget_obj,qp,GISView_view,self.GISSpatial_spatialpart.GISVertex_centroid,index)

    def drawLine(self,qwidget_obj,qp,GISView_view,bool_DrawAttributeOrNot,index):
        self.GISSpatial_spatialpart.draw(qwidget_obj,qp,GISView_view)
        if bool_DrawAttributeOrNot:
            self.GISAttribute_attribute.draw(qwidget_obj,qp,GISView_view,self.GISSpatial_spatialpart.List_allvertex[0],index)
    
    def getAttribute(self,index):
        return self.GISAttribute_attribute.GetValue(index)

# ----------------------------------------------------------

class GISAttribute:
    def __init__(self):
        self.List_values = []

    def AddValue(self,object_attribute):
        self.List_values.append(object_attribute)

    def GetValue(self,index):
        return self.List_values[index]
    
    def draw(self,qwidget_obj,qp,GISView_view,GISVertex_location,index):
        Point_screenpoint = GISView_view.ToScreenPoint(GISVertex_location)
        qp.setPen(Qt.red)
        size = qwidget_obj.size()
        qp.drawText(QRect(Point_screenpoint.x(),Point_screenpoint.y()-40,80,30),Qt.AlignCenter,self.List_values[index])        

# ----------------------------------------------------------

class GISSpatial(metaclass = ABCMeta):
    def __init__(self,GISVertex_centroid,GISExtent_extent):
        self.GISVertex_centroid = GISVertex_centroid
        self.GISExtent_extent = GISExtent_extent

    @abstractmethod
    def draw(self,qp,GISView_view):
        return
    
    @abstractmethod
    def Distance(self):
        return

# ----------------------------------------------------------

class GISExtent:
    
    ZoomingFactor = 2
    MovingFactor = 0.25
    
    action_record = [[0,0,100,100]]
    now_pointer = 0 

    def __init__(self,GISVertex_bottomleft,GISVertex_upright):
        self.GISVertex_bottomleft = GISVertex_bottomleft
        self.GISVertex_upright = GISVertex_upright
        self.newminx = self.GISVertex_bottomleft.x
        self.newminy = self.GISVertex_bottomleft.y
        self.newmaxx = self.GISVertex_upright.x
        self.newmaxy = self.GISVertex_upright.y

    def getMinX(self):
        return self.GISVertex_bottomleft.x

    def getMaxX(self):
        return self.GISVertex_upright.x

    def getMinY(self):
        return self.GISVertex_bottomleft.y

    def getMaxY(self):
        return self.GISVertex_upright.y
    
    def getWidth(self):
        return self.GISVertex_upright.x-self.GISVertex_bottomleft.x

    def getHeight(self):
        return self.GISVertex_upright.y-self.GISVertex_bottomleft.y

    def ChangeExtent(self,GISMapActions_action):       
        if GISMapActions_action == GISMapActions.zoomin:
            self.zoomin()
        elif GISMapActions_action == GISMapActions.zoomout:
            self.zoomout()
        elif GISMapActions_action == GISMapActions.moveup:
            self.moveup()
        elif GISMapActions_action == GISMapActions.movedown:
            self.movedown()
        elif GISMapActions_action == GISMapActions.moveleft:
            self.moveleft()
        elif GISMapActions_action == GISMapActions.moveright:
            self.moveright()
        elif GISMapActions_action == GISMapActions.preone:
            self.gopre()
        elif GISMapActions_action == GISMapActions.nextone:
            self.nextone()
        #另一种代替switch的写法，但是有点小bug
        #switch = {
        #    GISMapActions.zoomin:self.zoomin(),
        #    GISMapActions.zoomout:self.zoomout(),
        #    GISMapActions.moveup:self.moveup(),
        #    GISMapActions.movedown:self.movedown(),
        #    GISMapActions.moveleft:self.moveleft(),
        #    GISMapActions.moveright:self.moveright(),
        #}
        #        
        #switch[GISMapActions_action]
        self.GISVertex_upright.x = self.newmaxx
        self.GISVertex_upright.y = self.newmaxy
        self.GISVertex_bottomleft.x = self.newminx
        self.GISVertex_bottomleft.y = self.newminy
        
    
    def zoomin(self):
        self.newminx = ((self.getMinX()+self.getMaxX())-self.getWidth()/self.ZoomingFactor) /2
        self.newminy = ((self.getMinY()+self.getMaxY())-self.getHeight()/self.ZoomingFactor) /2
        self.newmaxx = ((self.getMinX()+self.getMaxX())+self.getWidth()/self.ZoomingFactor) /2
        self.newmaxy = ((self.getMinY()+self.getMaxY())+self.getHeight()/self.ZoomingFactor) /2    

    def zoomout(self):
        self.newminx = ((self.getMinX()+self.getMaxX())-self.getWidth()*self.ZoomingFactor) /2
        self.newminy = ((self.getMinY()+self.getMaxY())-self.getHeight()*self.ZoomingFactor) /2
        self.newmaxx = ((self.getMinX()+self.getMaxX())+self.getWidth()*self.ZoomingFactor) /2
        self.newmaxy = ((self.getMinY()+self.getMaxY())+self.getHeight()*self.ZoomingFactor) /2

    def moveup(self):
        self.newminy = self.getMinY()-self.getHeight()* self.MovingFactor
        self.newmaxy = self.getMaxY()-self.getHeight()* self.MovingFactor

    def movedown(self):
        self.newminy = self.getMinY() + self.getHeight() * self.MovingFactor
        self.newmaxy = self.getMaxY()+self.getHeight() * self.MovingFactor

    def moveleft(self):
        self.newminx = self.getMinX() + self.getWidth() * self.MovingFactor
        self.newmaxx = self.getMaxX()+self.getWidth() * self.MovingFactor

    def moveright(self):
        self.newminx = self.getMinX() - self.getWidth() * self.MovingFactor
        self.newmaxx = self.getMaxX()-self.getWidth() * self.MovingFactor 

    def gopre(self):
        [self.newminx,self.newminy,self.newmaxx,self.newmaxy ]= GISExtent.action_record[GISExtent.now_pointer-1]
        GISExtent.now_pointer-=1  
    
    def nextone(self):
        [self.newminx,self.newminy,self.newmaxx,self.newmaxy ]= GISExtent.action_record[GISExtent.now_pointer+1]
        GISExtent.now_pointer+=1  
    

    def copyFrom(self,GISExtent_extent):
        self.GISVertex_upright.copyFrom(GISExtent_extent.GISVertex_upright)
        self.GISVertex_bottomleft.copyFrom(GISExtent_extent.GISVertex_bottomleft)
 

# ----------------------------------------------------------
class GISVertex:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
    
    def Distance(self,GISVertex_anothervertex):
        # 返回距离
        distance = math.sqrt((self.x-GISVertex_anothervertex.x)*(self.x - GISVertex_anothervertex.x)+pow((self.y-GISVertex_anothervertex.y),2));
        return distance;

    def copyFrom(self,GISVertex_v):
        self.x = GISVertex_v.x
        self.y = GISVertex_v.y

# ------------------------------------------------------

class GISPoint(GISSpatial):
    def __init__(self,GISVertex_onevertex):
        self.GISVertex_centroid = GISVertex_onevertex
        self.GISExtent_extent = GISExtent(GISVertex_onevertex,GISVertex_onevertex)
    
    def draw(self,qwidget_obj,qp,GISView_view):
        Point_screenpoint = GISView_view.ToScreenPoint(self.GISVertex_centroid)
        pen = QPen(Qt.red, 10, Qt.SolidLine)
        r = QPoint(Point_screenpoint.x(), Point_screenpoint.y())
        # 用添加椭圆的方法画点
        qwidget_obj.scene.addEllipse(Point_screenpoint.x(), Point_screenpoint.y(), 2.0, 2.0, pen)

    def Distance(self,GISVertex_anothervertex):
        return self.GISVertex_centroid.Distance(GISVertex_anothervertex)


class GISLine(GISSpatial):
    def __init__(self,List_allvertex):
        self.List_allvertex = List_allvertex
    
    def draw(self,qwidget_obj,qp,GISView_view):
        qLineFsToScreenList = GISView_view.toScreenLine(self.List_allvertex)
        for qLineF in qLineFsToScreenList:
            pen = QPen(Qt.blue, 10, Qt.SolidLine)
            # 用添加椭圆的方法画点
            qwidget_obj.scene.addLine(qLineF , pen)

    def Distance(self,GISVertex_anothervertex):
        # 补充点到直线的距离
        x1 = self.List_allvertex[0].x
        y1 = self.List_allvertex[0].y
        x2 = self.List_allvertex[1].x
        y2 = self.List_allvertex[1].y
        k1 = (y2-y1)/(x2-x1)
        k2 = -1/k1
        b1 = y1-k1*x1
        x3 = GISVertex_anothervertex.x
        y3 = GISVertex_anothervertex.y
        x4 = (k2* x3+b1-y3)/(k2-k1)
        y4 = k1 * x4 + b1
        distance = math.sqrt((y3-y4)**2+(x3-x4)**2)

        return distance


class GISPolygon(GISSpatial):
    def __init__(self,List_allvertex):
        self.List_allvertex = List_allvertex
    
    def draw(self,qwidget_obj,qp,GISView_view):
        return

# -------------------------------------------------------------

class GISView:


    def __init__(self,GISExtent_extent,Qrect_rectangle):
        self.Update(GISExtent_extent,Qrect_rectangle)
    
    def Update(self,GISExtent_extent,Qrectrectangle):
        self.GISExtent_currentmapextent = GISExtent_extent
        self.MapWindowSize = Qrectrectangle
        self.MapMinX = self.GISExtent_currentmapextent.getMinX()
        self.MapMinY = self.GISExtent_currentmapextent.getMinY()
        # widh和height属性待补充
        self.WinW = Qrectrectangle.width()
        self.WinH = Qrectrectangle.height()
        self.MapW = self.GISExtent_currentmapextent.getWidth()
        self.MapH = self.GISExtent_currentmapextent.getHeight()
        self.ScaleX = self.MapW/self.WinW
        self.ScaleY = self.MapH/self.WinH

    def ToScreenPoint(self,GISVertex_onevertex):
        print(GISVertex_onevertex.x)
        ScreenX = (GISVertex_onevertex.x-self.MapMinX)/self.ScaleX
        ScreenY = self.WinH-(GISVertex_onevertex.y-self.MapMinY)/self.ScaleY
        point = QPoint(int(ScreenX),int(ScreenY))
        return point
    
    def toScreenLine(self,listVertex):
        qLineFs = []
        listPointF = []
        for i in range(len(listVertex)):# ?????为什么减一才行
            vertex = listVertex[i]
            qPoint = self.ToScreenPoint(vertex)
            pointF = QPointF(qPoint)
            listPointF.append(pointF)

        for i in range(len(listVertex)-2):
            qLineF = QLineF(listPointF[i],listPointF[i+1])
            qLineFs.append(qLineF)

        return qLineFs


    def ToMapVertex(self,Point_point):
        MapX = self.ScaleX * Point_point.x()+self.MapMinX
        MapY = self.ScaleY * (self.WinH-Point_point.y())+self.MapMinY
        return GISVertex(MapX,MapY)

    def ChangeView(self,GISMapActions_action):
        # 改变范围
        self.GISExtent_currentmapextent.ChangeExtent(GISMapActions_action)
        # 更新view的各比例
        self.Update(self.GISExtent_currentmapextent,self.MapWindowSize)

    def UpdateExtent(self,GISExtent_extent):
        self.GISExtent_currentmapextent.copyFrom(GISExtent_extent)
        self.Update(self.GISExtent_currentmapextent,self.MapWindowSize)

    # 这是个错误示范，self.GISExtent是引用变量，指向地址，不直接存储值大小，多个变量指向同一地址，修改一次，所有变量指向的值都会发生变化
    # def reView(self):
    #    GISView.now_pointer -=1
    #    self.GISExtent_currentmapextent = GISView.action_record[GISView.now_pointer]
    #    print(self.GISExtent_currentmapextent.GISVertex_upright.x)
    #    print(GISView.now_pointer)
    #    self.Update(self.GISExtent_currentmapextent,self.MapWindowSize)

# ---------------------------------------------------------------

class GISShapefile:
    def readshp(self,shp):
        name = os.path.basename(shp)
        # 读出二进制
        myshp = open(shp, "rb")
        # 从二进制读shp对象
        sf = shapefile.Reader(shp=myshp)
        # 图层
        shapes = sf.shapes()
        type = shapes[0].shapeType
        if type == 1 or 8:
            layer = self.readLine(shapes,type,name)
        elif type ==3:
            print('线')
            layer = self.readLine(shapes,type,name)
            
        elif type == 5:
            layer = self.readPolygon(shapes,type,name)
        else:
            QMessageBox.information(self,'提示','暂时不支持，请升级后再来。')
        
        return layer

    def readPoint(self,shapes,type,name):
        X = []
        Y = []
        features = []
        tempX = []
        tempY = []
        # 这里细化到组成每个空间对象的点
        for shape in shapes:
            for point in shape.points:
                X.append(point[0])
                Y.append(point[1])
                onePoint = GISPoint(GISVertex(point[0],point[1]))
                onefeature = GISFeature(onePoint,GISAttribute())
                features.append(onefeature)
        #minValue = []
        #for i in range(len(X)):
        #    tempX,tempY = copy.deepcopy(X),copy.deepcopy(Y)
        #    tempX.pop(i)
        #    tempY.pop(i)
        #    print('计算第个'+str(i)+'点')
        #    for n in range(len(tempX)):
        #        out = []
        #        out.append((pow(tempX[n]-X[i],2)+pow(tempY[n]-Y[i],2))**0.5)
        #    minValue.append(min(out))
        # 根据全部点的位置，找到最大和最小，构成extent
        xMin = min(X)
        yMin = min(Y)
        xMax = max(X)
        yMax = max(Y)
        GISExtent_extent = GISExtent(GISVertex(xMin,yMin),GISVertex(xMax,yMax))
        GISLayer_layer = GISLayer(name,type,GISExtent_extent)
        for feature in features:
            GISLayer_layer.AddFeature(feature)
        # 要返回一个layer类的对象
        # Re,Ro = self.pointPattern(GISLayer_layer,minValue,xMin,yMin,xMax,yMax)
        return GISLayer_layer#,Re,Ro

    def readLine(self,shapes,type,name):
        Xextent = []
        Yextent = []
        vertexInOneline = []
        allLines = []
        features = []

        for shape in shapes:
            # 录入每个线对象的经度和纬度范围，方便比较
            Xextent.append(shape.bbox[0])
            Xextent.append(shape.bbox[2])
            Yextent.append(shape.bbox[1])
            Yextent.append(shape.bbox[3])
            for point in shape.points:
                # 每条线上的vertex的列表
                vertexInOneline.append(GISVertex(int(point[0]),int(point[1])))
            # 存储所有线的列表
            allLines.append(GISLine(vertexInOneline))

        for line in allLines:
            features.append(GISFeature(line,GISAttribute()))

        xMin = min(Xextent)
        yMin = min(Yextent)
        xMax = max(Xextent)
        yMax = max(Yextent)
        GISExtent_extent = GISExtent(GISVertex(xMin,yMin),GISVertex(xMax,yMax))
        GISLayer_layer = GISLayer(name,type,GISExtent_extent)

        for feature in features:
            GISLayer_layer.AddFeature(feature)

        return GISLayer_layer



    def readPolygon(self,shapes,type):
        return 
        
    def pointPattern(self,GISLayer_layer,minValue,xMin,yMin,xMax,yMax):
        extentArea = (xMax-xMin)*(yMax-yMin)
        Re = 0.5 /((GISLayer_layer.FeatureCount()/extentArea)**0.5)
        Ro = sum(minValue)/(GISLayer_layer.FeatureCount())
        return Re,Ro

    