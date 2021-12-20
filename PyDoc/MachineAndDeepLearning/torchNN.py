import torch
import torch.nn as nn
import numpy as np
import pandas as pd

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

def dataReader(fileName):
    dataset = pd.read_csv(fileName, header=None)
    dataset = dataset.values[:, 0:5]
    return dataset

class linearNN:

    def __init__(self,dataset,labels):
        self.net = nn.Sequential(nn.Linear(4, 10),nn.Sigmoid(),nn.Linear(10, 10),nn.Sigmoid(),nn.Linear(10, 3),nn.Sigmoid())
        self.optimzer = torch.optim.SGD(self.net.parameters(), lr=0.05)
        self.loss_func = nn.MSELoss()
        self.dataset = torch.tensor(dataset).float()
        self.labels = torch.tensor(labels).float()

    def train(self, times, minloss):
        for time in range(times):
            out = self.net(self.dataset)
            loss = self.loss_func(out, self.labels)  # 计算误差
            print(loss)
            if (loss < minloss):
                print(loss)
                break
            self.optimzer.zero_grad()  # 清除梯度
            loss.backward()
            self.optimzer.step()
        torch.save(self.net, "model.pkl")

allData = dataReader('iris.csv')
dataset = np.mat(allData[:,0:4]).astype(float)
labels = np.mat(onehotCreater(allData[:,4])).astype(float)

net = linearNN(dataset,labels)
net.train(100000,0.01)