import os
import cv2
import torch.optim
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from PIL import Image
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision import transforms
class ThermoDataBase(Dataset):
    def __init__(self):
        self.CgroupList = os.listdir("ThermoDataBase/Control Group")
        self.DgroupList = os.listdir("ThermoDataBase/DM Group")
        self.totalList = self.CgroupList + self.DgroupList
        self.transform = transforms.Compose([transforms.ToTensor()])  #transforms.Resize((160, 60))

    def __getitem__(self, index):
        pathTail = self.totalList[index]
        pathHead, label = self.whichList(pathTail)
        Lpath = pathHead + "/" + pathTail + "/" + pathTail + "_L.png"
        Rpath = pathHead + "/" + pathTail + "/" + pathTail + "_R.png"
        Limg = cv2.resize(cv2.imread(Lpath), (80, 160))
        Rimg = cv2.resize(cv2.imread(Rpath), (80, 160))
        img = self.transform(Image.fromarray(np.hstack((Rimg, Limg))))
        return img, label

    def __len__(self):
        return len(self.totalList)

    def whichList(self, path):
        if path in self.CgroupList:
            return "ThermoDataBase/Control Group", torch.Tensor([1, 0])
        if path in self.DgroupList:
            return "ThermoDataBase/DM Group", torch.Tensor([0, 1])
class CNNnet(nn.Module):

    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.maxp1 = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(6, 12, 6)
        self.maxp2 = nn.MaxPool2d(2)
        self.flat = nn.Flatten()
        self.fc1 = nn.Linear(12 * 36 * 36, 64)
        self.fc2 = nn.Linear(64, 16)
        self.fc3 = nn.Linear(16, 2)

    def forward(self, x):
        x = self.conv1(x)
        x = self.maxp1(x)
        x = self.conv2(x)
        x = self.maxp2(x)
        x = self.flat(x)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

dataset = ThermoDataBase()
data_loader = DataLoader(dataset=dataset, batch_size=6, shuffle=True, drop_last=True)

cnn = CNNnet()
lossf = nn.CrossEntropyLoss()
losss = nn.CrossEntropyLoss(reduction='sum')
opt = optim.SGD(cnn.parameters(), lr=0.001)
epoch = 100

writer = SummaryWriter("History")
wstep = 0

for i in range(epoch):
    print("-----" + "训练第 " + str(i + 1) +" 轮"+ "-----")
    times = 0
    for data in data_loader:
        imgs, labels = data
        outputs = cnn(imgs)
        loss = lossf(outputs, labels)
        opt.zero_grad()
        loss.backward()
        opt.step()
        times = times + 1
        writer.add_images("Image Batches", imgs, wstep)

    with torch.no_grad():
        totalLoss = 0
        total = 0
        true = 0
        for data in data_loader:
            imgs, labels = data
            outputs = cnn(imgs)
            loss = losss(outputs, labels)
            totalLoss = totalLoss + loss
            for i in range(6):
                if outputs[i][0] > outputs[i][1]:
                    outputs[i] = torch.tensor([1, 0])
                else:
                    outputs[i] = torch.tensor([0, 1])
                total += 1
                if outputs[i][0] == labels[i][0] and outputs[i][1] == labels[i][1]:
                    true += 1
        writer.add_scalar("Accuracy", true/total, wstep)
        writer.add_scalar("Total Loss", totalLoss, wstep)
        print(totalLoss)
    wstep += 1
tempimg = torch.randn(6, 3, 160, 160)
writer.add_graph(cnn, tempimg)
writer.close()