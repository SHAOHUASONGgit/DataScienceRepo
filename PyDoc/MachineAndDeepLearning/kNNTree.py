from math import log

dataset = [
    [1 , 1 , 'yes'] ,
    [1 , 1 , 'yes'] ,
    [1 , 0 , 'no'] ,
    [0 , 1 , 'no'] ,
    [0 , 1 , 'no']
]
labels = ['surfacing' , 'flippers']

def Shannon(dataset , indexin):#计算信息熵
    times = {}
    output = 0
    for data in dataset:
        if data[indexin] not in times.keys():#{}.keys()：键的集合
            times[data[indexin]] = 0.0
        times[data[indexin]] += 1
    for key in times:
            prob = times[key] / len(dataset)
            output += prob * log(prob , 2)
    return abs(output)

def splitdata(dataset , indexin , value):#输入dataset，按照dataset[indexin]是否等于value对列表进行分解，即按照indexin对应特征进行区分
    output = []
    for data in dataset:
        if data[indexin] == value:
            splitindexin = data.copy()
            del splitindexin[indexin]
            output.append(splitindexin)
    return output

def calbestinfo(dataset , labels):
    features = {} #存储特征对应信息增益
    totalShannon = Shannon(dataset , -1) #总信息熵
    for label in labels: #取labels中的一个特征label
        samples = []
        splitShannon = []
        features[label] = 0
        for data in dataset: #获取特征label在数据集dataset中的所有取值，存储于samples[]中
            if data[labels.index(label)] not in samples:
                samples.append(data[labels.index(label)])
        for tag in samples: #对特征label的每个取值进行如下操作
            splitIt = splitdata(dataset , labels.index(label) , tag) #根据数据集dataset中特征label的取值tag对数据集dataset进行分割
            result = Shannon(splitIt , 0) #计算对应熵值
            splitShannon.append(result * len(splitIt) / len(dataset))
        features[label] = totalShannon - sum(splitShannon)
    features = sorted(features,reverse=True)
    return labels.index(features[0])


def majority(listin):
    times = {}
    for data in listin:
        if data[-1] not in times.keys():
            times[data[-1]] = 0
        times[data[-1]] += 1
    times = sorted(times, reverse=True)
    return times[0]

def createtree(dataset , labelin):
    label = labelin.copy()
    classlist = [data[-1] for data in dataset]
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    if len(dataset[0]) == 1:
        return majority(classlist)
    bestlabel = calbestinfo(dataset , label)
    best = label[bestlabel]
    mytree = {best:{}}
    del label[bestlabel]
    featvalues = [data[bestlabel] for data in dataset]
    uni = set(featvalues)
    for value in uni:
        sub = labels[:]
        mytree[best][value] = createtree(splitdata(dataset, bestlabel, value), sub)
    return mytree

def classify(tree, labels, data):
    firstStr = list(tree.keys())[0]
    subDict = tree[firstStr]
    featindex = labels.index(firstStr)
    for key in subDict.keys():
        if data[featindex] == key:
            if type(subDict[key]).__name__=='dict':
                classlabel = classify(subDict[key], labels, data)
            else:
                classlabel = subDict[key]
    return classlabel

mytree = createtree(dataset, labels)
print(classify(mytree, labels, [1,0]))
print(classify(mytree, labels, [1,1]))