import os

import numpy
from openai import OpenAI
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
import chromadb
from contextlib import asynccontextmanager


knowledge_base=None
collection=None
@asynccontextmanager
def lifespan(app:FastAPI):
    global knowledge_base,collection
    knowledge_base=build_knowledge_base(product_manual)
    collection=depositRag(knowledge_base)
    
    yield
    print("执行完毕")

app=FastAPI(lifespan=lifespan)

def createClient():
    load_dotenv()
    api_key=os.getenv("QWEN_KEY")
    client = OpenAI(
                        api_key=api_key,  # 请用阿里云百炼 API Key
                        base_url="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
                    )
    return client

def get_ali_embedding(text: str):
    resp = createClient().embeddings.create(
        model="qwen3.7-text-embedding",
        input=text
    )
    # 返回向量 list
    return resp.data[0].embedding
# print(len(rag))

def twoStringNp(str1,str2):
    rag=get_ali_embedding(str1)
    rag1=get_ali_embedding(str2)
    a=numpy.array(rag)
    b=numpy.array(rag1)
    return numpy.dot(a,b)/(numpy.linalg.norm(a)*numpy.linalg.norm(b))

# print(twoStringNp("投影仪多重?","产品质量约480克"))#更相似
# print(twoStringNp("投影仪多重？","支持Wi-Fi6"))

class ChatRequest(BaseModel):
     content:str

product_manual = {
    "产品简介": "小行星便携投影仪是一款面向移动观影和临时办公的微型投影设备。它体积接近一本口袋书，重量约480克，支持自动对焦和梯形校正，适合在卧室、露营或小型会议室使用。",
    
    "核心功能": "设备内置1080P物理分辨率，兼容4K输入，亮度为600 ANSI流明，并支持Wi-Fi 6与蓝牙5.2。用户可以通过手机投屏、U盘播放或HDMI连接电脑，系统内置主流视频应用，开机后无需复杂设置即可使用。",
    
    "操作方式": "长按电源键3秒开机，画面会自动完成对焦和梯形校正。通过遥控器或机身触控区可切换信号源、调整音量和选择应用。首次使用时，建议连接家庭Wi-Fi并登录账号，以便同步观看记录和获取系统更新。",
    
    "使用场景": "它适合在暗光环境下投射40至100英寸画面。露营时可搭配移动电源使用，卧室中可投在天花板或白墙，小型会议中可快速展示PPT。若环境光较强，建议拉上窗帘或使用便携幕布以提升画面清晰度。",
    
    "维护与注意": "请勿在潮湿、高温或多尘环境中长时间使用，清洁镜头时先用气吹去除灰尘，再用超细纤维布轻擦。内置电池充满约需2.5小时，续航约2小时，长期不用时建议每三个月充电一次。若出现异常发热或画面闪烁，请停止使用并联系售后。"
}
def build_knowledge_base(manual, chunk_size=100, overlap=20):
    knowledge_base = []
    
    for title, content in manual.items():
        # 把标题和内容拼在一起，检索时更有上下文
        full_text = f"{title}{content}"
        
        start = 0
        while start < len(full_text):
            end = start + chunk_size
            chunk = full_text[start:end]
            knowledge_base.append(chunk)
            start += chunk_size - overlap
            
    return knowledge_base

def depositRag(knowledge_base:list[str]):
    chroma_client=chromadb.PersistentClient("./chroma_db")
    try:
        collection=chroma_client.get_collection(name="product_knowledge")
        # 判断集合里面有没有数据
        count = collection.count()
        if count > 0:
            print("向量库已有数据，跳过入库")
            return collection
    except:
        collection=chroma_client.create_collection(name="product_knowledge",metadata={"hnsw:space":"cosine"})

    oneNum=1
    for i in knowledge_base:
        collection.add(
            embeddings=[get_ali_embedding(i)],
            documents=[i],
            ids=[f"doc__{str(oneNum)}"],
        )
        oneNum+=1
    print(f"入库完成，共{len(knowledge_base)}条")
    return collection
    
    

def getCorrelation(chatRequest:ChatRequest):
    requestRag=get_ali_embedding(chatRequest.content)
    requry=collection.query(
        query_embeddings=[requestRag],
        n_results=3     
    )
    return requry["documents"][0]
    
def get_response(chatRequest:ChatRequest):
    client=createClient()
    answenDocument=getCorrelation(chatRequest)
    print(answenDocument)
    messages=[{'role':'user','content':f"请根据以下参考资料{answenDocument}回答问题。如果资料中没有相关信息，请回答'根据现有资料无法回答'"}]        
    completion = client.chat.completions.create(
                                                    model="qwen-plus-2025-07-28",
                                                    messages=messages
                                                )
    aiAnswer=completion.choices[0].message.content
    return aiAnswer

@app.post("/chat")
def ai_chat(chatRequest:ChatRequest):
    return get_response(chatRequest)