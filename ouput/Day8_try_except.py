# 1. 写一个程序，让用户输入两个数字并相除
# 2. 使用 try-except 捕获除以0的错误
# 3. 如果出错，提示“除数不能为0”

# one_Num=float(input("请输入数字"))
# two_Num=float(input(str(one_Num)+"除以"))
# try:
#     print("等于"+str(one_Num/two_Num))
# except ZeroDivisionError:
#     print("除数为0，何意味？")

# 让用户输入一个数字，计算它的平方
# 要求：
# - 如果输入的不是数字，提示“请输入数字”
# - 使用 try-except 处理 ValueError
# try:
#     three_Num=input("请输入一个数字")
#     print("它的平方为",str(float(three_Num)**2))
# except ValueError:
#     print("输入的不是数字")

"""
练习3：文件操作 + 异常处理（重点）
改进之前的日记本程序，要求：
读取日记文件时，如果文件不存在，提示“还没有日记，请先写一篇”
不要让程序直接报错崩溃
使用 FileNotFoundError 进行捕获

"""
#查关键字是否包含
# def serchWord(file,keyWord):
#        str=file.read()
#        return bool(str.count(keyWord))

       
# if __name__=="__main__":
#        while True:
#             print("===== 我的日记本 =====\n1. 写日记\n2. 查看日记\n3. 退出\n")
#             str=input("请输入选项：\n").strip()
#             match str:
#                 case "1":
#                         with open(r"diary.txt","a",encoding="utf-8") as file:
#                                  writeDIary=input("请输入日记内容：\n")
#                                  file.write(writeDIary)
                       
#                 case "2":
#                         try:
#                             with open(r"diary.txt","r",encoding="utf-8") as file:
#                                 item=file.readlines()
#                                 for oneList in item:
#                                     print(oneList.rstrip())
#                                 print("文件一共",len(item),"行")#查多少行
#                         except FileNotFoundError:
#                             input("日记不存在请重头开始写作，回车键继续")
#                             pass 
                       
#                 case "3":
#                           print("结束")
#                           break
#                 case _:
#                           print("haha")

"""
练习4：综合小练习
写一个简单的“成绩录入”程序：
让用户输入学生姓名和成绩
成绩必须是 0~100 之间的数字
如果输入错误（不是数字，或超出范围），给出提示并让用户重新输入
使用异常处理完成
"""
stuInfo={}
while True:
    stuName=input("请输入学士姓名")
    stu_Scores=0
    while True:
        try:
            stuScorse=int(input("请输入成绩"))
            if stuScorse>=0 and stuScorse<=100:
                break
            else:
                raise Exception(AssertionError)
        except ValueError:
            print("输入的不是一个数字按")
        except AssertionError:
            print("输入的数字超出正常成绩范围")

    stuInfo.setdefault(stuName,stuScorse)
    isGo=input("是否结束录入按1确定退出,输入其他则继续")
    if isGo=="1":
        break

print(stuInfo)
import csv
with open("studen_Scores.csv","w",encoding="utf-8",newline="") as file:
    # csvWrite=csv.DictWriter(file,fieldnames=list(stuInfo))
    # csvWrite.writeheader()
    # csvWrite.writerow(stuInfo)
    csvWrite=csv.writer(file)
    csvWrite.writerow(["姓名","成绩"])
    for name,score in stuInfo.items():
        csvWrite.writerow([name,score])

