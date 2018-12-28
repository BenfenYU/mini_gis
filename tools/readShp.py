import os,shapefile,copy
from .classes import *

class ReadSHP:
    def readshp(self,shp):
        name = os.path.splitext(shp)[0]
        # 读出二进制
        myshp = open(name+".shp", "rb")
        mydbf = open(name+".dbf" ,"rb")
        # 从二进制读shp对象
        sf = shapefile.Reader(shp=myshp,dbf=mydbf)
        # 图层
        layerType = sf.shapeType
        if layerType == 1 or layerType == 8:
            layer = self.readPoint(sf,layerType,name)
        elif layerType ==3:
            layer = self.readLine(sf,layerType,name)

        elif layerType == 5:
            layer = self.readPolygon(sf,layerType,name)
        else:
            return

        return layer

    def readPoint(self,sf,layerType,name):
        features = []
        # 每条字段的名称、类型等（竖）
        fieldKind = copy.deepcopy(sf.fields)
        fieldKind0 = fieldKind[0]
        del fieldKind[0]
        # 每个空间对象是一个列表，由一个大列表存放在recs中
        recs = sf.records()
        n = 0
        # 这里细化到组成每个空间对象的点
        for shape in sf.shapes():
            for point in shape.points:
                onePoint = SoloPoint(point[0],point[1])
                features.append(onePoint)
                n +=1
         
        layerExtent = sf.bbox
        # 这里的列表四个元素存储了两点的xy坐标，写成0113，结果范围出错。。。
        extent = Extent(SoloPoint(layerExtent[0],layerExtent[1]),\
        SoloPoint(layerExtent[2],layerExtent[3]))
        layer = Layer(layerType,features = features,\
        extent = extent)
        #layer.addAttriColumn(fieldKind)

        return layer

    def readLine(self,sf,layerType,name):
        allLines = []
        # 每条字段的名称、类型等（竖）
        fieldKind = copy.deepcopy(sf.fields)
        fieldKind0 = fieldKind[0]
        del fieldKind[0]
        # 每个空间对象是一个列表，由一个大列表存放在recs中
        recs = sf.records()
        n = 0

        for shape in sf.shapes():
            # 必须每次都清空！
            pointInOneline = []
            for point in shape.points:
                # 每条线上的vertex的列表
                pointInOneline.append(SoloPoint(point[0],point[1]))
            # 存储所有线的列表
            allLines.append(SoloLine(pointInOneline))

        layerExtent=sf.bbox
        extent = Extent(SoloPoint(layerExtent[0],layerExtent[1]),\
        SoloPoint(layerExtent[2],layerExtent[3]))
        layer = Layer(layerType,features = allLines,\
        extent = extent)
        #layer.addAttriColumn(fieldKind)

        return layer

    def readPolygon(self,sf,layerType,name):
        allPolygon = []
        # 每条字段的名称、类型等（竖）
        fieldKind = copy.deepcopy(sf.fields)
        fieldKind0 = fieldKind[0]
        del fieldKind[0]
        # 每个空间对象是一个列表，由一个大列表存放在recs中
        recs = sf.records()

        for shape in sf.shapes():
            pointPerPolygon = []
            for point in shape.points:
                for p in pointPerPolygon:
                    if SoloPoint(point[0],point[1]) == p:
                        pointPerPolygon.append(SoloPoint(point[0],point[1]))
                        allPolygon.append(SoloPolygon(pointPerPolygon))
                        pointPerPolygon = []

                pointPerPolygon.append(SoloPoint(point[0],point[1]))
            allPolygon.append(SoloPolygon(pointPerPolygon))

        layerExtent = sf.bbox
        extent = Extent(Point(layerExtent[0],\
        layerExtent[1]),Point(layerExtent[2],layerExtent[3]))
        layer = Layer(layerType,features = allPolygon,\
        extent = extent)#,deleteFlag = fieldKind0
        #layer.addAttriColumn(fieldKind)

        return layer

    def pointPattern(self,layer,minValue,xMin,yMin,xMax,yMax):
        extentArea = (xMax-xMin)*(yMax-yMin)
        Re = 0.5 /((layer.FeatureCount()/extentArea)**0.5)
        Ro = sum(minValue)/(layer.FeatureCount())
        return Re,Ro




