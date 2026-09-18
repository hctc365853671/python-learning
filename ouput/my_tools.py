def getSum(a,b):
    return a+b

def isEven(a):
    return a%2==0

def getStrLenth(str):
    return len(str)

def getDouble(item):
    return list(map(lambda x:x*2,item))

def filterEven(item):
    return list(filter(lambda x:x%2==0,item))

def getSort(item):
    return sorted(item,key=lambda x:x)


if __name__=="__main__":
    print(getSum(5,9))