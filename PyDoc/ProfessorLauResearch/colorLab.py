import cv2
import numpy as np

def gamma2Lab(inputMat):
    outputMat = np.where(inputMat > 0.0405, ((inputMat + 0.055) / 1.055) ** 2.4, inputMat / 12.92)
    return outputMat

def funt2Lab(inputMat):
    outputMat = np.where(inputMat > 0.008856, inputMat ** (1 / 3), (inputMat * 7.787) + 16 / 116)
    return outputMat

def gamma2BGR(inputMat):
    outputMat = np.where(inputMat > 0.0031308, 1.055 * (inputMat ** 0.4166) - 0.055, inputMat * 12.92)
    return outputMat

def funt2BGR(inputMat):
    outputMat = np.where((inputMat ** 3) > 0.008856, inputMat ** 3, (inputMat - 16 / 116) / 7.787)
    return outputMat

def bgr2BRG(inputMat):
    outputMat = np.where(inputMat < 1, inputMat, 1)
    outputMat = np.where(outputMat > 0, outputMat, 0) * 255
    return outputMat

def BGR2Lab(image):  # Convert BGR Image to Lab Image
    B, G, R = cv2.split(image.astype(np.float32))
    B = gamma2Lab(B / 255)
    G = gamma2Lab(G / 255)
    R = gamma2Lab(R / 255)
    X = funt2Lab((R * 0.4124 + G * 0.3576 + B * 0.1805) / 0.95047)
    Y = funt2Lab((R * 0.2126 + G * 0.7152 + B * 0.0722) / 1.00000)
    Z = funt2Lab((R * 0.0193 + G * 0.1192 + B * 0.9505) / 1.08883)
    L = 116.0 * Y - 16.0
    a = 500.0 * (X - Y)
    b = 200.0 * (Y - Z)
    outputImage = cv2.merge([L, a, b])
    return outputImage

def Lab2BGR(image):  # Convert Lab Image to BGR Image
    L, a, b = cv2.split(image)
    Y = (L + 16) / 116
    X = a / 500 + Y
    Z = Y - b / 200
    Y = funt2BGR(Y) * 1
    X = funt2BGR(X) * 0.9547
    Z = funt2BGR(Z) * 1.08883
    R = bgr2BRG(gamma2BGR(X * 3.2406 + Y * -1.5372 + Z * -0.4986)).astype(np.uint8)
    G = bgr2BRG(gamma2BGR(X * -0.9689 + Y * 1.8758 + Z * 0.0415)).astype(np.uint8)
    B = bgr2BRG(gamma2BGR(X * 0.0557 + Y * -0.2040 + Z * 1.0570)).astype(np.uint8)
    outputImage = cv2.merge([B, G, R])
    return outputImage

def histLab(inputMat, rangeSize, min):
    hist = [0] * rangeSize
    U = 0
    totalPixels = inputMat.size
    for pixel in inputMat.flat:
        hist[pixel - min - 1] += 1 / totalPixels
    for data in range(len(hist)):
        U += (data + min) * hist[data]
    return hist, U

def BGR2LabColorReshape(image):  # Chapter 4 Step 1
    outputImage = BGR2Lab(image)
    L, a, b = cv2.split(outputImage)
    ahist, aU = histLab(a.astype(int), 255, -128)
    bhist, bU = histLab(b.astype(int), 255, -128)
    a = (a - aU).astype(np.float32)
    b = (b - bU).astype(np.float32)
    outputImage = cv2.merge([L, a, b])
    outputImage = Lab2BGR(outputImage)
    return outputImage

def BRGReblance(image):  # Chapter 4 Step 2
    B, G, R = cv2.split(image)
    B = cv2.equalizeHist(B)
    G = cv2.equalizeHist(G)
    R = cv2.equalizeHist(R)
    outputImage = cv2.merge([B, G, R])
    return outputImage

def darkChannelReblance(image):  # Chapter 3
    B, G, R = cv2.split(image)
    totalAverage = (np.average(B) + np.average(G) + np.average(R)) / 3
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
    newChannels = []
    for channel in [B, G, R]:
        if(np.average(channel)>totalAverage):
            afterChannel = cv2.erode(channel, kernel, iterations=1)
        else:
            afterChannel = cv2.dilate(channel, kernel, iterations=1)
        newChannels.append(afterChannel)
    outputImage = cv2.merge([newChannels[0], newChannels[1], newChannels[2]])
    return outputImage
#image = darkChannelReblance(image)

image = cv2.imread("beforeLab.png")
image = BGR2LabColorReshape(image)
image = BRGReblance(image)
cv2.imwrite("afterLab.png", image)