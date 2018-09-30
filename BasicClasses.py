# coding : utf-8
import math
from PyQt5.QtCore import Qt,QRect,QPoint
from abc import ABCMeta, abstractmethod
from PyQt5.QtGui import QPainter, QPen
from Enum import enum

# ----------------------------------------------------------

class GISMapActions(enum):
    zoomin = 1
    zoomout = 2
    moveup = 3
    movedown = 4
    moveleft = 5
    moveright = 6


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

    def __init__(self,GISVertex_bottomleft,GISVertex_upright):
        self.GISVertex_bottomleft = GISVertex_bottomleft
        self.GISVertex_upright = GISVertex_upright
    
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
        newminx = self.GISVertex_bottomleft.x
        newminy = self.GISVertex_bottomleft.y
        newmaxx = self.GISVertex_upright.x
        newmaxy = self.GISVertex_upright.y

        

# ----------------------------------------------------------
class GISVertex:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
    
    def Distance(self,GISVertex_anothervertex):
        # 返回距离
        distance = math.sqrt((self.x-GISVertex_anothervertex.x)*(self.x - GISVertex_anothervertex.x)+pow((self.y-GISVertex_anothervertex.y),2));
        return distance;

# ------------------------------------------------------

class GISPoint(GISSpatial):
    def __init__(self,GISVertex_onevertex):
        self.GISVertex_centroid = GISVertex_onevertex
        self.GISExtent_extent = GISExtent(GISVertex_onevertex,GISVertex_onevertex)
    
    def draw(self,qwidget_obj,qp,GISView_view):
        Point_screenpoint = GISView_view.ToScreenPoint(self.GISVertex_centroid)
        pen = QPen(Qt.red, 10, Qt.SolidLine)
        qp.setPen(pen)
        size = qwidget_obj.size()
        qp.drawPoint(Point_screenpoint.x(), Point_screenpoint.y())
        #qp.drawRect(self.GISVertex_centroid.x, self.GISVertex_centroid.y,5,5)

    def Distance(self,GISVertex_anothervertex):
        return self.GISVertex_centroid.Distance(GISVertex_anothervertex)


class GISLine(GISSpatial):
    def __init__(self,List_allvertex):
        self.List_allvertex = List_allvertex
    
    def draw(self,qwidget_obj,qp,GISView_view):
        pen = QPen(Qt.black, 5, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.List_allvertex[0].x, self.List_allvertex[0].y,self.List_allvertex[1].x,self.List_allvertex[1].y)

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
    
    def Update(self,GISExtent_extent,Qrect_rectangle):
        self._GISExtent_currentmapextent = GISExtent_extent
        self._MapWindowSize = Qrect_rectangle
        self._MapMinX = self._GISExtent_currentmapextent.getMinX()
        self._MapMinY = self._GISExtent_currentmapextent.getMinY()
        # width和height属性待补充
        self._WinW = Qrect_rectangle.width()
        self._WinH = Qrect_rectangle.height()
        self._MapW = self._GISExtent_currentmapextent.getWidth()
        self._MapH = self._GISExtent_currentmapextent.getHeight()
        self._ScaleX = self._MapW/self._WinW
        self._ScaleY = self._MapH/self._WinH

    def ToScreenPoint(self,GISVertex_onevertex):
        ScreenX = (GISVertex_onevertex.x-self._MapMinX)/self._ScaleX
        ScreenY = self._WinH-(GISVertex_onevertex.y-self._MapMinY)/self._ScaleY
        point = QPoint(int(ScreenX),int(ScreenY))
        return point

    def ToMapVertex(self,Point_point):
        MapX = self._ScaleX * Point_point.x()+self._MapMinX
        MapY = self._ScaleY * (self._WinH-Point_point.y())+self._MapMinY
        return GISVertex(MapX,MapY)