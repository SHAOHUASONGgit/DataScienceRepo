import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.tsa.api as smt

def drawer(series):
    plt.figure(figsize=(10,8))
    timeseries = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    acf = plt.subplot2grid((2, 2), (1, 0))
    pacf = plt.subplot2grid((2, 2), (1, 1))

    timeseries.plot(series, '*-')
    timeseries.set_title("Analysis")
    smt.graphics.plot_acf(series, lags=None, ax=acf, alpha=0.05)
    smt.graphics.plot_pacf(series, lags=None, ax=pacf, alpha=0.05)

    plt.show()
    plt.close()

def drawcompare(series, prediction, movestep):
    plt.plot(series, "*-", label='ob')
    plt.plot(range(int(movestep/2), int(movestep/2) + len(prediction)),prediction, label='avg')
    plt.legend()
    plt.show()
    plt.close()

def midMovingAverage(series, movestep):
    if(movestep%2==1 and movestep!=1):
        output = [0]
        for i in range(len(series)-(movestep+1)):
            output.append(sum(series[i:i+movestep])/movestep)
        return output #移动项数为奇数时直接返回
    elif(movestep!=1):
        output = []
        for i in range(len(series)-(movestep+1)):
            output.append(sum(series[i:i+movestep])/movestep)
        return midMovingAverage(output, 1) #移动项数为偶数时，再计算一次
    else:
        output = []
        for i in range(len(series)-1):
            output.append(sum(series[i:i+2])/2)
        return output

filename = "table_a1.17.csv"
series = pd.read_csv(filename, header=None)
series.iloc[:, 0] = series.iloc[:, 0].astype("float")
series = series.values[:, 0]
drawer(series)

output = midMovingAverage(series, 12)
drawcompare(series, output, 12)