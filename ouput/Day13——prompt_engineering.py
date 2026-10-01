from openai import OpenAI
import os,Day11_request,Day12_llm_chat
def getWeather():
    client=Day12_llm_chat.createClient()
    allMessage=[]
    formatAi={"城市": "","天气": "","温度": "","建议": ""}
    while True:
      try:
        strWord=input("请输入城市:")
        if strWord=="q":
            print("退出")
            break
        cityWeather=Day11_request.postWeather(strWord)
        
        messages=[{'role':'system','content':"你是一个天气助手，用萌妹的口吻进行简单的讲解"},
                  {'role':'user','content':f"{str(cityWeather)}请用卖萌的语言，总结该城市今天的天气情况，包含温度、天气状况和建议，控制在100字以内。请严格按照以下JSON格式返回：{formatAi}"}
                 ]
        allMessage.extend(messages)
        completion = client.chat.completions.create(
                    model="qwen-plus-2025-07-28",
                    messages=allMessage
        )
        aiAnswer=completion.choices[0].message.content
        allMessage.extend([{'role': 'assistant', 'content': aiAnswer}])
        print(aiAnswer)
      except Exception as e:
          print(e)
          
def get_response():   
    client = Day12_llm_chat.createClient()
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
        
        allMessage.extend(messages)
        completion = client.chat.completions.create(
            model="qwen-plus-2025-07-28",
            messages=messages
        )
        aiAnswer=completion.choices[0].message.content
        allMessage.extend([{'role': 'assistant', 'content': aiAnswer}])
        print(aiAnswer)
        
def aiAssistant():
    client = Day12_llm_chat.createClient()
    allMessage=[]
    formatAi={"城市": "","天气": "","温度": "","建议": ""}
    while True:
        strWord=input("请输入内容")
        if strWord=="q":
            print("退出")
            break
        messages=[]
        if strWord=="萌妹天气助手":
            allMessage=[]
            while True:               
                cityWeather=Day11_request.postWeather(strWord)
                messages=[{'role':'system','content':"你是一个天气助手，用萌妹的口吻进行简单的讲解"},
                              {'role':'user','content':f"{str(cityWeather)}请用卖萌的语言，总结该城市今天的天气情况，包含温度、天气状况和建议，控制在100字以内。请严格按照以下JSON格式返回：{formatAi}"}
                         ]
                allMessage.extend(messages)
                completion = client.chat.completions.create(
                                    model="qwen-plus-2025-07-28",
                                    messages=allMessage
                )
                aiAnswer=completion.choices[0].message.content
                allMessage.extend([{'role': 'assistant', 'content': aiAnswer}])
                print(aiAnswer)
                strWord=input("请输入内容")
                print(strWord)
                if strWord=="Python老师" or strWord=="翻译助手" or strWord=="简历优化顾问":
                    print("12312321")
                    break
        if strWord=="Python老师" or strWord=="翻译助手" or strWord=="简历优化顾问":
            print("12312321")
            allMessage=[]
            messages=[{'role':'system','content':strWord}]
        else:
            messages=[{'role':'user','content':strWord}]
        allMessage.extend(messages)
        completion = client.chat.completions.create(
                    model="qwen-plus-2025-07-28",
                    messages=allMessage
        )
        aiAnswer=completion.choices[0].message.content
        allMessage.extend([{'role': 'assistant', 'content': aiAnswer}])
        print(aiAnswer)
if __name__=="__main__":
    #getWeather()
    #get_response()
    aiAssistant()