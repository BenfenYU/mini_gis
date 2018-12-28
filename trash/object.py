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

