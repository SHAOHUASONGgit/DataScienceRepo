import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

def dataReader(fileName):
    dataset = pd.read_csv(fileName, header=None)
    dataset = dataset.values[:, 0:5]
    return dataset

def caculateDistance(startPoint, endPoint):
    return sum((startPoint-endPoint)**2)**0.5

def iriskNN_Classify(dataset, input, decideNumber):
    length = len(dataset)
    distances = [[0,'None']]*length
    labels = {}
    for pointer in range(length):
        startPoint = np.array(dataset[pointer][:-1])
        endPoint = np.array(input)
        label = dataset[pointer][-1]
        distance = caculateDistance(startPoint, endPoint)
        distances[pointer] = [distance,label]
    distances.sort(key=lambda x: x[0])
    for pointer in range(decideNumber):
        label = distances[pointer][-1]
        if (label not in labels):
            labels[label] = 0
        labels[label] += 1
    labelsInOrder = sorted(labels.items(),key=lambda x:x[1],reverse=True)
    result = labelsInOrder[0][0]
    return result

def check(dataset, decideNumber):
    labels = {}
    falseLabel = {}
    result = {}
    for data in dataset:
        realLabel = data[-1]
        if (realLabel not in labels):
            labels[realLabel] = 0
            falseLabel[realLabel] = 0
        labels[realLabel] += 1
        predictLabel = iriskNN_Classify(dataset, data[:-1], decideNumber)
        if predictLabel!=realLabel:
            falseLabel[realLabel] += 1
    for label in labels:
        total = labels[label]
        loss = falseLabel[label]
        result[label] = (total-loss)/total
    return result


dataset = dataReader('iris.csv')
prediction = iriskNN_Classify(dataset, [7,7,7,7], 7)
print("It is " + prediction)
checkResult = check(dataset,7)
print(checkResult)

dataset = dataReader('bezdekIris.csv')
prediction = iriskNN_Classify(dataset, [2,2,2,2], 7)
print("It is " + prediction)
checkResult = check(dataset,7)
print(checkResult)

dataset = dataReader('doubleiris.csv')
prediction = iriskNN_Classify(dataset, [2,2,2,2], 7)
print("It is " + prediction)
checkResult = check(dataset,7)
print(checkResult)

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