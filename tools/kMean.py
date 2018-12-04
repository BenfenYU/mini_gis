import copy,random,sys
import numpy as np
from basicClass import basic

class Kmeans:

    def __init__(self,layer,num,iterNum):
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
            randomIndex = self.iters(randomIndex,featureNum)
            k += 1
    
    def iters(self,random,featureNum):
        randomIndex = random
        result = np.array([])
        for index in randomIndex:
            # 计算每个点到随机点的距离
            distance = np.array(self.layer.distance(self.layer[index]\
            .GISSpatial_spatialpart.GISVertex_centroid))
            # 存储在result的二维数组中，方便下步比较
            result = np.concatenate((result,distance))
        result = result.reshape(len(distance),len(randomIndex))
        #print(result.shape)
        # 存储分了n类后各类的点
        resultTag = []
        for _ in range(len(randomIndex)):
            resultTag.append([])
        for m in range(len(result)):
            # 求得每个点距离哪个点最近，设置其颜色，分成n类并存储相对索引
            minIndex = np.where(result[m]==min(result[m]))[0]
            print('minIndex'+str(minIndex))
            #realFeatureIndex = randomIndex[minIndex]
            self.layer.setPen(m,minIndex+6)
            # resultTag是n维列表，存储各类各自的对象的索引
            resultTag[int(minIndex)].append(m)
        
        randomIndex = self.findCenter(resultTag)
        #print('Kmean完毕')
        return randomIndex

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