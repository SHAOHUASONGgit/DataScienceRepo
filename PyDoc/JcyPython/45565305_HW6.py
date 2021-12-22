import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def LSMReg(area, price):
    areaTemp = area - np.mean(area)
    priceTemp = price - np.mean(price)
    a = np.sum(areaTemp * priceTemp)/np.sum(areaTemp * areaTemp)
    b = np.mean(price) - a * np.mean(area)
    return [a, b]

data = pd.read_csv("data.csv", usecols=[1, 4])
price = data["总价(万元)"].values
area = data["面积"].values
line = LSMReg(area, price)
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.text(0, 5000, "y = " + str(round(line[0], 3)) + "x + " + str(round(line[1], 3)))
plt.title("房屋总价与面积线性回归")
plt.xlabel("面积(单位: 平方米)")
plt.ylabel("总价(单位: 万元)")
plt.plot(area, price, "b.")
plt.plot(area, line[0] * area + line[1], "y-")
plt.savefig("房屋总价与面积线性回归.png")
plt.show()

