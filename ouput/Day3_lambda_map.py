# 1. 写一个lambda，计算两个数的和
# 2. 写一个lambda，判断一个数是不是偶数
# 3. 写一个lambda，返回字符串的长度
twoSum=lambda a,b:a+b
isEven=lambda a:a%2==0
strLenth= lambda str:len(str)


numbers = [1, 2, 3, 4, 5, 6]

# 1. 用map把每个数字翻倍
# 2. 用map把每个数字转成字符串
# 3. 用map计算每个数字的平方
n1=list(map(lambda x:x*2,numbers))
n2=list(map(lambda x:str(x),numbers))
n3=list(map(lambda x:x**2,numbers))

numbers1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 1. 过滤出所有偶数
# 2. 过滤出所有大于5的数
# 3. 过滤出所有奇数
"""
n4=[num for num in numbers1 if num%2==0]
n5=[num for num in numbers1 if num>5]
n6=[num for num in numbers1 if num%2!=0]
"""
n4=list(filter(lambda x:x%2==0,numbers1))
n5=list(filter(lambda x:x>5,numbers1))
n6=list(filter(lambda x:x%2!=0,numbers1))

students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五六", "score": 78}
]

# 1. 按成绩从高到低排序
# 2. 按成绩从低到高排序
# 3. 按名字长度排序
n7=sorted(students,key=lambda x:x["score"])
n8=sorted(students,key=lambda x:x["score"],reverse=True)
n9=sorted(students,key=lambda x:len(x["name"]),reverse=True)

names = ["张三", "李四", "王五"]
scores = [85, 92, 78]

# 1. 用zip把名字和成绩配对
# 2. 把配对结果转成字典

genratorScores=zip(names,scores)
allScores=dict(genratorScores)

data = [3, 1, 4, 1, 5, 9, 2, 6]

# 要求：
# 1. 先过滤出偶数
# 2. 再把这些偶数翻倍
# 3. 最后按从大到小排序
# 尽量用 lambda + map + filter + sorted 组合完成

data=list(filter(lambda x:x%2==0,data))
data=list(map(lambda x:x*2,data))
data=list(sorted(data,key=None,reverse=True))
print(data)
