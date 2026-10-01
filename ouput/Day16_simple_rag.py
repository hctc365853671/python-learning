import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from fastapi import FastAPI

allMessage=[]
app=FastAPI()

class ChatRequest(BaseModel):
     content:str

product_manual = {
    "产品简介": "小行星便携投影仪是一款面向移动观影和临时办公的微型投影设备。它体积接近一本口袋书，重量约480克，支持自动对焦和梯形校正，适合在卧室、露营或小型会议室使用。",
    
    "核心功能": "设备内置1080P物理分辨率，兼容4K输入，亮度为600 ANSI流明，并支持Wi-Fi 6与蓝牙5.2。用户可以通过手机投屏、U盘播放或HDMI连接电脑，系统内置主流视频应用，开机后无需复杂设置即可使用。",
    
    "操作方式": "长按电源键3秒开机，画面会自动完成对焦和梯形校正。通过遥控器或机身触控区可切换信号源、调整音量和选择应用。首次使用时，建议连接家庭Wi-Fi并登录账号，以便同步观看记录和获取系统更新。",
    
    "使用场景": "它适合在暗光环境下投射40至100英寸画面。露营时可搭配移动电源使用，卧室中可投在天花板或白墙，小型会议中可快速展示PPT。若环境光较强，建议拉上窗帘或使用便携幕布以提升画面清晰度。",
    
    "维护与注意": "请勿在潮湿、高温或多尘环境中长时间使用，清洁镜头时先用气吹去除灰尘，再用超细纤维布轻擦。内置电池充满约需2.5小时，续航约2小时，长期不用时建议每三个月充电一次。若出现异常发热或画面闪烁，请停止使用并联系售后。"
}

def getCorrelation(chatRequest:ChatRequest):
    answenDocument={}
    for key,value in product_manual.items():
        if chatRequest.content in key or chatRequest.content in value:
            answenDocument.update({key:value})

    return answenDocument

# print(getCorrelation("核心"))
def createClient():
    load_dotenv()
    api_key=os.getenv("QWEN_KEY")
    client = OpenAI(
                        api_key=api_key,  # 请用阿里云百炼 API Key
                        base_url="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
                    )
    return client

def get_response(chatRequest:ChatRequest):
    client=createClient()
    answenDocument=getCorrelation(chatRequest:ChatRequest)
    messages=[{'role':'user','content':f"请根据以下参考资料回答问题。如果资料中没有相关信息，请回答'根据现有资料无法回答'{answenDocument}"}]        
    allMessage.append(messages)
    completion = client.chat.completions.create(
                                                    model="qwen-plus-2025-07-28",
                                                    messages=messages
                                                )
    aiAnswer=completion.choices[0].message.content
    allMessage.append({'role': 'assistant', 'content': aiAnswer})
    return aiAnswer


@app.post("/chat")
def ai_chat(chatRequest:ChatRequest):
    return get_response(chatRequest:ChatRequest)