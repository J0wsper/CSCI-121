def selectionSort(someList):
    
    def subSort(someList):
        if someList == []:
            return []
        else:
            minimum = someList[0]
            index = 0
            position = 0
            while index < len(someList):
                if someList[index] < minimum:
                    minimum = someList[index]
                    position = index
                index += 1
            
            placeholder = someList[0]
            someList[position] = placeholder
            return [minimum]+subSort(someList[1:])
    
    return subSort(someList)

    


