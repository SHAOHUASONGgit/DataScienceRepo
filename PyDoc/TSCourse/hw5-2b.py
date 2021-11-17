import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA


def drawer(input):
    plt.figure(figsize=(10,8))
    series = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    acf=plt.subplot2grid((2,2),(1,0))
    pacf=plt.subplot2grid((2,2),(1,1))
    series.plot(input, '*-')
    plot_acf(input,ax=acf)
    plot_pacf(input,ax=pacf)
    plt.show()
    plt.close()

def purerandtest(y):
    a,b=acorr_ljungbox(y,lags=None,boxpierce=False)
    LB_purerand=pd.DataFrame(np.c_[a,b],columns=['LB','Pvalue'])
    LB_purerand['lags']=range(1,len(a)+1)
    print('----time series: LB pure randomness test----')
    print(LB_purerand)

def caculatediff(diff, step, input):
    if(step!=0):
        input = input[step:] - input[:-step]
    if (diff == 0):
        return input
    input = input[1:] - input[:-1]
    return caculatediff(diff - 1, 0, input)

def drawcompare(series, prediction):
    plt.plot(series, "*-", label='observe')
    plt.plot(prediction, label='fittes')
    plt.legend()
    plt.show()
    plt.close()

filename = "data_hw5-2b.csv"
series = pd.read_csv(filename, header=None)
series.iloc[:, 0] = series.iloc[:, 0].astype("float")
series = series.values[:, 0]
drawer(series)

diff2 = caculatediff(2,0,series)
purerandtest(diff2)
drawer(diff2)

model = ARIMA(series, order=(1, 2, 1)).fit()
print('----fitting summary----')
print(model.summary())

resid=model.resid
print('\n----residual pure randomness test')
purerandtest(resid)

prediction = model.get_prediction(start=0,end=len(series)-1+20,dynamic=False)
print('\n----fitted confidence interval: %d %%'%((1-0.05)*100))
print(prediction.summary_frame(alpha=0.05))

prediction = prediction.summary_frame(alpha=0.05).iloc[:,[0]]
prediction = prediction.values[:, 0]
drawcompare(series,prediction[1:])