import numpy as np
import pandas as pd


def dataReader(fileName):
    dataset = pd.read_csv(fileName, header=None)
    dataset = dataset.values[:, 0:5]
    return dataset


def caculateDistance(startPoint, endPoint):
    return sum((startPoint-endPoint)**2)**0.5


def iriskNN_Classify(dataset, input, decideNumber, specialPoint):
    length = len(dataset)
    distances = []
    labels = {}
    for pointer in range(length):
        startPoint = np.array(dataset[pointer][:-1])
        endPoint = np.array(input)
        label = dataset[pointer][-1]
        distance = caculateDistance(startPoint, endPoint)
        distances.append([distance,label])
    distances.sort(key=lambda x: x[0])
    for pointer in range(decideNumber):
        label = distances[pointer][-1]
        if (label not in labels):
            labels[label] = 0
        labels[label] += 1
    labelsInOrder = sorted(labels.items(),key=lambda x:x[1],reverse=True)
    kNNPrediction = labelsInOrder[0][0]
    specialPointPrediction = ""
    for data in specialPoint:
        distance = caculateDistance(data[0], input)
        minDistance = data[1]
        specialLabel = data[2]
        if(distance <= minDistance):
            specialPointPrediction = specialLabel
    if(kNNPrediction == specialPointPrediction):
        return kNNPrediction
    elif(specialPointPrediction == ""):
        return kNNPrediction
    else:
        return specialPointPrediction


def elder_iriskNN_Classify(dataset, input, decideNumber):
    length = len(dataset)
    distances = []
    labels = {}
    for pointer in range(length):
        startPoint = np.array(dataset[pointer][:-1])
        endPoint = np.array(input)
        label = dataset[pointer][-1]
        distance = caculateDistance(startPoint, endPoint)
        distances.append([distance,label])
    distances.sort(key=lambda x: x[0])
    for pointer in range(decideNumber):
        label = distances[pointer][-1]
        if (label not in labels):
            labels[label] = 0
        labels[label] += 1
    labelsInOrder = sorted(labels.items(),key=lambda x:x[1],reverse=True)
    kNNPrediction = labelsInOrder[0][0]
    return kNNPrediction


def elder_check(dataset, decideNumber, specialPoint):
    labels = {}
    falseLabel = {}
    result = {}
    for data in dataset:
        realLabel = data[-1]
        if (realLabel not in labels):
            labels[realLabel] = 0
            falseLabel[realLabel] = 0
        labels[realLabel] += 1
        predictLabel = elder_iriskNN_Classify(dataset, data[:-1], decideNumber)
        if predictLabel!=realLabel:
            falseLabel[realLabel] += 1
    for label in labels:
        total = labels[label]
        loss = falseLabel[label]
        result[label] = (total-loss)/total
    return result


def check(dataset, decideNumber, specialPoint):
    labels = {}
    falseLabel = {}
    result = {}
    for data in dataset:
        realLabel = data[-1]
        if (realLabel not in labels):
            labels[realLabel] = 0
            falseLabel[realLabel] = 0
        labels[realLabel] += 1
        predictLabel = iriskNN_Classify(dataset, data[:-1], decideNumber, specialPoint)
        if predictLabel!=realLabel:
            falseLabel[realLabel] += 1
    for label in labels:
        total = labels[label]
        loss = falseLabel[label]
        result[label] = (total-loss)/total
    return result


def iriskNN_specialPoint_detector(dataset, decideNumber, specialRange):
    length = len(dataset)
    distances = []
    specialPoint = []
    labels = {}
    for firstPointer in range(length):
        realLabel = dataset[firstPointer][-1]
        for secondPointer in range(length):
            if(firstPointer != secondPointer):
                startPoint = np.array(dataset[secondPointer][:-1])
                endPoint = np.array(dataset[firstPointer][:-1])
                label = dataset[secondPointer][-1]
                distance = caculateDistance(startPoint, endPoint)
                distances.append([distance, label])
        distances.sort(key=lambda x: x[0])
        for pointer in range(decideNumber):
            label = distances[pointer][-1]
            if (label not in labels):
                labels[label] = 0
            labels[label] += 1
        labelsInOrder = sorted(labels.items(),key=lambda x:x[1],reverse=True)
        prediction = labelsInOrder[0][0]
        if(prediction!=realLabel):
            location = dataset[firstPointer][:-1]
            distance = distances[0][0]*specialRange
            specialPoint.append([location, distance, realLabel])
        distances.clear()
    return specialPoint


dataset = dataReader('iris.csv')
specialPoint = iriskNN_specialPoint_detector(dataset, 7, 1)
# [5.9, 3.2, 4.8, 1.8] is Iris-versicolor
prediction = elder_iriskNN_Classify(dataset, [5.9, 3.2, 4.8, 1.8], 7)
print("It is " + prediction)
checkResult = elder_check(dataset, 7, specialPoint)
print(checkResult)
prediction = iriskNN_Classify(dataset, [5.9, 3.2, 4.8, 1.8], 7, specialPoint)
print("It is " + prediction)
checkResult = check(dataset, 7, specialPoint)
print(checkResult)

specialPoint = iriskNN_specialPoint_detector(dataset, 7, 0.8)
prediction = iriskNN_Classify(dataset, [5.9, 3.2, 4.8, 1.8], 7, specialPoint)
print("It is " + prediction)
checkResult = check(dataset, 7, specialPoint)
print(checkResult)
'''
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
print(dataset)
for data in dataset:
    x = data[0]
    y = data[1]
    z = data[2]
    if(data[-1] == "Iris-virginica"):
        ax.scatter(x, y, z,c='#000000')
    elif(data[-1] == "Iris-versicolor"):
        ax.scatter(x, y, z, c='#ff0000')
    else:
        ax.scatter(x, y, z, c='#008000')
plt.show()
plt.close()
'''