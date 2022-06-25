import torch
import torch.nn as nn

class patchEmbedding(nn.Module):

    def __init__(self, inputChannels, imageSize, patchSize, patches, outputChannels):
        super().__init__()
        self.inputChannels = inputChannels
        self.imageSize = imageSize
        self.patchSize = patchSize
        self.patches = patches
        self.outputChannels = outputChannels

        self.patchEmbedding = nn.Conv2d(in_channels=self.inputChannels,
                                        out_channels=self.outputChannels,
                                        kernel_size=patchSize,
                                        stride=patchSize)
        self.flatten = nn.Flatten(2)

    def forward(self, batchInOut):
        batchInOut = self.patchEmbedding(batchInOut)
        batchInOut = self.flatten(batchInOut)
        batchInOut = torch.transpose(batchInOut, -1, -2)
        return batchInOut

class tokenMixing(nn.Module):

    def __init__(self, patches, inputChannels):
        super().__init__()
        self.patches = patches
        self.inputChannels = inputChannels

        self.layerNormalization = nn.LayerNorm(self.inputChannels)
        self.firstFullyConnectedLayer = nn.Linear(self.patches, self.patches)
        self.activateFunction = nn.GELU()
        self.secondFullyConnectedLayer = nn.Linear(self.patches, self.patches)


    def forward(self, batchInOut):
        residual = batchInOut
        batchInOut = self.layerNormalization(batchInOut)
        batchInOut = torch.transpose(batchInOut, -1, -2)
        batchInOut = self.firstFullyConnectedLayer(batchInOut)
        batchInOut = self.activateFunction(batchInOut)
        batchInOut = self.secondFullyConnectedLayer(batchInOut)
        batchInOut = torch.transpose(batchInOut, -1, -2)
        batchInOut = residual + batchInOut
        return batchInOut

class channelMixing(nn.Module):

    def __init__(self, inputChannels):
        super().__init__()
        self.inputChannels = inputChannels

        self.layerNormalization = nn.LayerNorm(self.inputChannels)
        self.firstFullyConnectedLayer = nn.Linear(self.inputChannels, self.inputChannels)
        self.activateFunction = nn.GELU()
        self.secondFullyConnectedLayer = nn.Linear(self.inputChannels, self.inputChannels)

    def forward(self, batchInOut):
        residual = batchInOut
        batchInOut = self.layerNormalization(batchInOut)
        batchInOut = self.firstFullyConnectedLayer(batchInOut)
        batchInOut = self.activateFunction(batchInOut)
        batchInOut = self.secondFullyConnectedLayer(batchInOut)
        batchInOut = residual + batchInOut
        return batchInOut

class MLPBlock(nn.Module):

    def __init__(self, patches, inputChannels):
        super().__init__()
        self.patches = patches
        self.inputChannels = inputChannels

        self.tokenMixing = tokenMixing(self.patches,
                                       self.inputChannels)
        self.channelMixing = channelMixing(self.inputChannels)

    def forward(self, batchInOut):
        batchInOut = self.tokenMixing(batchInOut)
        batchInOut = self.channelMixing(batchInOut)
        return batchInOut

class MLPMixerModule(nn.Module):

    def __init__(self, inputChannels, imageSize, patchSize, classes, depth, dropoutRate):
        super().__init__()
        self.inputChannels = inputChannels
        self.imageSize = imageSize
        self.patchSize = patchSize
        self.classes = classes
        self.patches = (imageSize // patchSize) ** 2
        self.outputChannels = (self.patchSize ** 2) * self.inputChannels

        self.patchEmbedding = patchEmbedding(self.inputChannels,
                                             self.imageSize,
                                             self.patchSize,
                                             self.patches,
                                             self.outputChannels)
        self.MLPBlocks = nn.Sequential(*[
            MLPBlock(self.patches, self.outputChannels) for blocks in range(depth)
        ])
        self.pooling = nn.AvgPool1d(kernel_size=self.outputChannels)
        self.classifier = nn.Linear(self.patches, self.classes)
        self.dropout = nn.Dropout(dropoutRate)
        self.flatten = nn.Flatten(1)

    def forward(self, batchInOut):
        batchInOut = self.patchEmbedding(batchInOut)
        batchInOut = self.MLPBlocks(batchInOut)
        batchInOut = self.pooling(batchInOut)
        batchInOut = torch.transpose(batchInOut, -1, -2)
        batchInOut = self.classifier(batchInOut)
        batchInOut = self.dropout(batchInOut)
        batchInOut = self.flatten(batchInOut)
        return batchInOut