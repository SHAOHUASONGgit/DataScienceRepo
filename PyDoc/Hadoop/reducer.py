import sys
currentKey = None
key = None
currentCount = []
for line in sys.stdin:
    line = line.strip()
    data = line.split()
    key = data[0]
    count = int(data[1])
    if(currentKey == key):  # 如果当前键相同，则追加
        currentCount.append(count)
    else:
        if(currentKey == None):  # 初始化
            currentKey = key
            currentCount.append(count)
        else:
            if(-1 in currentCount):  # 如果有-1，那么就不输出，并重置
                currentKey = key
                currentCount.clear()
                currentCount.append(count)
            else:  # 如果没有，则输出后再重置
                print("Recommend:"+currentKey+"\t"+"Mutual Friends:"+str(currentCount))
                currentKey = key
                currentCount.clear()
                currentCount.append(count)
if(-1 in currentCount):  # 最后一行
    pass
else:
    print("Recommend:"+currentKey+"\t"+"Mutual Friends:"+currentCount)