import torch
import pandas as pd

def getLabels(labels):
    allLabels = []
    for data in labels:
        if data not in allLabels:
            allLabels.append(data)
    return allLabels

def classfy(input, allLabels):
    output = allLabels[input.index(max(input))]
    return output

def dataReader(fileName):
    dataset = pd.read_csv(fileName, header=None)
    dataset = dataset.values[:, 0:5]
    return dataset

allData = dataReader('iris.csv')
allLabels = getLabels((allData[:,4]))
net = torch.load("model.pkl")
raw = list(net(torch.tensor([6.5,3.0,5.5,1.8]).float()))
predction = classfy(raw, allLabels)
print("It is " + predction)