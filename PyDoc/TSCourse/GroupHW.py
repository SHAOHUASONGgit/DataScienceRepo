import matplotlib.pyplot as plt
import pandas as pd

def caculatediff(diff, step, input):
    if(step!=0):
        input = input[step:] - input[:-step]
    if (diff == 0):
        return input
    input = input[1:] - input[:-1]
    return caculatediff(diff - 1, 0, input)

def drawer(input):
    plt.plot(input, '*-')
    plt.show()
    plt.close()

filename = "tw1.csv"
series = pd.read_csv(filename, header=None)
series.iloc[:, 0] = series.iloc[:, 0].astype("float")
series = series.values[:, 0]