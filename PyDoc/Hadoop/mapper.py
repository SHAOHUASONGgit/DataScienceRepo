import sys
for line in sys.stdin:
    line = line.strip()
    data = line.split('\t')
    if len(data)==2:  # 如果用户有好友
        user = data[0]
        friends = data[1].split(',')
        for firstPointer in range(len(friends)):
            print(user + "," + friends[firstPointer] + "\t" + "-1")  # 已经是好友了
            for secondpointer in range(len(friends)):
                if firstPointer!=secondpointer:
                    print(friends[firstPointer] + "," + friends[secondpointer] + "\t" + user)  # 输出所有可能的朋友组合