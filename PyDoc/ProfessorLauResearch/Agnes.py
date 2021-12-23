import numpy as np
import cv2

def calcDistance(start, end):
    distance = np.sqrt(np.sum(np.square(np.array(start) - np.array(end))))
    return distance

def getIndexPixel(BGR, index):
    B = BGR[0][index]
    G = BGR[1][index]
    R = BGR[2][index]
    return [B, G, R]

def agnesImage(image, setNum, setMin):
    b, g, r = cv2.split(image)
    pixelNum = image.shape[0] * image.shape[1]  # 像素数量
    totalPixels = [b.flatten(), g.flatten(), r.flatten()]  # 打平RGB通道成3个一维数组
    setData = []  # 簇的集合
    for num in range(pixelNum):
        setData.append([num])
    while(len(setData) > setNum):  # 当簇的数量仍然大于setNum的时候
        minDistance = float('inf')  # float形变量的最大值
        setMasterIndex = 0
        setSlaveIndex = 0
        for firstPointer in range(len(setData) - 1):  # 对簇两两间
            for secondPointer in range(firstPointer + 1, len(setData)):
                avgDistance = 0
                for firstSetPoint in setData[firstPointer]:  # 计算簇间平均距离
                    for secondSetPoint in setData[secondPointer]:
                        avgDistance += (1 / (len(setData[firstPointer]) * len(setData[secondPointer]))) * (calcDistance(start=getIndexPixel(totalPixels, firstSetPoint), end=getIndexPixel(totalPixels, secondSetPoint)))
                if(avgDistance < minDistance):  # 求取簇之间最短的平均距离
                    minDistance = avgDistance
                    setMasterIndex = firstPointer
                    setSlaveIndex = secondPointer
        if(minDistance < setMin):  # 如果簇之间的最小距离小于设定的最小距离 仍然合并
            setData[setMasterIndex] = setData[setMasterIndex] + setData[setSlaveIndex]  # 合并簇
            setData.pop(setSlaveIndex)  # 弹出被合并的簇
        else:
            break
    return setData

image = cv2.imread("beforeLab.png")
image = cv2.resize(image, dsize=(10, 10))  # 把图像变小
pixelSet = agnesImage(image, 5, 10000)