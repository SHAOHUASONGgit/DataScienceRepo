import numpy as np
from collections import  Counter

group = np.array([[1.0 , 1.1] , [1.0 , 1.0] , [0 , 0] , [0 , 0.1]])
labels = ['A' , 'A' , 'B' , 'B']

def classify(input, group, labels, k):
    distance = np.zeros(len(group)) #距离数组
    for i in range(len(group)):
        distance[i] = sum(((group[i] - input) ** 2)) ** 0.5 #计算距离
    z = zip(distance , labels) #合并排序
    z = sorted(z , reverse=False) #False升序排列
    distance , labels = zip(*z)
    pre = sorted(Counter(labels[:k]).items() , key = lambda x: x[1], reverse=True)
    return pre[0][0]

print(classify([0,0] , group , labels, 3))