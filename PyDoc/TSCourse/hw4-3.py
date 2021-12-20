import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def caculateSeason(input, period):
    length = int(len(input)/period)
    output = [0]*period
    totalAverage = np.average(input)
    for i in range(0,period):
        for j in range(0,length):
            output[i] += input[i+j*period]/length/totalAverage
    return np.around(output,decimals=2)

def drawer(input):
    plt.plot(input, '*-')
    plt.show()
    plt.close()

filename = "hw4-3data.csv"
series = pd.read_csv(filename, header=None)
series.values[1:,1:]
datainput = []
for row in series.values[1:,1:]:
    for data in row:
        datainput.append(data)
dataoutput = caculateSeason(datainput,12)
print(dataoutput)