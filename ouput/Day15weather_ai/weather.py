import requests,os
from dotenv import load_dotenv
def postWeather(city):
    load_dotenv()
    api_code=os.getenv("WEATHER_API_CODE")
    url="https://kztq.market.alicloudapi.com/api/weather/one/forty"
    header={"Authorization":f"APPCODE {api_code}"}
    payload={"city":city}

    try:
        response=requests.post(url=url,data=payload,headers=header)
        return response.json()
    except Exception:
        print("网络似乎有问题")