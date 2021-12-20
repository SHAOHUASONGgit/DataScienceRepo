import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.tsa.api as smt
import statsmodels.api as sm

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

def drawcompare(series, prediction):
    plt.plot(series, "*-", label='observe')
    plt.plot(prediction, label='fittes')
    plt.legend()
    plt.show()
    plt.close()

filename = "table_a1.16.csv"
series = pd.read_csv(filename, header=None)
series.iloc[:, 0] = series.iloc[:, 0].astype("float")
series = series.values[:, 0]
drawer(series)

x = np.arange(1, len(series) + 1)
x2times = x ** 2

model = sm.OLS(series, sm.add_constant(x))
model = model.fit()
print(model.summary())
prediction = model.predict(sm.add_constant(x))
drawcompare(series, prediction)

model = sm.OLS(series, sm.add_constant(x2times))
model = model.fit()
print(model.summary())
prediction = model.predict(sm.add_constant(x2times))
drawcompare(series, prediction)

xx2times = np.c_[x, x2times]
model = sm.OLS(series, sm.add_constant(xx2times))
model = model.fit()
print(model.summary())
prediction = model.predict(sm.add_constant(xx2times))
drawcompare(series, prediction)