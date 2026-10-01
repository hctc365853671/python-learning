from openai import OpenAI
import os,Day11_request
from dotenv import load_dotenv


def createClient():
    load_dotenv()
    api_key=os.getenv("QWEN_KEY")
    print(api_key)
    client = OpenAI(
                        api_key=api_key,  # 请用阿里云百炼 API Key
                        base_url="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
                    )
    return client
def get_Ragresponse():
    client=createClient()
    allMessage=[]
    while True:
        strWord=input()
        if strWord=="q":
            print("退出")
            break
        messages=[]
        if strWord=="你是一个耐心的Python老师" or strWord=="你是一个简洁的天气助手" or strWord=="你是一个专业的简历优化顾问":
            messages=[{'role':'system','content':strWord}]
        else:
            messages=[{'role':'user','content':strWord}]
        
        allMessage.append(messages)
        completion = client.chat.completions.create(
            model="qwen-plus-2025-07-28",
            messages=messages
        )
        aiAnswer=completion.choices[0].message.content
        allMessage.append({'role': 'assistant', 'content': aiAnswer})
        print(aiAnswer)

def getWeather():
    client=createClient()
    while True:
        strWord=input("请输入城市:")
        if strWord=="q":
            print("退出")
            break
        cityWeather=Day11_request.postWeather(strWord)
        print(cityWeather)
        messages=[{'role':'system','content':"你是一个天气助手，用萌妹的口吻进行简单的讲解"},
                  {'role':'user','content':f"{str(cityWeather)}请用卖萌的语言用以下例子。"+"{'caity':'黄石','summary':'今天黄石小雨，温度223度，记得带伞哦'}json格式回复"}
                 ]
        completion = client.chat.completions.create(
                    model="qwen-plus-2025-07-28",
                    messages=messages
        )
        aiAnswer=completion.choices[0].message.content
        return aiAnswer
if __name__=="__main__":
    print(getWeather())
    #get_response()
