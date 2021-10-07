import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
import matplotlib.pyplot as plt

def caculatePk(input, lag, method):
    if method == "LB":
        lag += 1
    Pk = np.ones(lag)
    N = len(input)
    u = input.mean()
    for k in range(0, lag):
        upsum = 0
        downsum = 0
        for i in range(0, N - k):
            upsum += (input[i] - u) * (input[i + k] - u)
        for i in range(0, N):
            downsum += (input[i] - u) ** 2
        Pk[k] = (upsum / downsum)
    return Pk

def caculateLB(Pk, input):
    LB = np.zeros(len(Pk))
    n = len(input)
    m = len(Pk)
    for i in range(1, m):
        for j in range(1, i + 1):
            LB[i] += n * (n + 2) * (Pk[j]**2 / (n - j))
    return LB[1:]

def drawer(input, Pk):
    plt.figure()
    inputplot = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    Pkplot = plt.subplot2grid((2, 2), (1, 0))

    twosigma = np.ones(len(Pk))
    n = len(input)
    twosigma[0] = ((1 / n) ** 0.5)
    for i in range(1, len(Pk)):
        sum = 0
        for j in range(0, i):
            sum += Pk[j] ** 2
        twosigma[i] = (((1 / n) * (1 + 2 * sum)) ** 0.5)

    Pkplot.bar(range(len(Pk)), Pk)
    Pkplot.fill_between(range(len(Pk)), -1 * twosigma, twosigma, color='lightblue')
    inputplot.plot(input, "-*")

    plt.show()
    plt.close()

def outputSeries(x1, x2):
    output = np.zeros(101)
    if(x2 != 0):
        output[0] = np.random.normal(0, 1, 1)
        output[1] = np.random.normal(0, 1, 1)
    for i in range(1, 101):
        output[i] = output[i-1] * x1 + output[i-2] * x2 + np.random.normal(0, 1, 1)
    return output

Series = []
Series.append(outputSeries(0.8, 0))
Series.append(outputSeries(-1.1, 0))
Series.append(outputSeries(1, -0.5))
Series.append(outputSeries(1, 0.5))
Series.append(outputSeries(-0.9, 0))
Series.append(outputSeries(0.9, -0.2))

for item in Series:
    Pk = caculatePk(item, 50, "")
    drawer(item, Pk)

"""
dfname='附录1.4'
input=pd.read_csv('%s.csv'%dfname,header=None)
input.iloc[:,0]=input.iloc[:,0].astype('float')
input=input.values[:,0]

Pk = caculatePk(input, 12, "LB")
LB = caculateLB(Pk, input)
print(Pk)
print(LB)
print((LB[6]))
print((LB[11]))

#statsmodels_lb_test
lb, pvalue = acorr_ljungbox(input, 12)
print(lb)
print((lb[5]))
print((lb[11]))
print(pvalue)

drawer(input, Pk)


dfname='data1.5'
input=pd.read_csv('%s.csv'%dfname,header=None)
input.iloc[:,0]=input.iloc[:,0].astype('float')
input=input.values[:,0]

Pk = caculatePk(input, 12, "LB")
LB = caculateLB(Pk, input)
print(Pk)
print(LB)
print((LB[5]))
print((LB[11]))

#statsmodels_lb_test
lb, pvalue = acorr_ljungbox(input, 12)
print(lb)
print((lb[5]))
print((lb[11]))
print(pvalue)

drawer(input, Pk)

dfname='table2.6'
input=pd.read_csv('%s.csv'%dfname,header=None)
input.iloc[:,0]=input.iloc[:,0].astype('float')
input=input.values[:,0]

Pk = caculatePk(input, 12, "LB")
LB = caculateLB(Pk, input)
print(Pk)
print(LB)
print((LB[5]))
print((LB[11]))

#statsmodels_lb_test
lb, pvalue = acorr_ljungbox(input, 12)
print(lb)
print((lb[5]))
print((lb[11]))
print(pvalue)

drawer(input, Pk)

Yt = np.zeros(len(input)-1)
for i in range(0, len(input)-1):
    Yt[i] = input[i+1] - input[i]

Pk = caculatePk(Yt, 12, "LB")
LB = caculateLB(Pk, Yt)
print(Pk)
print(LB)
print((LB[5]))
print((LB[11]))

#statsmodels_lb_test
lb, pvalue = acorr_ljungbox(Yt, 12)
print(lb)
print((lb[5]))
print((lb[11]))
print(pvalue)

drawer(Yt, Pk)
"""