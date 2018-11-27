import os,shapefile,copy
from .layer import * 

class GISShapefile:
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
            QMessageBox.information(self,'提示','暂时不支持，请升级后再来。')

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
                onePoint = GISPoint(GISVertex(point[0],point[1]))
                onefeature = GISFeature(onePoint,GISAttribute(recs[n]))
                features.append(onefeature)
                n +=1
        print(len(features))       
        layerExtent = sf.bbox
        # 这里的列表四个元素存储了两点的xy坐标，写成0113，结果范围出错。。。
        GISExtent_extent = GISExtent(GISVertex(layerExtent[0],layerExtent[1]),GISVertex(layerExtent[2],layerExtent[3]))
        GISLayer_layer = GISLayer(name,layerType,GISExtent_extent,fieldKind0)
        GISLayer_layer.addAttriColumn(fieldKind)

        for feature in features:
            GISLayer_layer.AddFeature(feature)

        return GISLayer_layer#,Re,Ro

    def readLine(self,sf,layerType,name):
        vertexInOneline = []
        allLines = []
        features = []

        for shape in sf.shapes():
            for point in shape.points:
                # 每条线上的vertex的列表
                vertexInOneline.append(GISVertex(int(point[0]),int(point[1])))
            # 存储所有线的列表
            allLines.append(GISLine(vertexInOneline))

        for line in allLines:
            features.append(GISFeature(line,GISAttribute()))

        layerExtent = sf.bbox
        GISExtent_extent = GISExtent(GISVertex(layerExtent[0],layerExtent[1]),GISVertex(layerExtent[2],layerExtent[3]))
        GISLayer_layer = GISLayer(name,layerType,GISExtent_extent)

        for feature in features:
            GISLayer_layer.AddFeature(feature)

        return GISLayer_layer


    def readPolygon(self,sf,layerType,name):
        vertexPerPolygon = []
        allPolygon = []
        features = []

        for shape in sf.shapes():
            for point in shape.points:
                vertexPerPolygon.append(GISVertex(int(point[0]),int(point[1])))

            allPolygon.append(GISPolygon(vertexPerPolygon))

        for polygon in allPolygon:
            features.append(GISFeature(polygon,GISAttribute()))

        layerExtent = sf.bbox
        GISExtent_extent = GISExtent(GISVertex(layerExtent[0],layerExtent[1]),GISVertex(layerExtent[2],layerExtent[3]))
        GISLayer_layer = GISLayer(name,layerType,GISExtent_extent)

        for feature in features:
            GISLayer_layer.AddFeature(feature)

        return GISLayer_layer

    def pointPattern(self,GISLayer_layer,minValue,xMin,yMin,xMax,yMax):
        extentArea = (xMax-xMin)*(yMax-yMin)
        Re = 0.5 /((GISLayer_layer.FeatureCount()/extentArea)**0.5)
        Ro = sum(minValue)/(GISLayer_layer.FeatureCount())
        return Re,Ro
