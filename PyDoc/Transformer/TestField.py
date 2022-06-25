import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from ThermoDataLoader import ThermoDataBaseTest, ThermoDataBase
from MLPMixer import MLPMixerModule


trainSet = ThermoDataBase()
trainSetLoader = DataLoader(dataset=trainSet, batch_size=1, shuffle=True, drop_last=False)

testSet = ThermoDataBaseTest()
testSetLoader = DataLoader(dataset=testSet, batch_size=1, shuffle=True, drop_last=False)

module = MLPMixerModule(3, 224, 16, 2, 8, 0.3)
lossFunction = nn.MSELoss()
lossSum = nn.MSELoss(reduction="sum")
learningRate = 0.001 # 学习率
optimizer = torch.optim.SGD(module.parameters(), learningRate, weight_decay=0.05)
scheduler = None
epoch = 100
writer = SummaryWriter("History")
GlobalStep = 0

for currentEpoch in range(epoch):
    print("----- Now epoch " + str(currentEpoch + 1) + " -----")

    module.train()
    for data in trainSetLoader:
        images, labels = data
        predictions = module(images)
        loss = lossFunction(predictions, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    module.eval()
    trainLoss = 0
    testLoss = 0
    trainRate = 0
    testRate = 0
    with torch.no_grad():
        totalLoss = 0
        totalNumbers = 0
        rightNumbers = 0
        for data in testSetLoader:
            images, labels = data
            predictions = module(images)
            totalLoss += float(lossSum(predictions, labels))
            _, predictionsMax = torch.max(predictions, dim = 1)
            _, labelMax = torch.max(labels, dim = 1)
            predictionsMax = predictionsMax.cpu().detach().numpy()
            labelMax = labelMax.cpu().detach().numpy()
            for index in range(len(labelMax)):
                totalNumbers += 1
                if labelMax[index] == predictionsMax[index]:
                    rightNumbers += 1
        testRate = round(100 * rightNumbers / totalNumbers, 2)
        testLoss = round(totalLoss, 2)

    with torch.no_grad():
        totalLoss = 0
        totalNumbers = 0
        rightNumbers = 0
        for data in trainSetLoader:
            images, labels = data
            predictions = module(images)
            totalLoss += float(lossSum(predictions, labels))
            _, predictionsMax = torch.max(predictions, dim = 1)
            _, labelMax = torch.max(labels, dim = 1)
            predictionsMax = predictionsMax.cpu().detach().numpy()
            labelMax = labelMax.cpu().detach().numpy()
            for index in range(len(labelMax)):
                totalNumbers += 1
                if labelMax[index] == predictionsMax[index]:
                    rightNumbers += 1
        trainRate = round(100 * rightNumbers / totalNumbers, 2)
        trainLoss = round(totalLoss, 2)

    print("测试集正确率: " + str(testRate) + "%")
    print("训练集正确率: " + str(trainRate) + "%")
    print("测试集总损失: " + str(testLoss))
    print("训练集总损失: " + str(trainLoss))
    writer.add_scalar("测试集正确率", testRate, global_step=GlobalStep)
    writer.add_scalar("训练集正确率", trainRate, global_step=GlobalStep)
    writer.add_scalar("测试集总损失", testLoss, global_step=GlobalStep)
    writer.add_scalar("训练集总损失", trainLoss, global_step=GlobalStep)
    GlobalStep += 1

imageModule = torch.randn(1, 3, 224, 224)
writer.add_graph(module, input_to_model=imageModule)
writer.close()