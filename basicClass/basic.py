from enum import Enum
import math

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

class GISVertex:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;

    def distance(self,pointTuple):
        # 返回距离
        distance = math.sqrt((self.x-pointTuple[0])*(self.x - pointTuple[0])+pow((self.y-pointTuple[1]),2));
        return distance;

    def copyFrom(self,GISVertex_v):
        self.x = GISVertex_v.x
        self.y = GISVertex_v.y
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y


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