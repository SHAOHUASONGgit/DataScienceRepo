import numpy as np
import cv2

def calcDistance(start, end):
    distance = np.sqrt(np.sum(np.square(np.array(start) - np.array(end))))
    return distance

def agnesImage(image):
    b, g, r = cv2.split(image)
    b = b.flatten()
    g = g.flatten()
    r = r.flatten()