# 有一个想法，记录在此，点、线、多边形类都是不可见的，在窗口处只能初始化一个layer，其他事情
# 都交给layer来做，即完全封装，点线多边形的类都是不可见的。

from .object import *

class GISLayer: # layer类建一个字典，全类的静态属性，用来存储不同的图层。所
    def __init__(self,name,SHAPETYPE_ShapeType,GISExtent_Extent,\
    deleteFlag = ()):
        self.name = name
        self.shapeType = SHAPETYPE_ShapeType
        self.GISExtent_Extent = GISExtent_Extent
        self.bool_DrawAttributeOrNot = False
        self.labelIndex = 0
        self.__GISFeature_Features = []
        self._attriColumn = []
        self.__deleteFlag = ()

    def draw(self,qwidget_obj,GISView_view,qp = None,\
    featureIndex = None):
        # 不同参数不同处理
        if isinstance(featureIndex,list):
            return
        elif featureIndex:
            self.__GISFeature_Features[featureIndex].\
            draw(qwidget_obj,GISView_view,self.bool_DrawAttributeOrNot,\
            qp,featureIndex)
            return 
        else:
            # 每个都画了
            for i in range(len(self.__GISFeature_Features)):
                self.__GISFeature_Features[i].draw(qwidget_obj,GISView_view,\
                self.bool_DrawAttributeOrNot,qp,self.labelIndex)
            #print(len(self.__GISFeature_Features))
            #self.__GISFeature_Features[1].draw(qwidget_obj,GISView_view,\
            #    self.bool_DrawAttributeOrNot,qp,color,thickness\
            #    ,self.labelIndex)

    def AddFeature(self,GISFeature_feature):
        self.__GISFeature_Features.append(GISFeature_feature)    

    def getFeature(self):
        return self.__GISFeature_Features

    def FeatureCount(self):
        return len(self.__GISFeature_Features)

    def addAttriColumn(self,listAttri):
        for attri in listAttri:
            self._attriColumn.append(attri)

    def getAttriColum(self):
        return self._attriColumn

    def distance(self,vertex):
        distanceList = []
        for feature in self.__GISFeature_Features:
            distanceList.append(feature.distance(vertex))
        
        return distanceList

    # m指明具体哪个feature，n指明使用枚举中的哪种颜色
    def setPen(self,m,n):
        self.__GISFeature_Features[m].spatialPen = QPen(Qt.GlobalColor(n),6)
        return 
    
    def __len__(self):
        return len(self.__GISFeature_Features)

    def __getitem__(self,index):
        return self.__GISFeature_Features[index]

    def __iter__(self):
        for feature in self.__GISFeature_Features:
            return feature

    def __bool__(self):
        return bool(self.__GISFeature_Features)

    def __index__(self,feature):
        return self.__GISFeature_Features.index(feature)

class GISFeature:
    def __init__(self,GISSpatial_spatialpart,GISAttribute_attribute):
        self.GISSpatial_spatialpart = GISSpatial_spatialpart
        self.GISAttribute_attribute = GISAttribute_attribute
        self.spatialPen = QPen(Qt.red,2)
        self.attriPen = QPen(Qt.gray,2)

    def draw(self,qwidget_obj,GISView_view,bool_DrawAttributeOrNot,qp\
    ,index):
        qp.begin(qwidget_obj)
        qp.setPen(self.spatialPen)
        self.GISSpatial_spatialpart.draw(qwidget_obj,GISView_view,qp,\
        index)
        qp.end()

        if bool_DrawAttributeOrNot:
            qp.begin(qwidget_obj)
            qp.setPen(self.attriPen)
            self.GISAttribute_attribute.draw(qwidget_obj,qp,GISView_view,\
            self.GISSpatial_spatialpart.GISVertex_centroid,index)
            qp.end()

    #def drawLine(self,qwidget_obj,qp,GISView_view,bool_DrawAttributeOrNot,index):
    #    self.GISSpatial_spatialpart.draw(qwidget_obj,qp,GISView_view)
    #    if bool_DrawAttributeOrNot:
    #        self.GISAttribute_attribute.draw(qwidget_obj,qp,GISView_view,self.GISSpatial_spatialpart.List_allvertex[0],index)

    def getAttribute(self,index):
        return self.GISAttribute_attribute.GetValue(index)
    
    def distance(self,vertex):
        return self.GISSpatial_spatialpart.distance(vertex)

    #def __repr__(self):
    #    return 
#
class GISView:

    def __init__(self,GISExtent_extent,Qrect_rectangle):
        self.Update(GISExtent_extent,Qrect_rectangle)

    def Update(self,GISExtent_extent,Qrectrectangle):
        self.GISExtent_currentmapextent = GISExtent_extent
        self.MapWindowSize = Qrectrectangle
        self.MapMinX = self.GISExtent_currentmapextent.getMinX()
        self.MapMinY = self.GISExtent_currentmapextent.getMinY()
        # widh和height属性待补充
        self.WinW = Qrectrectangle.width()-100
        self.WinH = Qrectrectangle.height()-10
        self.MapW = self.GISExtent_currentmapextent.getWidth()
        self.MapH = self.GISExtent_currentmapextent.getHeight()
        self.ScaleX = self.MapW/self.WinW
        self.ScaleY = self.MapH/self.WinH

    # 这里的转换有点有点多余，只要新建图层则必然要画，所以这个可以封装起来。
    def toScreenPoint(self,GISVertex_onevertex,pointOrNot = True):
        #print(GISVertex_onevertex.x)
        ScreenX = (GISVertex_onevertex.x-self.MapMinX)/self.ScaleX
        ScreenY = self.WinH-(GISVertex_onevertex.y-self.MapMinY)/self.ScaleY
        point = QPoint(int(ScreenX),int(ScreenY))
        if pointOrNot:
            return point

        return ScreenX,ScreenY

    #def toScreenVertex(self,onevertex):
    #    #print(GISVertex_onevertex.x)
    #    ScreenX = (onevertex.x-self.MapMinX)/self.ScaleX
    #    ScreenY = self.WinH-(onevertex.y-self.MapMinY)/self.ScaleY
    #    onevertex = GISVertex(ScreenX,ScreenY)



    def toMapVertex(self,vertex):
        MapX = self.ScaleX * (vertex.getX()-5)+self.MapMinX
        MapY = self.ScaleY * (self.WinH-(vertex.getY()-71))+self.MapMinY
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