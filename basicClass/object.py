from .basic import *
from PyQt5.QtCore import Qt,QRect,QPoint,QPointF,QLineF
from abc import ABCMeta, abstractmethod
from PyQt5.QtGui import QPainter, QPen,QPolygon,QPolygonF,QColor
from PyQt5.QtWidgets import  QGraphicsScene,QGraphicsLineItem,QGraphicsPolygonItem
from abc import ABCMeta, abstractmethod

class GISSpatial(metaclass = ABCMeta):
    def __init__(self,GISVertex_centroid,GISExtent_extent):
        self.GISVertex_centroid = GISVertex_centroid
        self.GISExtent_extent = GISExtent_extent

    @abstractmethod
    def draw(self,qp,GISView_view):
        return

    @abstractmethod
    def distance(self):
        return


class GISAttribute:
    def __init__(self,listValues = []):
        self.List_values = listValues

    def AddValue(self,object_attribute):
        self.List_values.append(object_attribute)

    def GetValue(self,index):
        return self.List_values[index]

    def draw(self,qwidget_obj,qp,GISView_view,GISVertex_location,index):
        Point_screenpoint = GISView_view.ToScreenPoint(GISVertex_location)
        qp.setPen(Qt.red)
        size = qwidget_obj.size()
        qp.drawText(QRect(Point_screenpoint.x(),Point_screenpoint.y()-40,80,30),Qt.AlignCenter,self.List_values[index])

class GISPoint(GISSpatial):
    def __init__(self,GISVertex_onevertex):
        self.GISVertex_centroid = GISVertex_onevertex
        self.GISExtent_extent = GISExtent(GISVertex_onevertex\
        ,GISVertex_onevertex)

    def draw(self,qwidget_obj,GISView_view,qp,index):
        Point_screenpoint = GISView_view.toScreenPoint\
        (self.GISVertex_centroid)
        r = QPoint(Point_screenpoint.x(), Point_screenpoint.y())
        #print(Point_screenpoint.x(), Point_screenpoint.y())
        # 用添加椭圆的方法画点
        qp.drawPoint(Point_screenpoint)

    def distance(self,vertex):
        return self.GISVertex_centroid.distance(vertex)

class GISLine(GISSpatial):
    def __init__(self,List_allvertex):
        self.List_allvertex = List_allvertex

    def draw(self,qwidget_obj,GISView_view,qp,index):
        qPoints = [GISView_view.toScreenPoint(vertex) 
        for vertex in self.List_allvertex]
        #print(self)
        #qPointsF = [qPoints) for qPoints in qPoints]
        qp.drawPolyline(QPolygon(qPoints))
        #for qLineF in qLineFsToScreenList:
        #    pen = QPen(color, thickness)
        #    qwidget_obj.scene.addLine(qLineF,pen)
        #    #pen = QPen(Qt.blue, 1, Qt.SolidLine)
        #    #qwidget_obj.scene.addLine(qLineF , pen)

    def distance(self,GISVertex_anothervertex):
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

    def __repr__(self):
        return 'Line object:From {} To {}'.format(str(self.List_allvertex[0]),\
        str(self.List_allvertex[-1]))

class GISPolygon(GISSpatial):
    def __init__(self,List_allvertex):
        self.List_allvertex = List_allvertex

    def draw(self,qwidget_obj,GISView_view,qp,\
    index):
        #qPolygonFsToScreen = GISView_view.toScreenPolygon(self.List_allvertex)
        points = [GISView_view.toScreenPoint(vertex,False) 
        for vertex in self.List_allvertex]
        # 必须转化为setPoints函数要求的参数格式
        pointxy = []
        for point in points:
            pointxy.append(point[0])
            pointxy.append(point[1])
        qPolygon = QPolygon()
        qPolygon.setPoints(pointxy)
        qp.drawPolygon(qPolygon)
            #pen = QPen(Qt.blue, 1, Qt.SolidLine)
            #qwidget_obj.scene.addLine(qLineF , pen)

        return

    def distance(self):
        return

