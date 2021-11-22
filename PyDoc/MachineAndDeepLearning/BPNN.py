import numpy as np
import pandas as pd

def dataReader(fileName):
    dataset = pd.read_csv(fileName, header=None)
    dataset = dataset.values[:, 0:5]
    return dataset

def onehotCreater(labels):
    allLabels = []
    output = []
    for data in labels:
        if data not in allLabels:
            allLabels.append(data)
    for data in labels:
        toInsert = np.zeros(len(allLabels))
        toInsert[allLabels.index(data)] = 1
        output.append(toInsert)
    return output

class net:
    def __init__(self,dataset,labels):
        self.weight1 = np.random.rand(10,4)#10output
        self.weight2 = np.random.rand(10,10)#10output
        self.weight3 = np.random.rand(3,10)#3output
        self.dataset = dataset
        self.labels = labels

    def sigmod(self,input):
        output = np.zeros((input.shape[0],input.shape[1]))
        for pointer in range(len(input.flat)):
            output[pointer] = 1/(1+np.exp(-input[pointer,0]))
        return output

    def frontSpred(self, weights, input):
        output = weights*input
        output = self.sigmod(output)
        return output

    def train(self):
        length = self.dataset.shape[0]
        for pointer in range(length):
            layer1 = np.matrix(self.dataset[pointer]).reshape(-1,1)#原始数据输入，转化为列向量
            layer2 = np.matrix(self.frontSpred(self.weight1, layer1)).reshape(-1,1)
            layer3 = np.matrix(self.frontSpred(self.weight2, layer2)).reshape(-1,1)
            layer4 = np.matrix(self.frontSpred(self.weight3, layer3)).reshape(-1,1)
            delta4 = layer4-np.matrix(self.labels[pointer]).reshape(-1,1)


allData = dataReader('iris.csv')
dataset = allData[:,0:4]
labels = onehotCreater(allData[:,4])
irisNet = net(dataset,labels)
irisNet.train()