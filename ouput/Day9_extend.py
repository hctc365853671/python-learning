# 1. 定义一个父类 Person，包含姓名和年龄，以及一个介绍自己的方法
# 2. 定义一个子类 Student，继承 Person
# 3. 在 Student 中新增“学校”属性，并重写介绍方法
# 在 Student 的 __init__ 方法中，使用 super() 调用父类的初始化
# 然后再添加自己的属性
# class Person:
#     def __init__(self,name,age):
#         self.name:str=name
#         self.age:int=age

#     def introduceSelf(self):
#         print("姓名:"+self.name+",年龄:"+str(self.age))


# class Student(Person):
#     def __init__(self,name,age,schcool):
#         super().__init__(name,age)
#         self.schcool=schcool

#     def introduceSelf(self):
#         super().introduceSelf()
#         print("学校为:"+self.schcool)


# stu=Student("洪晨",31,"三中")
# stu.introduceSelf()
"""
练习3：综合练习（重点）
设计一个简单的“员工管理系统”：
定义父类 Employee（员工）
属性：姓名、工号
方法：显示基本信息
定义子类 Manager（经理），继承 Employee
新增属性：管理的部门
重写显示信息的方法
定义子类 Developer（程序员），继承 Employee
新增属性：擅长的编程语言
重写显示信息的方法
创建几个对象并调用方法，测试继承效果
"""
# class Employee:
#     def __init__(self,name,workNum):
#        self.name:str=name
#        self. workNum:int=workNum

#     def introduceSelf(self):
#         print("姓名:"+self.name+",年龄:"+str(self.workNum),end="")

# class Manager(Employee):
#     def __init__(self,name,workNum,depart):
#         super().__init__(name,workNum)
#         self.depart=depart

#     def introduceSelf(self):
#         super().introduceSelf()
#         print("部门"+self.depart,end="")

# class Developer(Employee):
#     def __init__(self, name, workNum,programLag):
#         super().__init__(name, workNum)
#         self.programLag=programLag

#     def introduceSelf(self):
#         super().introduceSelf()
#         print("擅长"+self.programLag,end="")


# manager=Manager("洪晨",106,"交付部")
# manager.introduceSelf()
# programer=Developer("洪亮",657,"python")
# programer.introduceSelf()

class Person:
    def __init__(self):
        self.informa={}#录入数据初始为空字典

    def inputInformation():
        print("开始录入信息")

class Student(Person):
    def __init__(self):
        super().__init__()

    def inputInformation(self):
        while True:
            stuName=input("请输入学生姓名")
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
                except Exception:
                    print("输入的数字超出正常成绩范围")

            self.informa.setdefault(stuName,stuScorse)
            isGo=input("是否结束录入按1确定退出,输入其他则继续")
            if isGo=="1":
                break

        print(self.informa)
        import csv
        with open("studen_Scores.csv","w",encoding="utf-8",newline="") as file:
            # csvWrite=csv.DictWriter(file,fieldnames=list(stuInfo))
            # csvWrite.writeheader()
            # csvWrite.writerow(stuInfo)
            csvWrite=csv.writer(file)
            csvWrite.writerow(["姓名","成绩"])
            for name,score in self.informa.items():
                csvWrite.writerow([name,score])


stus=Student()
stus.inputInformation()
