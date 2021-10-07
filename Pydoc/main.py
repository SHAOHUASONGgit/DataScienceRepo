import statsmodels.tsa.api as smt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def drawts(y,pname):
    ##draw ax
    fig = plt.figure(figsize=(10,8))
    ts_ax=plt.subplot2grid((2,2),(0,0),colspan=2)
    acf_ax=plt.subplot2grid((2,2),(1,0))
    pacf_ax=plt.subplot2grid((2,2),(1,1))
    ##draw plot
    ts_ax.plot(y,'*-')
    ts_ax.set_title('Time Series Analysis Plots')
    smt.graphics.plot_acf(y,lags=None,ax=acf_ax,alpha=0.05) ##2sigma
    smt.graphics.plot_pacf(y,lags=None,ax=pacf_ax,alpha=0.05)  ##2sigma
    #plt.savefig('%s.jpg'%pname,dpi=256)
    plt.show()
    plt.close()


def mydrawts(y, pname, kstep):
    myname = 'SHAO_HUASONG'
    ##draw ax
    fig = plt.figure(figsize=(10, 8))
    ts_ax = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    acf_ax = plt.subplot2grid((2, 2), (1, 0))
    pacf_ax = plt.subplot2grid((2, 2), (1, 1))
    ##draw plot
    ts_ax.plot(y, '*-')
    ts_ax.set_title('Time Series Analysis Plots(custom %s)' % myname)

    ##calclate acf
    myacf = np.ones((kstep))
    N = len(y)
    u = y.mean()
    for k in range(0 , kstep):
        upsum = 0
        downsum = 0
        for i in range (0 , N-k):
            upsum += (y[i] - u) * (y[i + k] - u)
        for i in range (0 , N):
            downsum += (y[i] - u) ** 2
        #print((upsum / downsum))#第一个值应当为1，输出检查
        myacf[k] = (upsum / downsum)
    print(myacf)

    #k=0
    #while (k!=17):
        #yk=0
        #y0=0
        #n=len(y)
        #x_=np.sum(y)/n
        #xt=y[0:n-k]
        #xt_k=y[k:n-1]
        #i=0
        #while (i!=(n-k-1)):
        #    yk=yk+((xt[i]-x_)*(xt_k[i]-x_))/(n-k-1)
        #    i=i+1
        #j = 0
        #while (j!=(n-1)):
        #    y0=y0+((y[j]-x_)*(y[j]-x_))/(n-1)
        #    j=j+1
        #myacf[k]=yk/y0
        #k+=1


    twosigma = np.ones((kstep))
    #sum = 0
    n = len(y)
    twosigma[0] = ((1 / n) ** 0.5)
    for i in range(1 , kstep):
        sum = 0
        for j in range(0 , i):
            sum += myacf[j] ** 2
        twosigma[i] = (((1 / n) * (1 + 2 * sum)) ** 0.5)
        #sum = 0

    acf_ax.bar(range(len(myacf)), myacf)
    acf_ax.fill_between(range(len(myacf)), -1 * twosigma, twosigma, color='lightblue')

    # plt.savefig('%s.jpg'%pname,dpi=256)
    plt.show()
    plt.close()

dfname='附录1.2'
y=pd.read_csv('%s.csv'%dfname,header=None)
y.iloc[:,0]=y.iloc[:,0].astype('float')
y=y.values[:,0]
drawts(y,dfname)
mydrawts(y,dfname,17)

##read data
dfname='附录1.3'
y=pd.read_csv('%s.csv'%dfname,header=None)
y.iloc[:,0]=y.iloc[:,0].astype('float')
y=y.values[:,0]
drawts(y,dfname)
mydrawts(y,dfname, 24)

##read data
dfname='附录1.4'
y=pd.read_csv('%s.csv'%dfname,header=None)
y.iloc[:,0]=y.iloc[:,0].astype('float')
y=y.values[:,0]
drawts(y,dfname)
mydrawts(y,dfname, 18)