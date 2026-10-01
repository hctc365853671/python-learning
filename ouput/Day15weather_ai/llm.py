from openai import OpenAI
from chatRequest import ChatRequest
import os,weather
from dotenv import load_dotenv
allMessage=[]
def createClient():
    load_dotenv()
    api_key=os.getenv("QWEN_KEY")
    client = OpenAI(
                        api_key=api_key,  # 请用阿里云百炼 API Key
                        base_url="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
                    )
    return client
def getWeather(city):
  try:
    load_dotenv()
    api_key=os.getenv("QWEN_KEY")
    client = createClient()

    cityWeather=weather.postWeather(city)
    messages=[{'role':'system','content':"你是一个天气助手，用萌妹的口吻进行简单的讲解"},
                  {'role':'user','content':f"{str(cityWeather)}必须遵照下面例子。"+"{'code':200,'city':'黄石','summary':'今天黄石小雨','message':'success'}json格式回复"}
                 ]
    completion = client.chat.completions.create(
                    model="qwen-plus-2025-07-28",
                    messages=messages
    )
    aiAnswer=completion.choices[0].message.content
    return aiAnswer
  except Exception as e:
    return {"code":500,"message":str(e)}


def get_response(chatRequest:ChatRequest):
    client=createClient()
    content=chatRequest.content
    
    if content=="你是一个耐心的Python老师" or content=="你是一个简洁的天气助手" or content=="你是一个专业的简历优化顾问":
            messages=[{'role':'system','content':content}]
    else:
            messages=[{'role':'user','content':content}]
           
    allMessage.extend(messages)
    completion = client.chat.completions.create(
                                                    model="qwen-plus-2025-07-28",
                                                    messages=messages
                                                )
    aiAnswer=completion.choices[0].message.content
    allMessage.extend({'role': 'assistant', 'content': aiAnswer})
    return aiAnswer
