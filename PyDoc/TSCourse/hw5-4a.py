import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.tsa.arima.model as smt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox

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

def purerandtest(input):
    LB,Pvalue=acorr_ljungbox(input,lags=None,boxpierce=False)
    for pointer in range(len(Pvalue)):
        Pvalue[pointer] = round(Pvalue[pointer],3)
    LB_purerand=pd.DataFrame(np.c_[LB,Pvalue],columns=['LB','Pvalue'])
    LB_purerand['lags']=range(1,len(LB)+1)
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

filename = "data_hw5.2.csv"
series = pd.read_csv(filename, header=None)
series.iloc[:, 0] = series.iloc[:, 0].astype("float")
series = series.values[:, 0]
drawer(series)

diff1step12 = caculatediff(1, 12, series)
drawer(diff1step12)
purerandtest(diff1step12)

model=smt.ARIMA(series,order=(1,1,1),seasonal_order=(3,1,0,12)).fit() #trend=n,c,t,ct
print('----fitting summary----')
print(model.summary())

resid=model.resid
print('\n----residual pure randomness test')
purerandtest(resid)

prediction = model.get_prediction(start=0,end=len(series)-1+20,dynamic=False)
prediction = prediction.summary_frame(alpha=0.05).iloc[:,[0]]
prediction = prediction.values[:, 0]
drawcompare(series,prediction[1:])