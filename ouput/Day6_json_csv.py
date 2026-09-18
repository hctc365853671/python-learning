"""
练习1：JSON 基础读写
创建一个字典，包含自己的信息（姓名、年龄、爱好列表等）
把它写入 my_info.json 文件
再读取这个文件并打印内容
练习2：JSON 稍复杂一点
准备一个包含多个学生信息的列表（每个学生是一个字典）
写入 students.json
读取后，打印出所有学生的姓名和成绩
练习3：CSV 基础读写
创建一个 scores.csv 文件，写入表头和几行学生成绩数据
读取这个 CSV 文件，并逐行打印
尝试只打印“姓名”和“总分”两列
练习4：综合小练习（重点）
写一个小程序，实现以下功能：
把之前日记本里的内容，或者自己编的几条数据，保存成 JSON 格式
再把同样的数据保存成 CSV 格式
分别读取这两种文件并打印，对比一下区别
可选挑战：
读取 CSV 后，计算某一列的平均分
把 JSON 数据转换成 CSV 保存
"""
# import json
# myInfo={"姓名":"洪晨","年龄":32,"爱好":"游戏"}
# with open("my_info.json","w",encoding="utf-8") as file:
#     json.dump(myInfo,file)

# with open("my_info.json","r",encoding="utf-8") as file:
#     jsonInfo=json.load(file)
#     print(jsonInfo)
# import json
# stuInfo=[{"姓名":"洪晨","年龄":32,"爱好":"游戏"},
#          {"姓名":"洪辉","年龄":27,"爱好":"跑步"},{"姓名":"罗雷","年龄":31,"爱好":"游戏"}]
# with open("students.json","w",encoding="utf-8") as file:
#         json.dump(stuInfo,file)

# with open("students.json","r",encoding="utf-8") as file:
#         print(json.load(file))

# import csv
# with open("scores.csv","w",encoding="gbk",newline="") as file:
#     csvWriter=csv.writer(file)
#     csvWriter.writerow(["姓名\\学科","语文","数学","英文","理综","总分"])
#     csvWriter.writerow(["洪晨",105,115,38,165,423])
#     csvWriter.writerow(["洪辉",103,115,107,211,536])
#     csvWriter.writerow(["罗磊",80,64,44,69,197])

# with open("scores.csv","r",encoding="gbk",newline="") as file:
#     csvRead=csv.DictReader(file)
#     print("姓名:总分")
#     for scorse in csvRead:
#         print(scorse["姓名\\学科"]+":"+scorse["总分"])

import json,csv
stuInfo=[{"姓名":"洪晨","年龄":32,"爱好":"游戏"},
         {"姓名":"洪辉","年龄":27,"爱好":"跑步"},{"姓名":"罗雷","年龄":31,"爱好":"游戏"}]
with open("students.json","w",encoding="utf-8") as file:
        json.dump(stuInfo,file)
with open("students.json","r",encoding="utf-8") as file:
        suInfo=json.load(file)
        print(suInfo)
with open("students.csv","w",encoding="utf-8",newline="") as file:
        fileHead=list(suInfo[0])
        print(fileHead)
        csvWriter=csv.DictWriter(file,fieldnames=fileHead)
        csvWriter.writeheader()
        for s in suInfo:
            csvWriter.writerow(s)
with open("students.csv","r",encoding="utf-8",newline="") as file:
        csvRead=csv.DictReader(file)
        allAge=[cr["年龄"]for cr in csvRead]
        sumAge=0
        print(allAge)
        for age in allAge:
               sumAge+=int(age)
        averageAge=sumAge/len(allAge)
        print("平均年龄为:",str(averageAge))