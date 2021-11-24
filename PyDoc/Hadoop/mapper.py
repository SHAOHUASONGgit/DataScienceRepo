import sys
for line in sys.stdin:
    line = line.strip()
    data = line.split()
    if len(data)==2:
        user = data[0]
        friends = data[1].split(',')
        for firstPointer in range(len(friends)):
            for secondpointer in range(len(friends)):
                if firstPointer!=secondpointer:
                    print(friends[firstPointer]+","+"r="+friends[secondpointer]+"    "+user)