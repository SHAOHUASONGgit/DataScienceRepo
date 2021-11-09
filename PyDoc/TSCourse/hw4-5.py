import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

def caculateSeason(input, period):
    length = int(len(input)/period)
    output = [0]*period
    totalAverage = np.average(input)
    for i in range(0,period):
        for j in range(0,length):
            output[i] += input[i+j*period]/length/totalAverage
    return np.around(output,decimals=2)

def removeSeason(series, season):
    length = int(len(series))
    period = int(len(season))
    output = [0]*length
    for i in range(0,length):
        output[i] = series[i]/season[i%period]
    return output

def plusSeason(series, season):
    length = int(len(series))
    period = int(len(season))
    output = [0]*length
    for i in range(0,length):
        output[i] = series[i]*season[i%period]
    return output

def drawer(input):
    plt.plot(input, '*-')
    plt.show()
    plt.close()

def drawcompare(series, prediction):
    plt.plot(series, "*-", label='observe')
    plt.plot(prediction, "*", label='fittes')
    plt.legend()
    plt.show()
    plt.close()

filename = "data1.11.csv"
series = pd.read_csv(filename, header=None)
series.iloc[:, 0] = series.iloc[:, 0].astype("float")
series = series.values[:, 0]
season = caculateSeason(series,12)
afterRemove = removeSeason(series,season)

x = np.arange(1, len(afterRemove) + 1)
model = sm.OLS(series, sm.add_constant(x))
model = model.fit()
print(model.summary())
prediction = model.predict(sm.add_constant(x))
prediction = plusSeason(prediction,season)
drawcompare(series, prediction)

