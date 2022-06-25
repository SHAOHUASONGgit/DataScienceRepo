import os
import cv2
import torch
import torch.optim
import numpy as np
from PIL import Image
from torch.utils.data import Dataset
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
        Limg = cv2.resize(cv2.imread(Lpath), (112, 224))
        Rimg = cv2.resize(cv2.imread(Rpath), (112, 224))
        img = self.transform(Image.fromarray(np.hstack((Rimg, Limg))))
        return img, label

    def __len__(self):
        return len(self.totalList)

    def whichList(self, path):
        if path in self.CgroupList:
            return "ThermoDataBase/Control Group", torch.Tensor([1, 0])
        if path in self.DgroupList:
            return "ThermoDataBase/DM Group", torch.Tensor([0, 1])

class ThermoDataBaseTest(Dataset):

    def __init__(self):
        self.CgroupList = os.listdir("ThermoDataBaseTest/Control Group")
        self.DgroupList = os.listdir("ThermoDataBaseTest/DM Group")
        self.totalList = self.CgroupList + self.DgroupList
        self.transform = transforms.Compose([transforms.ToTensor()])  #transforms.Resize((160, 60))

    def __getitem__(self, index):
        pathTail = self.totalList[index]
        pathHead, label = self.whichList(pathTail)
        Lpath = pathHead + "/" + pathTail + "/" + pathTail + "_L.png"
        Rpath = pathHead + "/" + pathTail + "/" + pathTail + "_R.png"
        Limg = cv2.resize(cv2.imread(Lpath), (112, 224))
        Rimg = cv2.resize(cv2.imread(Rpath), (112, 224))
        img = self.transform(Image.fromarray(np.hstack((Rimg, Limg))))
        return img, label

    def __len__(self):
        return len(self.totalList)

    def whichList(self, path):
        if path in self.CgroupList:
            return "ThermoDataBaseTest/Control Group", torch.Tensor([1, 0])
        if path in self.DgroupList:
            return "ThermoDataBaseTest/DM Group", torch.Tensor([0, 1])
'''
trainSet = ThermoDataBase()
trainSetLoader = DataLoader(dataset=trainSet, batch_size=6, shuffle=True, drop_last=True)

testSet = ThermoDataBaseTest()
testSetLoader = DataLoader(dataset=testSet, batch_size=6, shuffle=True, drop_last=True)
'''