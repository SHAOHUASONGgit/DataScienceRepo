import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure

def gamma2Lab(inputMat):
    return np.where(inputMat > 0.0405, ((inputMat + 0.055) / 1.055) ** 2.4, inputMat / 12.92)


def funt2Lab(inputMat):
    return np.where(inputMat > 0.008856, inputMat ** (1 / 3), (inputMat * 7.787) + 16 / 116)


def gamma2BGR(inputMat):
    return np.where(inputMat > 0.0031308, 1.055 * (inputMat ** 0.4166) - 0.055, inputMat * 12.92)


def funt2BGR(inputMat):
    return np.where((inputMat ** 3) > 0.008856, inputMat ** 3, (inputMat -16 / 116) / 7.787)


def bgr2BRG(inputMat):
    inputMat = np.where(inputMat < 1, inputMat, 1)
    return np.where(inputMat > 0, inputMat, 0) * 255


def BGR2Lab(image):
    B, G, R = cv2.split(image.astype(np.float32))
    B = gamma2Lab(B/255)
    G = gamma2Lab(G/255)
    R = gamma2Lab(R/255)
    X = funt2Lab((R * 0.4124 + G * 0.3576 + B * 0.1805) / 0.95047)
    Y = funt2Lab((R * 0.2126 + G * 0.7152 + B * 0.0722) / 1.00000)
    Z = funt2Lab((R * 0.0193 + G * 0.1192 + B * 0.9505) / 1.08883)
    L = 116.0 * Y - 16.0
    a = 500.0 * (X - Y)
    b = 200.0 * (Y - Z)
    return cv2.merge([L, a, b])


def Lab2BGR(image):
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
    return cv2.merge([B, G, R])

imageB = cv2.imread("input/test.png")
imageB2L = BGR2Lab(imageB)
imageB2L2B = Lab2BGR(imageB2L)

L, a, b = cv2.split(imageB2L)