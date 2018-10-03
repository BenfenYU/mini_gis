# coding : utf-8
import math
from PyQt5.QtCore import Qt,QRect,QPoint
from abc import ABCMeta, abstractmethod
from PyQt5.QtGui import QPainter, QPen
from enum import Enum

# ----------------------------------------------------------

class GISMapActions(Enum):
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
    MovingFactor = 0.25

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
        switch = {
            GISMapActions.zoomin:self.zoomin(),
            GISMapActions.zoomout:self.zoomout(),
            GISMapActions.moveup:self.moveup(),
            GISMapActions.movedown:self.movedown(),
            GISMapActions.moveleft:self.moveleft(),
            GISMapActions.moveright:self.moveright(),
        }
        switch[GISMapActions_action]
        self.GISVertex_upright.x = newmaxx
        self.GISVertex_upright.y = newmaxy
        self.GISVertex_bottomleft.x = newminx
        self.GISVertex_bottomleft.y = newminy
        
    
    def zoomin(self):
        newminx = ((self.getMinX()+self.getMaxX())-self.getWidth()/GISExtent.ZoomingFactor) /2
        newminy = ((self.getMinY()+self.getMaxY())-self.getHeight()/GISExtent.ZoomingFactor) /2
        newmaxx = ((self.getMinX()+self.getMaxX())+self.getWidth()/GISExtent.ZoomingFactor) /2
        newmaxy = ((self.getMinY()+self.getMaxY())+self.getHeight()/GISExtent.ZoomingFactor) /2      

    def zoomout(self):
        newminx = ((self.getMinX()+self.getMaxX())-self.getWidth()*GISExtent.ZoomingFactor) /2
        newminy = ((self.getMinY()+self.getMaxY())-self.getHeight()*GISExtent.ZoomingFactor) /2
        newmaxx = ((self.getMinX()+self.getMaxX())+self.getWidth()*GISExtent.ZoomingFactor) /2
        newmaxy = ((self.getMinY()+self.getMaxY())+self.getHeight()*GISExtent.ZoomingFactor) /2

    def moveup(self):
        newminy = self.getMinY()-self.getHeight()* GISExtent.MovingFactor
        newmaxy = self.getMaxY()-self.getHeight()* GISExtent.MovingFactor

    def movedown(self):
        newminy = self.getMinY() + self.getHeight() * GISExtent.MovingFactor
        newmaxy = self.getMaxY()+self.getHeight() * GISExtent.MovingFactor

    def moveleft(self):
        newminx = self.getMinX() + self.getWidth() * GISExtent.MovingFactor
        newmaxx = self.getMaxX()+self.getWidth() * GISExtent.MovingFactor

    def moveright(self):
        newminx = self.getMinX() - self.getWidth() * GISExtent.MovingFactor
        newmaxx = self.getMaxX()-self.getWidth() * GISExtent.MovingFactor
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
        ScreenX = (GISVertex_onevertex.x-self.MapMinX)/self.ScaleX
        ScreenY = self.WinH-(GISVertex_onevertex.y-self.MapMinY)/self.ScaleY
        point = QPoint(int(ScreenX),int(ScreenY))
        return point

    def ToMapVertex(self,Point_point):
        MapX = self.ScaleX * Point_point.x()+self.MapMinX
        MapY = self.ScaleY * (self.WinH-Point_point.y())+self.MapMinY
        return GISVertex(MapX,MapY)

    def ChangeView(self,GISMapActions_action):
        self.GISExtent_currentmapextent.ChangeExtent(GISMapActions_action)
        self.Update(self.GISExtent_currentmapextent,self.MapWindowSize)