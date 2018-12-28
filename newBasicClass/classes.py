import math,sys,copy
sys.setrecursionlimit(10000000)
#from mainWindow.main_window import ZOOMIN,ZOOMOUT 
from collections import deque
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import Qt,QRect,QPoint,QPointF,QLineF,QRectF,pyqtSignal
ZOOMIN = 1
ZOOMOUT = 0

class PointToCanvasMixin:
    def toScreenPoint(point,view):
        point = view.toScreenPoint(point)
        point = point.pointToQpoint()

        return point

class LineToCanvasMixin:
    def lineToCanvas(line,canvas,view):
        newLine = []
        for point in line:
            x,y = point.toScreenPoint(canvas,view)
            newLine.append(SoloPoint(x,y))

        return SoloLine(newLine)

class MagicMethodsMixin:
    def __iter__(self):
        return iter(self.points)

    def __getitem__(self,posi):
        return self.points[posi]
    
    def __len__(self):
        return len(self.points)
    
    def __setitem__(self,key,value):
        # 这里鼻血指到self.points，直接self[key]，python不会调用__getitem__
        self.points[key] = value   
    
    def __eq__(self,other):
        return self.points == other.points
    
    def index(self,value):
        return self.points.index(value)

class SoloPoint(PointToCanvasMixin):
    def __init__(self,x,y):
        self.__x = float(round(x,8))
        self.__y = float(round(y,8))
    
    def inRectangle(self,polygon):
        maxx = max([polygon[0].x,polygon[3].x,polygon[2].x,polygon[1].x])
        minx = min([polygon[0].x,polygon[3].x,polygon[2].x,polygon[1].x])
        maxy = max([polygon[0].y,polygon[3].y,polygon[2].y,polygon[1].y])
        miny = min([polygon[0].y,polygon[3].y,polygon[2].y,polygon[1].y])

        if (minx<=self.x<=maxx and miny<=self.y<=maxy):
            return True
        else:
            return False
    
    def inPolygon2(self,polygon):
        px = self.x
        py = self.y
        flag = False
        j = -1

        for i in range(len(polygon)):
            sx = polygon[i].x
            sy = polygon[i].y
            tx = polygon[j].x
            ty = polygon[j].y

            # 与顶点重合
            if (self.dcmp(sx-px) and self.dcmp(sy-py))\
            or (self.dcmp(tx - px) and self.dcmp(ty- py)):
                return False
            
            # 线段俩端点是否在射线两侧
            if (sy<py and ty >= py) or\
            (sy >= py and ty < py):
                x = sx + (py - sy) * (tx - sx) / (ty - sy)
                if self.dcmp(x -px):
                    return False
                if x>px:
                    flag = not flag
            j = i

        return flag     
    
    def dcmp(self,x):
        if abs(x)<10**-5:
            return True
        else:
            False

    def onPolyLines(self,polygon):
        lines = polygon.lines()
        for l in lines:
            if self.onLine(l):
                return True
        return False
    
    def onLine(self,line):
        k = line.k
        b = line.b
        new = TwoPointLine(line[0],self)
        if abs(new.k-k)>=10**-4:
            return False
        if line[0].y <= self.x*k+b <= line[1].y\
        or line[1].y <= self.x*k+b <= line[0].y:
            return True
        return False
    
    def pointToQpointF(self):
        x = self.x
        y = self.y

        return QPointF(x,y)
    
    def pointToQpoint(self):
        x = self.x
        y = self.y

        return QPoint(x,y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
    
    @property
    def centroid(self):
        return (self.__x,self.__y)
    
    def __getitem__(self,position):
        return self.centroid[position]
    
    def __repr__(self):
        return 'SoloPoint:x={},y={}'.format(self.x,self.y)
    
    def __str__(self):
        return 'SoloPoint:x={},y={}'.format(self.x,self.y)
    
    def __eq__(self,other):
        return abs(self.__x - other.__x)<10**-4 and \
        abs(self.__y - other.__y)<10**-4
    
    def __hash__(self):
        return hash((self.__x,self.__y))

    def draw(self,qp,view = None,r = 1):
        if view:
            point = super().toScreenPoint(view)
        else :
            point = self.pointToQpoint()
        qp.drawPoint(point)

        return 

    def distance(self,point):
        # 返回距离
        distance = math.sqrt((self.x-point.x)**2\
        +pow((self.y-point.y),2))

        return distance
    
    def distanceToLine(self,line):
        A = k = line.k
        C = b = line.b
        B = -1
        x = self.x
        y = self.y
        dis = abs(A*x+B*y+C)/math.sqrt(A**2+B**2)

        return dis
    
    def pointLine(self,line):
        x = self.x
        y = self.y
        k = line.k
        b = line.b
        if (k*x+b)>y:
            n = -1
        elif (k*x+b)<y:
            n = 1
        else:
            n = 0

        return n 

class SoloLine(LineToCanvasMixin, MagicMethodsMixin):
    def __init__(self,points,extent= None):
        self.points = points
        self.__extent = extent

    @property
    def extent(self):
        if self.__extent:
            pass
        else:
            xList = [point.x for point in self]
            yList = [point.y for point in self]
            minX =min(xList)
            minY = min(yList)
            maxX = max(xList)
            maxY = max(yList)
            self.__extent= Extent(SoloPoint(minX,minY),\
            SoloPoint(maxX,maxY))
            
        return self.__extent 

    def draw(self,qp,view = None):
        if view:
            screenPoints = [(view.toScreenPoint(p)). 
            pointToQpointF() for p in self]
        else:
            screenPoints = [p.pointToQpointF() for p in self]
        
        [qp.drawLine(QLineF(screenPoints[i],screenPoints[i+1]))
        for i in range(len(screenPoints)-1)]

        return

    def slope(self):
        a = self[0]
        b = self[1]
        k = math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

        return k
    
    def b(self):
        k = self.slope()
        y = self[0].x
        x = self[0].y
        b = y-k*x

        return b

    def __repr__(self):
        return 'Line object:From {} To {}'.format(str(self.List_allvertex[0]),\
        str(self.List_allvertex[-1]))

    #def distance(self,GISVertex_anothervertex):
    #    # 补充点到直线的距离
    #    x1 = self.List_allvertex[0].x
    #    y1 = self.List_allvertex[0].y
    #    x2 = self.List_allvertex[1].x
    #    y2 = self.List_allvertex[1].y
    #    k1 = (y2-y1)/(x2-x1)
    #    k2 = -1/k1
    #    b1 = y1-k1*x1
    #    x3 = GISVertex_anothervertex.x
    #    y3 = GISVertex_anothervertex.y
    #    x4 = (k2* x3+b1-y3)/(k2-k1)
    #    y4 = k1 * x4 + b1
    #    distance = math.sqrt((y3-y4)**2+(x3-x4)**2)

    #    return distance
    
class SoloPolygon( MagicMethodsMixin):
    def __init__(self,points,clock = True):
        self.points = points
        self.clock = clock
    
    def lines(self):
        l = [TwoPointLine(self[m],self[m+1])
        for m in range(len(self)-1)]
        l = l+[TwoPointLine(self[-1],self[0])]

        return l

    def draw(self,qp,view,fill = None,width = 2):
        polygon = QtGui.QPolygon()
        for point in self:
            if view:
                screenPoint = point.toScreenPoint(view)
            else:
                screenPoint = point.pointToQpoint()
            polygon.append(screenPoint)
        qp.drawPolygon(polygon)
        
        return

    def distance(self):
        return

class TwoPointLine(LineToCanvasMixin, MagicMethodsMixin):

    directions = {'first':0,'second':1,'third':2,'fourth':3}

    def __init__(self,p1,p2):
        self.line = SoloLine([p1,p2])
        self.points = [p1,p2]
        self.vector = self._vector()
        self.length = self._length()
        self.direction = self._direction()
    
    # 线与多边形相交
    def interPolygon(self,polygon):
        lines = polygon.lines()
        for line in lines:
            if self.interPlace(line) or \
            (self[0].inPolygon(polygon) and \
            self[1].inPolygon(polygon)):
                return True
        return False
    
    # 两线相交
    def interPlace(self,line):
        k1 = self.k
        b1 = self.b
        k2 = line.k
        b2 = line.b
        if math.isnan(k1) or math.isnan(k2):
            # k2是k1不是nan
            if not math.isnan(k1):
                x = line[0].x
                minn = min([self[0].x,self[1].x])
                maxx = max([self[0].x,self[1].x])
                if (minn<=x and maxx>=x)\
                and ((TwoPointLine.getX(line[1].y,self)-x)\
                *(TwoPointLine.getX(line[0].y,self)-x)<=0):
                    return line.getIntersecNan(self)
            # k2不是nan
            elif not math.isnan(k2):
                x = self[0].x
                minn = min([line[0].x,line[1].x])
                maxx = max([line[0].x,line[1].x])
                if (minn<=x and maxx>=x)\
                and ((TwoPointLine.getX(self[1].y,line)-x)\
                *(TwoPointLine.getX(self[0].y,line)-x)<=0):
                    return self.getIntersecNan(line)
            # 俩都是nan
            else:
                x1 = self[0].x
                x2 = line[0].x
                minn1 = min([self[0].y,self[1].y])
                maxx1 = max([self[0].y,self[1].y])
                minn2 = min([line[0].y,line[1].y])
                maxx2 = max([line[0].y,line[1].y])
                if x1-x2>10**-5:
                    return False
                elif (minn1>= minn2 and maxx1<=maxx2) \
                or (minn2<=minn1<=maxx2)\
                or (minn2<=maxx1<=maxx2):
                    return  self[0]
                elif (minn1<= minn2 and maxx1>=maxx2):
                    return line[0]                    

        # 如果两个判断都等于0，则两个两点线有一个公共顶点
        if (self[0].x*k2+b2-self[0].y)*(self[1].x*k2+b2-self[1].y)<=0:
            if (line[0].x*k1+b1-line[0].y)*(line[1].x*k1+b1-line[1].y)<=0:
                return self.getIntersec(line)
        
        return False

    # 专门计算self是nan的交点    
    def getIntersecNan(self,other):
        b = other.b
        k = other.k
        x = self[0].x
        y = other.k*x+b
        return SoloPoint(x,y)
    
    @staticmethod
    def getX(y,other):
        k2 = other.k
        b2 = other.b
        if k2 ==0:
            return other[0].y
        if not math.isnan(k2):
            return (y-b2)/k2
    
    def _vector(self):
        p1 = self[0]
        p2 = self[1]
        return (p2.x-p1.x,p2.y-p1.y)
    
    def _length(self):
        return math.sqrt((self[0].x-self[1].x)**2\
        +(self[0].y-self[1].y)**2)

    def draw(self,canvas,view,r = 1,fill = 'red'):
        l = super().lineToCanvas(canvas,view)
        canvas.create_line(l[0][0],l[0][1],l[1][0],l[1][1],\
        fill =fill,width = r)

        return
    
    def tan(self,other):
        k1 = self.k
        k2 = other.k
        return abs((k2-k1)/(1+k1*k2))
    
    def cos(self,other):
        value = self.pMul(other)
        cos = value/(self.length*other.length)
        
        return cos

    def reverse(self):
        return TwoPointLine(self[1],self[0])
    
    # 叉积,判断柺向
    def xMul(self,other):
        vector1 = self.vector
        vector2 = other.vector
        value = vector1[0]*vector2[1]-vector1[1]*vector2[0]

        return value
    
    def pMul(self,other):
        v1 = self.vector
        v2 = other.vector
        value = v1[0] * v2[0] + v1[1] * v2[1]

        return value

    def _direction(self):
        v = self.vector
        if v[0]>0 and v[1]>0:
            return TwoPointLine.directions['first']
        elif v[0]<0 and v[1]>0:
            return TwoPointLine.directions['second']
        elif v[0]>0 and v[1]<0:
            return TwoPointLine.directions['fourth']
        else:
            return TwoPointLine.directions['third']


    @property
    def k(self):
        a = self[0]
        b = self[1]
        if (a.x-b.x) == 0:
            k = float('nan')
        else:
            k = (a.y-b.y)/(a.x-b.x)
        #try:
        #    k = (a.y-b.y)/(a.x-b.x)
        #except  BaseException:
        #    k = 100000

        return k
    
    @property
    def b(self):
        k = self.k
        x = self[0].x
        y = self[0].y
        b = y-k*x

        return b
    
    def parallel(self,d):
        k = self.k
        p1 = self[0]
        p2 = self[1]
        # op即otherpoint，生成的平行线的点
        delta = d/math.sqrt(k**2 + 1)
        # 上方线的两点
        op1 = SoloPoint(p1.x - k*delta,p1.y + delta)
        op2 = SoloPoint(p2.x - k*delta,p2.y + delta)
        # 下方线的两点
        op3 = SoloPoint(p1.x + k*delta,p1.y - delta)
        op4 = SoloPoint(p2.x + k*delta,p2.y - delta)
        line1 = TwoPointLine(op1,op2)
        line2 = TwoPointLine(op3,op4)
        # 判断向量的指向,向量指向左和右是不同的，
        # 上方线即为左边的，反之是右边的，按照此顺序返回
        if self.vector[0]>=0:
            return (line1,line2)
        elif self.vector[0] < 0:
            return (line2,line1)

    # 返回两线的交点，不一定在线上
    def getIntersec(self,otherLine):
        k1 = self.k
        k2 = otherLine.k
        b1 = self.b
        b2 = otherLine.b
        if k2 == k1:
            x = (self[1].x+otherLine[0].x)/2
            y = (self[1].y+otherLine[0].y)/2
        else:
            x = (b2 - b1)/(k1 - k2)
            y = x*k1+b1

        return SoloPoint(x,y)
    
    def __repr__(self):
        return 'SoloLine:第一点：{}，第二点：{}'.format(self[0],self[1])

# layer类建一个字典，全类的静态属性，用来存储不同的图层。所
class Layer:
    def __init__(self,shapeType,features ,extent=None,\
    deleteFlag = None,name = None):
        self.name = name
        self.shapeType = shapeType
        self.bool_DrawAttributeOrNot = False
        self.labelIndex = 0
        self.features = features
        self.attriColumn = []
        self.deleteFlag = deleteFlag
        self.__extent = extent

    def draw(self,qp,view):
        for feature in self:
            feature.draw(qp,view)
        
        return
        
    def kMean(self,classNum = 3,iterNum = 50):
        kMeanObj = KMeans(self,classNum,iterNum)
        classIndex,classResult,returnValue = kMeanObj.startK()

        return returnValue

    def AddFeature(self,GISFeature_feature):
        self.GISFeature_Features.append(GISFeature_feature)    

    def getFeature(self):
        return self.GISFeature_Features

    def FeatureCount(self):
        return len(self.GISFeature_Features)

    def addAttriColumn(self,listAttri):
        for attri in listAttri:
            self._attriColumn.append(attri)

    def getAttriColum(self):
        return self._attriColumn

    def distance(self,vertex):
        distanceList = []
        for feature in self.GISFeature_Features:
            distanceList.append(feature.distance(vertex))
        
        return distanceList
    
    @property
    def extent(self):
        if self.__extent:
            pass
        elif self.shapeType == 3:
            linesExtent = [l.extent for l in self]
            self.__extent = Extent.getMultiExtent(linesExtent)
        elif self.shapeType == 1:
            xList = [point.x for point in self]
            yList = [point.y for point in self]
            minX =min(xList)
            minY = min(yList)
            maxX = max(xList)
            maxY = max(yList)
            self.__extent= Extent(SoloPoint(minX,minY),\
            SoloPoint(maxX,maxY))
        else:
            pass
        
        return self.__extent       

    def __len__(self):
        return len(self.GISFeature_Features)

    def __getitem__(self,index):
        return self.GISFeature_Features[index]

    def __iter__(self):
        # 返回一个迭代器对象
        return iter(self.features)

    def __bool__(self):
        return bool(self.GISFeature_Features)

    def __index__(self,feature):
        return self.GISFeature_Features.index(feature)

class Attribute:
    def __init__(self,values = []):
        self.values = values

    def AddValue(self,object_attribute):
        self.List_values.append(object_attribute)

    def GetValue(self,index):
        return self.List_values[index]

    def draw(self,qwidget_obj,qp,GISView_view,GISVertex_location,index):
        Point_screenpoint = GISView_view.ToScreenPoint(GISVertex_location)
        qp.setPen(Qt.red)
        size = qwidget_obj.size()
        qp.drawText(QRect(Point_screenpoint.x(),Point_screenpoint.y()-40,80,30),Qt.AlignCenter,self.List_values[index])

class View:

    def __init__(self,extent,rectangle):
        self.update(extent,rectangle)

    def update(self,extent,rectangle):
        self.currentMapExtent = extent
        self.windowSize = rectangle
        self.mapMinX = self.currentMapExtent.minX
        self.mapMinY = self.currentMapExtent.minY
        # widh和height属性待补充
        self.winW = rectangle.width()
        self.winH = rectangle.height()
        self.mapW = self.currentMapExtent.width
        self.mapH = self.currentMapExtent.height
        self.scaleX = self.mapW/self.winW
        self.scaleY = self.mapH/self.winH

    # 这里的转换有点有点多余，只要新建图层则必然要画，所以这个可以封装起来。
    def toScreenPoint(self,point,pointOrNot = True):
        screenX = (point.x-self.mapMinX)/self.scaleX
        screenY = self.winH-(point.y-self.mapMinY)/self.scaleY

        return SoloPoint(screenX,screenY)

    def toMapPoint(self,point):
        MapX = self.scaleX * (point.x)+self.mapMinX
        MapY = self.scaleY * (self.winH-(point.y))+self.mapMinY
        return SoloPoint(MapX,MapY)

    def changeView(self,action,*args):
        point = self.toMapPoint(SoloPoint(args[0],args[1]))
        # 改变范围
        self.currentMapExtent=self.currentMapExtent.changeExtent(action,point)
        # 更新view的各比例
        self.update(self.currentMapExtent,self.windowSize)

    #def UpdateExtent(self,extent):
    #    self.currentMapExtent.copyFrom(extent)
    #    self.Update(self.currentMapExtent,self.MapWindowSize)

    # 这是个错误示范，self.GISExtent是引用变量，指向地址，不直接存储值大小，多个变量指向同一地址，修改一次，所有变量指向的值都会发生变化
    # def reView(self):
    #    GISView.now_pointer -=1
    #    self.GISExtent_currentmapextent = GISView.action_record[GISView.now_pointer]
    #    print(self.GISExtent_currentmapextent.GISVertex_upright.x)
    #    print(GISView.now_pointer)
    #    self.Update(self.GISExtent_currentmapextent,self.MapWindowSize)

class Extent:

    ZoomingFactor = 1.1
    MovingFactor = 0.25

    action_record = [[0,0,100,100]]
    now_pointer = 0

    def __init__(self,bottomLeft=SoloPoint(-180,-90)\
    ,upRight = SoloPoint(180,90)):
        self.bottomLeft = bottomLeft
        self.upRight = upRight
        self.__minX = bottomLeft.x
        self.__minY = bottomLeft.y
        self.__maxX = upRight.x
        self.__maxY = upRight.y
    
    @staticmethod
    def getMultiExtent(extents):
        blx = [e.bottomLeft.x for e in extents]
        bly = [e.bottomLeft.y for e in extents]
        upx = [e.upRight.x for e in extents]
        upy = [e.upRight.y for e in extents]

        return Extent(SoloPoint(min(blx),min(bly))\
        ,SoloPoint(max(upx),max(upy)))

    @property
    def minX(self):
        return self.__minX

    @property
    def maxX(self):
        return self.__maxX

    @property
    def maxY(self):
        return self.__maxY

    @property
    def minY(self):
        return self.__minY

    @property
    def width(self):
        return self.__maxX-self.__minX

    @property
    def height(self):
        return self.__maxY-self.__minY

    def changeExtent(self,action,point):
        w =self.__maxX-self.__minX
        h =self.__maxY-self.__minY 
        xs = point.x/w
        ys = point.y/h
        if action == ZOOMIN:
            newWidth = w/Extent.ZoomingFactor
            newHeight =h/Extent.ZoomingFactor
        elif action == ZOOMOUT:
            newWidth = w*Extent.ZoomingFactor
            newHeight =h*Extent.ZoomingFactor
        minx = point.x-newWidth*xs
        maxx = point.x+newWidth*(1-xs)
        miny = point.y-newHeight*ys
        maxy = point.y+newHeight*(1-ys)

        nl = SoloPoint(minx,miny)
        nr = SoloPoint(maxx,maxy)
        newExtent = Extent(nl,nr)

        return newExtent


    def zoomin(self):
        newminx = ((self.minX+self.maxX)-self.width/self.ZoomingFactor) /2
        newminy = ((self.minY+self.maxY)-self.height/self.ZoomingFactor) /2
        newmaxx = ((self.minX+self.maxX)+self.width/self.ZoomingFactor) /2
        newmaxy = ((self.minY+self.maxY)+self.height/self.ZoomingFactor) /2

        return SoloPoint(newminx,newminy),SoloPoint(newmaxx,newmaxy)

    def zoomout(self):
        newminx = ((self.minX+self.maxX)-self.width*self.ZoomingFactor) /2
        newminy = ((self.minY+self.maxY)-self.height*self.ZoomingFactor) /2
        newmaxx = ((self.minX+self.maxX)+self.width*self.ZoomingFactor) /2
        newmaxy = ((self.minY+self.maxY)+self.height*self.ZoomingFactor) /2

        return SoloPoint(newminx,newminy),SoloPoint(newmaxx,newmaxy)

    def copyFrom(self,extent):
        self.upRight.copyFrom(extent.upRight)
        self.bottomLeft.copyFrom(extent.bottomLeft)

class Buffer(LineToCanvasMixin):

    # 返回平行线和多边形半圆弧构成的多边形，逆时针存储
    def para(self,p1,p2,d = 5):
        line = TwoPointLine(p1,p2)
        k = line.k
        # 斜率无穷
        if math.isnan(k):
            op1 = SoloPoint(p1.x+d,p1.y)
            op2 = SoloPoint(p2.x+d,p2.y)
            op3 = SoloPoint(p1.x-d,p1.y)
            op4 = SoloPoint(p2.x-d,p2.y)
        else:
            # op即otherpoint，生成的平行线的点
            delta = d/math.sqrt(k**2 + 1)
            # 上方线的两点
            op1 = SoloPoint(p1.x - k*delta,p1.y + delta)
            op2 = SoloPoint(p2.x - k*delta,p2.y + delta)
            # 下方线的两点
            op3 = SoloPoint(p1.x + k*delta,p1.y - delta)
            op4 = SoloPoint(p2.x + k*delta,p2.y - delta)

        polygon = SoloPolygon([op1,op2,op4,op3],clock = None)

        def pDistance1(point):
            return point.distance(op1)
        def pDistance2(point):
            return point.distance(op2)
        def pDistance3(point):
            return point.distance(op3)
        def pDistance4(point):
            return point.distance(op4)

        # 原始线上p1和p2圆周上的点
        rPoints1 = self.randomCircular(p1)
        rPoints2 = self.randomCircular(p2)

        # 剔除圆周上不合适的点
        okPoints1 = []
        okPoints2 = []
        for i in range(len(rPoints1)):
            if not rPoints1[i].inRectangle(polygon):
                okPoints1.append(rPoints1[i])
            if not rPoints2[i].inRectangle(polygon):
                okPoints2.append(rPoints2[i])

        okPoints1 = [okPoints1[0]]
        okPoints2 = [okPoints2[0]]

        # 构造点逆时针排列的多边形
        if line.vector[0] > 0 or \
        (math.isnan(k) and line.vector[1]<0):
            okPoints1.sort(key = pDistance1)
            okPoints2.sort(key = pDistance4)
            finalPoints = [op1]+okPoints1+[op3,op4]+okPoints2+[op2]
        elif line.vector[0] < 0 or\
        (math.isnan(k) and line.vector[1]>0):
            okPoints1.sort(key = pDistance3)
            okPoints2.sort(key = pDistance2)
            finalPoints = [op1,op2]+okPoints2+[op4,op3]+okPoints1
        finalPolygon = SoloPolygon(finalPoints,clock=False)

        return finalPolygon
        
    def buffer(self,layer,r = 5):
        self.r = r

        if layer.shapeType == 1:
            polygon = []
            points = [SoloPoint(120,20),SoloPoint(125,21)]
            for point in points:#layer.features:
                pPolygon = SoloPolygon(self.randomCircular(point,num = 10))
                polygon.append(pPolygon)
            allBuffer= self.polyInter(polygon)
        
        elif layer.shapeType == 3:
            paraPolygons = []
            for lineP in layer:
                # 每相邻的俩点做平行线，返回一多边形列表
                allPara = [self.para(lineP[i],lineP[i+1],r)
                for i in range(len(lineP)-1)]
                paraPolygons+=allPara
            allBuffer = self.polyInter(paraPolygons)
        
        elif layer.shapeType == 5:
            pass

        bufferLayer = Layer(5,allBuffer)
        
        return bufferLayer

    def polyInter(self,paraPolygons):

        allBuffer = []
        copyPara = copy.deepcopy(paraPolygons)
        okP = []
        pIndexes = []
        for polygon in paraPolygons:
            polygonIndex = paraPolygons.index(polygon)
            polyLines = polygon.lines()
            nowPolygon = copyPara[polygonIndex]
            # 每条线段为一个扫描单位
            for polyline in polyLines:

                #polyline.draw(canvas,view,r = 4)
                
                # 构造扫描条带
                scanXmin = min([polyline[0].x,polyline[1].x])
                scanXmax = max([polyline[0].x,polyline[1].x])
                # 找有哪些线经过或在条带中，并判断哪些线是原本该缓冲区的线，
                # 然后判断和line是否有交点
                linesInScan = []
                bufferInScan = []
                # 循环所有线，判断是否在矩形区域内
                for spolygon in paraPolygons:
                    if spolygon == polygon:
                        continue
                    spolyLines = spolygon.lines()
                    for sline in spolyLines:
                        if (math.isnan(sline.k) or\
                        math.isnan(polyline.k)):
                            if not sline.interPlace(polyline):
                                continue
                        else:
                            minn = min([sline[0].x,sline[1].x])
                            maxx = max([sline[0].x,sline[1].x])
                            # 如果线经过条幅或者在条幅以内
                            if not ((scanXmin >= minn and \
                            maxx >= scanXmax)\
                            or (scanXmin <= sline[0].x <= scanXmax)\
                            or (scanXmin <= sline[1].x <= scanXmax)\
                            or (scanXmin <= minn and \
                            maxx <= scanXmax)):
                                continue
                        linesInScan.append(sline)
                        if spolygon in bufferInScan:
                            continue
                        bufferInScan.append(spolygon)
                
                # 条带中没有其他线经过，则进入下一个扫描条带
                if not linesInScan:
                    continue
                # 对于所有经过矩形区域的非本缓冲区的线
                for sline in linesInScan:
                    p = sline.interPlace(polyline)
                    pIndex = []
                    if not p:
                        continue
                    # okp中不重复添加p
                    if p in okP:
                        def distanceP(point):
                            return nowPolygon[index0]\
                            .distance(point)
                        indexOfp = okP.index(p)
                        pIndexes[indexOfp].append(nowPolygon)

                        index0 = nowPolygon\
                        .index(polyline[0])
                        index1 = nowPolygon\
                        .index(polyline[1])
                        if p==polyline[0] :
                            p = polyline[0]
                        elif p==polyline[1]:
                            p = polyline[1]
                        else:
                            # 这里本应是不需要判断的，但是为啥不行呢？？？
                            if p not in nowPolygon.points:
                                nowPolygon.points.insert(index1,p)
                                # 如果是最后一条线，插入的时候就要小心了
                                if p.x==55.0:
                                    pass
                                if polyline == polyLines[-1]:
                                    #要知道polyline在nowpolygon中的起始点位置
                                    index0 = -1

                                a = nowPolygon[index0+1:index1+1]
                                a.sort(key = distanceP)
                                nowPolygon[index0+1:index1+1] = a
                        # 如果p已经有了,就不必再向下，直接插入和记录即可
                        continue
                    #p.draw(canvas,view,4)
                    
                    for scanPoly in bufferInScan:
                        # 如果在多边形内，就丢掉
                        if p.inPolygon2(scanPoly):
                            break
                        # 如果在最后一轮还没丢掉，说明不在多边形内
                        index = bufferInScan.index(scanPoly)
                        if index == len(bufferInScan)-1:
                            def distanceP(point):
                                return nowPolygon[index0]\
                                .distance(point)
                            # 记录下p在哪个多边形内
                            pIndex.append(nowPolygon)

                            #p.draw(canvas,view,r = 5)
                            pIndexes.append(pIndex)
                            # p.draw(canvas,view,r = 6)

                            index0 = nowPolygon\
                            .index(polyline[0])
                            index1 = nowPolygon\
                            .index(polyline[1])
                            if p==polyline[0] :
                                p = polyline[0]
                            elif p==polyline[1]:
                                p = polyline[1]
                            else:
                                if p not in nowPolygon.points:
                                    nowPolygon.points.insert(index1,p)
                                    # 如果是最后一条线，插入的时候就要小心了
                                    if polyline == polyLines[-1]:
                                        #要知道polyline在nowpolygon中的起始点位置
                                        index0 = -1

                                    a = nowPolygon[index0+1:index1+1]
                                    a.sort(key = distanceP)
                                    nowPolygon[index0+1:index1+1] = a

                            okP.append(p)
                        
        # 画轮廓线
        finalBuffers = []
        finishedP = []

        kps = 0

        while True:
            kps+=1
            finalBuffer = []
            minusOkP = [i for i in okP if i not in finishedP]
            if minusOkP:
                p = minusOkP[0]
            else:
                break
            index = okP.index(p)
            pPolygons = pIndexes[index]

            kps1 = 0
            while True:
                #p.draw(canvas,view,r = 10)

                kps1 +=1
                finalBuffer.append(p)
                if p in okP:
                    if p in finishedP:
                        finalBuffers.append(finalBuffer)
                        break
                    pNum = okP.index(p)
                    pPolygons = pIndexes[pNum]
                    finishedP.append(p)
                    # 判断哪条路在右
                    aLines = []

                    kpppppp=0
                    for pPolygon in pPolygons:

                        kpppppp+=1
                        index = pPolygon.index(p)
                        if index == len(pPolygon)-1:
                            index = -1
                        #pPolygon.draw(canvas,view,fill = 'green')
                        aPoint = pPolygon[index+1]   
                        #if kps==1 and kps1==1 and kpppppp==2:
                        #    p.draw(canvas,view,r = 7)
                        #    aPoint.draw(canvas,view,r = 5)
                            #return    
                            #pPolygon.draw(canvas,view,fill = 'green')                              
                        #aPoint.draw(canvas,view,4)
                        aLine = TwoPointLine(p,aPoint)
                        #aLine.draw(canvas,view,r = 8,fill = 'black')
                        aLines.append(aLine)
                    rightIndex = Buffer.whoIsRight(aLines)
                    rightPoly = pPolygons[rightIndex]
        

                indexOfp = rightPoly.index(p)
                if indexOfp == len(rightPoly)-1:
                    indexOfp = -1
                p = rightPoly[indexOfp+1]
            #return
            
            [allBuffer.append(SoloPolygon(b)) for b in finalBuffers]
        
        return allBuffer 

    def randomCircular(self,centroid,num = 15):
        # 圆周上均匀产生一些点
        angle = 360//num*math.pi/180
        pnum = (num-2)//2
        cx = centroid.x
        cy = centroid.y
        pointUp = SoloPoint(cx,cy+self.r)
        pointDown = SoloPoint(cx,cy-self.r)
        points1 = [pointUp]
        points2 = [pointDown]
        nowAngle = 0
        for i in range(pnum):
            nowAngle += angle
            k = 1/math.tan(nowAngle)
            b = cy-k*cx
            p1,p2 = self.lineCircle(centroid,k,b)
            points1.append(p1)
            points2.append(p2)
        points = points1+points2

        return points
    
    def lineCircle(self,centroid,k,b):
        x1 = centroid.x
        y1 = centroid.y
        A = 1+k**2
        B = 2*(k*b-x1-k*y1)
        C = x1**2+b**2+y1**2-2*y1*b-self.r**2
        px = (-B+math.sqrt(B**2-4*A*C))/(2*A)
        nx = (-B-math.sqrt(B**2-4*A*C))/(2*A)
        py = px*k+b
        ny = nx*k+b

        return SoloPoint(px,py),SoloPoint(nx,ny)      

    @staticmethod
    def whoIsRight(vectors):
        n = 1
        vector = vectors[0]
        while True:
            if n == len(vectors):
                return vectors.index(vector)
            value = vector.xMul(vectors[n])
            # 大于0，其vector1就在右边
            if value>=0:
                pass
            else:
                vector = vectors[n]
            n += 1

class MergeMixin():
    def merge(self,polygon):
        for selfPoint in self:
            # 找到和point相等的点
            for point in polygon:
                if selfPoint == point:
                    copyPolygon = copy.deepcopy(polygon)
                    newPolygon = copy.deepcopy(self)
                    selfIndex = self.index(selfPoint)
                    pointIndex = polygon.index(point)
                    eqList = deque([(selfIndex,pointIndex)])
                    try:
                        n = 0
                        while 1:
                            selfIndex+=1
                            pointIndex-=1
                            if self[selfIndex] == polygon[pointIndex]:
                                eqList.append((selfIndex,pointIndex))
                            else:
                                break
                        selfIndex = self.index(selfPoint)
                        pointIndex = polygon.index(point)
                        while 2:
                            selfIndex-=1
                            pointIndex+=1 
                            if self[selfIndex] == polygon[pointIndex]:
                                eqList.appendleft((selfIndex,pointIndex))
                            else:
                                break
                        if len(eqList)==1:
                            return
                    except expression as identifier:
                        pass
                    finally:
                        
                        return