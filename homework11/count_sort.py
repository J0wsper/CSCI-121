def countSort(someList, m):

    def count(someList):
        countList = []
        index = 0
        while index < m:
            countList.append(0)
            index += 1
        for i in someList:
            countList[i] += 1
        return countList
    
    countList = count(someList)
    sortedList = []

    index = 0
    while index < len(countList):
        sindex = 0
        while sindex < countList[index]:
            sortedList.append(index)
            sindex += 1
        index += 1

    return sortedList