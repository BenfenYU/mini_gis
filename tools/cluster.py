import copy,random,sys
import numpy as np
from collections import deque
from basicClass import basic

class KMeans:

    def __init__(self,layer,num,iterNum,view = None):
        self.num = num
        self.layer = layer
        self.iterNum = iterNum
    
    def startK(self):
        featureNum = len(self.layer)
        # 随机产生分类
        randomIndex = [random.randint(0,featureNum) 
        for _ in range(self.num)]
        
        k = 0
        while k < self.iterNum:
            randomIndex ,classResult= self.iters(randomIndex,featureNum)
            k += 1
        
        return randomIndex,classResult,1
    
    def iters(self,random,featureNum):
        randomIndex = random
        result = np.array([])
        # 每个类代表点的索引
        for index in randomIndex:
            # 计算每个点到随机点的距离
            distance = np.array(self.layer.distance(self.layer[index]\
            .GISSpatial_spatialpart.GISVertex_centroid))
            # 存储在result的二维数组中，方便下步比较
            result = np.concatenate((result,distance))
        # 每次把距离计算结果接在result里面，然后再reshape和transpose
        result = result.reshape(len(randomIndex),len(distance))
        result = result.transpose()
        #print(result.shape)
        # 存储分了n类后各类的点
        resultTag = []
        # 分类的结果，即每个点属于哪个类
        classResult = []
        for _ in range(len(randomIndex)):
            resultTag.append([])
        for m in range(len(result)):
            # 求得每个点距离哪个点最近，设置其颜色，分成n类并存储相对索引
            minIndex = np.where(result[m]==min(result[m]))[0]
            self.layer.setPen(m,minIndex+6)
            # resultTag是n维列表，存储各类各自的对象的索引
            resultTag[int(minIndex)].append(m)
            classResult.append((m,minIndex))
        
        randomIndex = self.findCenter(resultTag)
        
        # 返回的是新的类的中心点，然后接着循环
        return randomIndex,classResult

    def findCenter(self,resultTag):
        newKindIndex = []
        averageCenter = []

        # 平均值求中心
        for kind in resultTag:
            sumX = 0
            sumY = 0
            # 把一类的所有点的坐标求均值
            for kindIndex in kind:
                sumX += self.layer[kindIndex].GISSpatial_spatialpart.\
                GISVertex_centroid.getX()
                sumY += self.layer[kindIndex].GISSpatial_spatialpart.\
                GISVertex_centroid.getY()
            averageX = sumX / len(kind)
            averageY = sumY / len(kind)
            averageCenter.append((averageX,averageY))

        # 求各点到中心的距离
        count = 0
        for kind in resultTag:
            distances = []
            for kindIndex in kind:
                vertex = basic.GISVertex(averageCenter[count][0],\
                averageCenter[count][1])
                distances.append(self.layer[kindIndex].\
                distance(vertex))
            minDistance = min(distances)
            minIndex = distances.index(minDistance)
            # kind里面是真正的feature索引
            minRealIndex = kind[minIndex]
            newKindIndex.append(minRealIndex)
            count += 1
        
        return newKindIndex

class DBScan:
    def __init__(self,layer,r =200 ,minPts = 4,view = None):
        self.r = r
        self.minPts = minPts   
        self.layer = layer
        self.view = view
    
    def findKernal(self):
        s = 1
        length = len(self.layer)
        # 所有的点由经纬度转换为屏幕坐标
        vertexes = []
        for vertex in \
        [self.layer[i].GISSpatial_spatialpart.GISVertex_centroid
        for i in range(length)]:
            vertexes.append(self.view.toScreenVertex(vertex))

        # 核心点和核心点r范围里的点
        kernalPts = []
        # 这是个二维列表
        kernalSons = []
        # 用于把kernalSons中的列表拆成一个个元素
        breakKernalSons=[]
        # 遍历所有点，找核心点
        for vertex in vertexes:
            # 当前点的索引
            vertexIndex = vertexes.index(vertex)
            ptNum = 0
            # 与图层所有点的距离
            distances = self.layer.distance(vertex)
            # 存放该核心点周围的附从点
            distancesIndex = []
            for distance in distances:
                # 如果距离在r以内且不为0，即不是自己本身，
                if distance < self.r and distance != 0:
                    # 记下符合要求的距离的索引，即为该feature的索引
                    distanceIndex = distances.index(distance)
                    # 确保不与以前非核心点的重复，但计数器会加1，核心点先到先得周围的点
                    #if kernalSons :
                    #    # 这个sons原本生成的是个二维列表！！！
                    #    for sons in kernalSons[-1]:
                    #        breakKernalSons.append(sons)
                    #    if distanceIndex not in breakKernalSons:
                    #        distancesIndex.append(distanceIndex)
                    #else :
                    #    distancesIndex.append(distanceIndex)
                    # 这里没判断两个核心点之间是否会有重复的附从点
                    distancesIndex.append(distanceIndex)
                    ptNum += 1
            # 如果范围内的点符合要求,筛选掉那些范围内有一定数目的附从点
            # 但是这些附从点都被先到的拿走了的点
            if ptNum >= self.minPts and distancesIndex:
                # 保存核心点索引
                kernalPts.append(vertexIndex)
                kernalSons.append(distancesIndex)
                print('找到第'+ str(s) +'个核心点')
                s += 1
        
        # 如果找到的核心点为0，返回0
        if not kernalPts:
            return 0
            
        allCluster,allSons = self.findCluster(kernalPts,kernalSons)

        # 显示
        m = 0
        for cluster in allCluster:
            k = 0
            if  isinstance(cluster,list):
                for pt in cluster:
                    self.layer.setPen(cluster[k],m+2)
                    k += 1
            else:
                self.layer.setPen(cluster,m+2)

            # 由于某个核心点可能有10个附从点，但是其对应的sons列表中未必有10个，
            # 所以不能用索引计数
            for sons in allSons[m]:
                for son in sons:
                    self.layer.setPen(son,m+2)

            m+=1
        
        return

    def  findCluster(self,kernalPt,kernalSons):
        p = 1
        # 深拷贝后可直接在列表上修改
        kernalPts = copy.deepcopy(kernalPt)
        # 用来获得索引，和sons对照
        kernalPt = kernalPt
        kernalSons = kernalSons

        # 遍历核心点找其范围内的其他核心点
        n = 0
        allCluster = []
        allSons = []
        # 打乱核心点列表
        random.shuffle(kernalPts)
        # 遍历所有核心点，即可能的所有簇
        for kernal in kernalPts:
            # 一个簇中的核心点队列
            clusterDeque = []
            # 添加第一个核心点
            clusterDeque.append(kernal)
            # 所有的核心点列表中删去当前的，表示该核心点已经在某簇中
            kernalPts.remove(kernal)
            sons = []
            
            # 遍历队列里的点，同时发现新的点会添加进去
            for queKernal in clusterDeque:
                # 核心点在原列表的索引，用以找到其半径范围内的附从点
                kernalIndex = kernalPt.index(queKernal)
                sons.append(kernalSons[kernalIndex])
                # 遍历quekernal的附从点，判断其是否为核心点
                for kernalSon in kernalSons[kernalIndex]:
                    # 如果是核心，就加入队列
                    if kernalSon in kernalPts:
                        clusterDeque.append(kernalSon)
                        kernalPts.remove(kernalSon)
                        print('核心点列表的长度：'+str(len(kernalPts)))
            
            # 队列只加不删，所以队列即为该簇的所有核心点
            allCluster.append(clusterDeque)
            # 与cluster对应的附从点
            allSons.append(sons)
            print('找到第'+ str(p) +'个簇')
            p += 1

        return allCluster,allSons