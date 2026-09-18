# 1. 导入 math 模块，计算 16 的平方根
# 2. 导入 random 模块，随机生成 1\~100 的整数
# 3. 导入 datetime 模块，打印当前日期和时间
from datetime import datetime
import math,random
print(math.sqrt(16))
i=int(random.random()*-101)
print(datetime.now())

# 练习2：创建自己的模块
# 新建一个文件，命名为 my_tools.py
# 把之前写过的几个函数放进去，例如：
# 判断奇偶的函数
# 字符串反转函数
# 计算两个数之和的函数（用普通函数或 lambda 都可以）
# 在 my_tools.py 里加上测试代码（用 if __name__ == "__main__": 包裹）


# 练习3：在其他文件中调用自己的模块
# 新建另一个文件，命名为 main.py
# 在 main.py 中导入 my_tools 模块
# 调用里面的函数并打印结果
# 尝试用不同的导入方式（import 和 from ... import）


# 练习4：综合小练习
# 把第三天写的 map / filter / sorted 相关功能，也整理进 my_tools.py，然后在 main.py 里调用