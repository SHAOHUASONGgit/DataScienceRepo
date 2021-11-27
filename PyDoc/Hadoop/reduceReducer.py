import sys
currentUser1 = None
currentUser2 = None
user1 = None
user2 = None
mutualCount = []
outputStream = []
for line in sys.stdin:
    line = line.strip()
    data = line.split()
    user12 = data[0].split(',')

    user1 = int(user12[0])
    user2 = int(user12[1])
    mutualUser = int(data[1])
    if(currentUser1 == user1):
        if(currentUser2 == user2):
            mutualCount.append(mutualUser)
        elif(-1 in mutualCount):
            mutualCount.clear()
            currentUser2 = user2
            mutualCount.append(mutualUser)
        else:
            outputStream.append([currentUser2, mutualCount.copy()])
            mutualCount.clear()
            currentUser2 = user2
            mutualCount.append(mutualUser)
    else:
        if(currentUser1 == None):
            currentUser1 = user1
            currentUser2 = user2
            mutualCount.append(mutualUser)
            outputStream.append(currentUser1)
        else:
            if(-1 in mutualCount):
                if(len(outputStream)==1):
                    currentUser1 = user1
                    currentUser2 = user2
                    outputStream.clear()
                    mutualCount.clear()
                    mutualCount.append(mutualUser)
                    outputStream.append(currentUser1)
                else:
                    output = "Recommend for user:" + str(outputStream[0]) + "\t"
                    for data in outputStream[1:]:
                        output = output + str(data[0]) + "(" + str(len(data[1])) + ":" + str(data[1]) + ") "
                    print(output)
                    currentUser1 = user1
                    currentUser2 = user2
                    outputStream.clear()
                    mutualCount.clear()
                    mutualCount.append(mutualUser)
                    outputStream.append(currentUser1)
            else:
                outputStream.append([currentUser2, mutualCount.copy()])
                output = "Recommend for user:" + str(outputStream[0]) + "\t"
                for data in outputStream[1:]:
                    output = output + str(data[0]) + "(" + str(len(data[1])) + ":" + str(data[1]) + ") "
                print(output)
                currentUser1 = user1
                currentUser2 = user2
                mutualCount.clear()
                outputStream.clear()
                mutualCount.append(mutualUser)
                outputStream.append(currentUser1)
if(-1 in mutualCount):
    if(len(outputStream)==1):
        pass
    else:
        output = "Recommend for user:" + str(outputStream[0]) + "\t"
        for data in outputStream[1:]:
            output = output + str(data[0]) + "(" + str(len(data[1])) + ":" + str(data[1]) + ") "
        print(output)