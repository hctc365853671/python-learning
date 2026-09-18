# 1. 创建一个文件 test.txt，写入一句话：“这是我的第一行文件内容”
# 2. 读取这个文件并打印内容
# 3. 向文件追加一句话：“这是追加的内容”
# 4. 再次读取并打印全部内容

# with open(r".\.test.txt","w",encoding="utf-8") as file:
#         file.write("这是我的第一行文件内容")

# with open(r".\.test.txt","r",encoding="utf-8") as file:
#         print(file.read())

# with open(r".\.test.txt","a",encoding="utf-8") as file:
#         file.write("这是追加的内容\n1.创建一个文件 test.txt,写入一句话：“这是我的第一行文件内容”\n2.读取这个文件并打印内容\n3.向文件追加一句话：“这是追加的内容”\n4.再次读取并打印全部内容")

# with open(r".\.test.txt","r",encoding="utf-8") as file:
#         print(file.read())


# 准备一个多行文本文件（自己先写入几行）
# 1. 用 readlines() 读取所有行并打印
# 2. 用 for 循环逐行读取并打印（推荐方式）

# with open(r".\.test.txt","r",encoding="utf-8") as file:
#         item=file.readlines()
#         print(item)
#         for oneList in item:
#             print(oneList.rstrip())

"""
练习3：日记本程序（重点）
写一个简单的「日记本」程序，要求具备以下功能：
提示用户输入今天的日记内容
把内容追加保存到 diary.txt 文件中（每次记录带上当前时间）
可以查看历史日记（读取并打印全部内容）
用菜单方式实现（例如输入1写日记，输入2查看日记，输入3退出）
参考菜单效果：
===== 我的日记本 =====
1. 写日记
2. 查看日记
3. 退出
请输入选项：
"""
#查关键字是否包含
def serchWord(file,keyWord):
       str=file.read()
       return bool(str.count(keyWord))

       
if __name__=="__main__":
       while True:
            print("===== 我的日记本 =====\n1. 写日记\n2. 查看日记\n3. 退出\n")
            str=input("请输入选项：\n").strip()
            match str:
                case "1":
                        with open(r"D:\tool\vs_vode\workspace\diary.txt","a",encoding="utf-8") as file:
                                 writeDIary=input("请输入日记内容：\n")
                                 file.write(writeDIary)
                       
                case "2":
                        with open(r"D:\tool\vs_vode\workspace\diary.txt","r",encoding="utf-8") as file:
                                item=file.readlines()
                                for oneList in item:
                                    print(oneList.rstrip())
                                print("文件一共",len(item),"行")#查多少行
                        
                case "3":
                          print("结束")
                          break
                case _:
                          print("haha")