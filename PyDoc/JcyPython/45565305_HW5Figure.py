import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"]=["SimHei"]
data = pd.read_csv("data.csv", usecols=[0, 1])
boxplot = data.boxplot(column="总价(万元)", by="片区")
plt.title("北京房价箱形图")
plt.suptitle("")
plt.savefig("北京房价箱形图.png")
plt.show()