import numpy as np


def getgi(phi, n=20):
    gi = np.zeros((n))
    gi[0] = 1

    power = len(phi) - 1
    for j in range(1, 20):
        if (j <= power):
            sum = 0
            i = 1
            while (i <= j):
                sum = sum + phi[i] * gi[j - i]
                i = i + 1
            gi[j] = sum
        else:
            sum = 0
            i = 1
            while (i <= power):
                sum = sum + phi[i] * gi[j - i]
                i = i + 1
            gi[j] = sum

    return gi


phi=np.array([0,0.8,-0.64])
mygi=getgi(phi)
print('Green:',mygi)
print((mygi**2).sum())