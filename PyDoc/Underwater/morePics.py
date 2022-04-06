import cv2
from Underwater.colorLab import darkChannelReblance

image = cv2.imread("3.png")
B, G, R = cv2.split(image)
R = cv2.normalize(R, R, alpha=0, beta=4, norm_type=cv2.NORM_MINMAX)
cv2.imshow("R1", R*10)

image = darkChannelReblance(image)
B, G, R = cv2.split(image)
R = cv2.normalize(R, R, alpha=0, beta=4, norm_type=cv2.NORM_MINMAX)
cv2.imshow("R2", R*20)

cv2.waitKey()