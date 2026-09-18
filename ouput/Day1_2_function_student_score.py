# import keyword
# #! 输出年龄
# age=5
# print(age)
# # 输出关键字
# print(keyword.kwlist)
# if True:
#     print ("True")#缩进必须和下面保持一致
# else:
#     print ("False")
# print(1+1+2\
#       +2+5)
# length=[1,2,3,4,5
        
#         ,6,7,8,9]
# print(length)
# num=1+2j
# print(num.__class__)
# numb_in=2
# numb_fl=1.23
# print(type(numb_in))
# print(type(numb_fl))    
# print(type(numb_in+numb_fl))
# num_it=13
# str="123"
# print(num_it+str)# This will raise a TypeError because you cannot add an integer and a string in Python
# print(int(1.9))
# print(int("123"))
# # print(int("123sdafiuj"))
# print(int(1+2j))# This will raise a TypeError because you cannot convert a complex number to an integer
# class A:
#     pass
# class B(A):
#     pass
# print(isinstance(B(),A))
# def invrt(str):
#     oneList=str.split(" ")
#     print(oneList)
#     oneStr=" ".join(oneList[-1::-1])
#     return oneStr
# if __name__=="__main__":
#     str1=invrt("i love runmbb")
#     print(str1)
# print("结束")
#函数练习
# x=int("3",10)#第二参数为进制数，当输入第二个参数时，第一个参数必须是字符串类型
# print(x)
# x=float("6.98")
# print(x)
# x=complex(1.3,2.5)
# print(x)
# x=str("hello world")
# y=repr("hello world")
# print(x)# 输出字符串
# print(y)# 输出字符串的表示形式
# print(eval("3+5"))# 输出表达式的值
# print(eval("pow(2,3)"))# 输出表达式的值
# print(eval("'3+5'"))# 输出表达式的值
# x={"one":1,"two":2,"three":3}
# y=(1,"asdoifj",3.14)
# z={1,"oij",3.14,b"asdoifj"}
# a=[1,"oijioj",1.9,3.14]
# print(tuple(x))# 输出字典的键
# print(tuple(y))# 输出元组
# print(tuple(z))# 输出集合
# print(tuple(a))# 输出列表
# print(list(x))# 输出字典的键
# print(list(y))# 输出元组
# print(list(z))# 输出集合q  
# print(list(a))# 输出列表
# print(set(x))# 输出字典的键
# print(set(y))# 输出元组
# print(set(z))# 输出集合
# print(set(a))# 输出列表  
# print(set("sdfewr"))
'''
x=dict(one=1,two=2,three=3,var=4)
print(x)
y=dict([("one",1),("two",2),("three",3),("var",4)])
print(y)
'''
'''
class Person:
    """人物类"""
    def famliyName():
        """家族名"""
        return "洪"

import inspect
print(Person.__doc__)
print(Person.famliyName.__doc__)
print(inspect.getdoc(Person))
'''
#位运算
# a=13 #0000 1101
# b=31 #0001 1111
# print(a>>2)
# print(b<<4)
# if (n:=10)>5:
#     print(n)
# print("\a")
# import time
# print(range(100))
# for i in range(101): # 添加进度条图形和百分比
#     bar = '[' + '=' * (i // 2) + ' ' * (50 - i // 2) + ']'
#     print(f"\r{bar} {i:3}%", end='', flush=True)
#     time.sleep(0.05)
# # print()
# print("我叫%s,今年%d岁"%("小闵",10))
# class stuScore:
#     allScore={}
#     def ScoreRegistration(self,oneName,someScore):#录入学生成绩
#         name=oneName
#         score={}
#         oneList=someScore.strip().split(",")
#         for i in oneList:
#             item=i.strip().split(":")
#             score.setdefault(item[0],item[1])
#         self.allScore.setdefault(name,score)

#     def modifyScore(self,oneName,someScore):
#         oneDict=self.allScore[oneName]
#         oneList=someScore.strip().split(",")
#         for i in oneList:
#             item=i.strip().split(":")
#             oneDict[item[0]]=item[1]

#     def checkResults(self,oneName):
#         for key in self.allScore:
#             if oneName==key:
#                 print("成绩为"+str(self.allScore[key])+"分")
#                 break
#         else:
#             print("没有这个学生信息")

#     def delResults(self,oneName):
#         for key in self.allScore:
#             if oneName==key:
#                 del self.allScore[key]
#                 print("删除成功")
#                 break
#         else:
#             print("没有这个学生信息")

# manager=stuScore()
# manager.ScoreRegistration("洪辰","语文:90,数学:80,英语:100")
# manager.ScoreRegistration("罗雷","语文:60,数学:70,英语:30")
# manager.ScoreRegistration("洪辉","语文:96,数学:100,英语:103")
# print(manager.allScore)
# manager.modifyScore("洪辰","语文:103,数学:115,英语:38")
# manager.modifyScore("罗雷","语文:91,数学:83")
# print(manager.allScore)
# manager.checkResults("洪辉")
# manager.delResults("罗雷")
# print(manager.allScore)
# d={"hc":1,"ll":4,"hy":7}
# print(list(d))
# print(input("输入："))
# print("好了")

        