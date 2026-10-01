"""
二、综合练习项目（120分钟）——重点
项目名称：简易学生信息管理系统
请完成以下功能：
定义类
父类 Person：姓名、年龄
子类 Student：继承 Person，增加成绩、学校
功能要求
可以添加学生信息
可以查看所有学生
可以保存到 JSON 或 CSV 文件
可以读取已保存的文件
使用异常处理，防止程序崩溃
用菜单方式操作（输入数字选择功能）
菜单示例
===== 学生信息管理系统 =====
1. 添加学生
2. 查看所有学生
3. 保存到文件
4. 从文件读取
5. 退出
请输入选项：
加分项（可选）
按成绩排序显示
查找某个学生
删除学生
"""
class Person:#人物类
    def __init__(self,name,age):
        self.name=name
        self.age=age

class Student(Person):#学生类
    def __init__(self, name, age,result,school):
        super().__init__(name, age)
        self.result=result
        self.school=school

class stuManagSys:#学生系统管理类
    def __init__(self):
        self.allInfo=[]

    def addStu(self,stu:Student):#添加学生
        self.allInfo.append({"姓名":stu.name,"年龄":stu.age,"成绩":stu.result,"学校":stu.school})

    def showAllstu(self):#显示所有的学生
        print(self.allInfo)
        input("任意键继续")

    def saveToJson(self):#保存到文件
        import json
        with open("stuInfo.json","w",encoding="utf-8") as file:
            json.dump(self.allInfo,file,ensure_ascii=False)

    def loadAllstu(self):#读取到文件
        import json
        try:
            with open("stuInfo.json","r",encoding="utf-8") as file:
                self.allInfo=json.load(file)
                self.showAllstu()
                
        except FileExistsError:
            input("文件不存在")

    def resultSort(self):#按成绩排序
        self.allInfo=sorted(self.allInfo,lambda x:x["成绩"])
        input("排序成功")

    def findStu(self,name):#查找学生
        for i in self.allInfo:
            if i["姓名"]==name:
                return i
            else:
                return None

    def delStu(self,name):#删除学生
        for i in self.allInfo:
            if i["姓名"]==name:
                self.allInfo.remove(i)
                input("删除成功")
            else:
                input("没有这个学生")

if __name__=="__main__":
    dealstuInfo=stuManagSys()
    while True:
        inputStr=input("菜单示例\n===== 学生信息管理系统 =====\n1. 添加学生\n2. 查看所有学生\n3. 保存到文件\n4. 从文件读取\n5. 按成绩排序\n6. 查找学生\n7. 删除学生\n8. 退出")
        match inputStr:
            case "1":
                name=input("姓名")
                while True:
                    try:
                        age=int(input("年龄"))
                        if age<=0 or age>=120:
                            raise Exception
                        break
                    except Exception:
                        input("输入有误,请重新输入")
                while True:
                    try:
                        result=int(input("成绩"))
                        if result<=0 or result>=100:
                            raise Exception
                        break
                    except Exception:
                        input("输入有误,请重新输入")
                school=input("学校")
                dealstuInfo.addStu(Student(name,age,result,school))
                input("添加成功")
            case "2":
                dealstuInfo.showAllstu()
            case "3":
                dealstuInfo.saveToJson()
            case "4":
                dealstuInfo.loadAllstu()
            case "5":
                dealstuInfo.resultSort()
            case "6":
                name=input("姓名")
                oneStu=dealstuInfo.findStu(name)
                if oneStu==None:
                    input("没有该学生")
                else:
                    print(oneStu)
                    input("已找到学生")
            case "7":
                name=input("姓名")
                dealstuInfo.delStu(name)
            case "8":
                break

