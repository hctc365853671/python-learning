import json
import os

from dotenv import load_dotenv
from openai import OpenAI
import requests

def createClient():
    load_dotenv()
    api_key=os.getenv("QWEN_KEY")
    client = OpenAI(
                        api_key=api_key,  # 请用阿里云百炼 API Key
                        base_url="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
                        
                    )
    return client

def getWeather(city):
    load_dotenv()
    api_code=os.getenv("WEATHER_API_CODE")
    url="https://kztq.market.alicloudapi.com/api/weather/seven/days"
    header={"Authorization":f"APPCODE {api_code}"}
    payload={"city":city}

    try:
        response=requests.post(url=url,data=payload,headers=header)
        return response.json()
    except Exception:
        return {"code":500,"error": "网络似乎有问题"}
    
def getresponse(client:OpenAI,inpt:str):
    messages=[{"role": "user", "content": f"{inpt}"}]
    tools=[{
                    "type": "function",
                    "function": {
                        "name": "getWeather",
                        "description": "查询指定城市未来7天天气预报，入参为城市中文名称，例如：北京",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "city": {
                                    "type": "string",
                                    "description": "需要查询天气的城市中文名称，例如：北京、上海"
                                }
                            },
                            "required": ["city"]
                        }
                    }
                }
            ]
    while True:
        response=client.chat.completions.create(
            model="qwen-plus-2025-07-28",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        msg=response.choices[0].message
        
        if msg.tool_calls:
            messages.append(msg)
            for tool_call in msg.tool_calls:
                tool_name=tool_call.function.name
                tool_args=json.loads(tool_call.function.arguments)
                city=tool_args.get("city")
                if tool_name=="getWeather":
                    tool_result=getWeather(city)
                    print(tool_result)
                    messages.append({
                        "role":"tool",
                        "tool_call_id":tool_call.id,
                        "content":json.dumps(tool_result,ensure_ascii=False)
                    })
        else:
            print("AI回答:"+msg)
            break


getresponse(createClient())

