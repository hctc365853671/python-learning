import requests,os
from dotenv import load_dotenv
# 访问一个测试接口
# response = requests.get("https://httpbin.org/get")
# print(response.status_code)
# print(response.json())
# # 访问 https://httpbin.org/get?name=张三&age=25
# 并打印返回结果
# other_response=requests.get("https://httpbin.org/get?name=张三&age=25")
# print(other_response)
# 向 https://httpbin.org/post 发送一个 JSON 数据
# 内容为：{"name": "洪晨", "message": "你好"}
# response=requests.post("https://httpbin.org/post",json={"name": "洪晨", "message": "你好"})
# print(response)
"""
练习4：综合小练习
写一个小程序：
输入一个城市名
调用一个公开的天气接口或测试接口（可用 httpbin）
打印返回的信息
加上异常处理（网络错误、超时等）
如果天气接口不好找，就用 https://httpbin.org 做测试即可。
"""


def postWeather(city):
    load_dotenv()
    api_code=os.getenv("WEATHER_API_CODE")
    url="https://kztq.market.alicloudapi.com/api/weather/seven/days"
    header={"Authorization":f"APPCODE {api_code}"}
    payload={"city":city}

    try:
        response=requests.post(url=url,data=payload,headers=header)
        return response.json()
    except Exception:
        print("网络似乎有问题")


if __name__=="__main__":
    huangshiWeather=postWeather("黄石")
    print(huangshiWeather)