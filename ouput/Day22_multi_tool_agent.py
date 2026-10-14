import json
import os

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
import requests

class twoTools:
    def __init__(self):
        load_dotenv()
        self.product_manual = {
            "产品简介": "小行星便携投影仪是一款面向移动观影和临时办公的微型投影设备。它体积接近一本口袋书，重量约480克，支持自动对焦和梯形校正，适合在卧室、露营或小型会议室使用。",
            
            "核心功能": "设备内置1080P物理分辨率，兼容4K输入，亮度为600 ANSI流明，并支持Wi-Fi 6与蓝牙5.2。用户可以通过手机投屏、U盘播放或HDMI连接电脑，系统内置主流视频应用，开机后无需复杂设置即可使用。",
            
            "操作方式": "长按电源键3秒开机，画面会自动完成对焦和梯形校正。通过遥控器或机身触控区可切换信号源、调整音量和选择应用。首次使用时，建议连接家庭Wi-Fi并登录账号，以便同步观看记录和获取系统更新。",
            
            "使用场景": "它适合在暗光环境下投射40至100英寸画面。露营时可搭配移动电源使用，卧室中可投在天花板或白墙，小型会议中可快速展示PPT。若环境光较强，建议拉上窗帘或使用便携幕布以提升画面清晰度。",
            
            "维护与注意": "请勿在潮湿、高温或多尘环境中长时间使用，清洁镜头时先用气吹去除灰尘，再用超细纤维布轻擦。内置电池充满约需2.5小时，续航约2小时，长期不用时建议每三个月充电一次。若出现异常发热或画面闪烁，请停止使用并联系售后。"
        }
        self.client=self.createClient()
        self.knowledge_base=self.build_knowledge_base(self.product_manual)
        self.collection=self.depositRag(self.knowledge_base)
        self.messages=[{
                            "role": "system",
                            "content": "你是一个专业的产品助手。如果用户问天气请调用天气查询工具getWeather，如果客户要查产品知识库请调用getCorrelation工具，请严格根据参考资料回答，不要编造。如果资料不足，请回答：根据现有资料无法回答。"
                        }]

    def createClient(self):
        
        api_key=os.getenv("QWEN_KEY")
        client = OpenAI(
                            api_key=api_key,  # 请用阿里云百炼 API Key
                            base_url="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
                            
                        )
        return client

    def getWeather(self, city):
        api_code=os.getenv("WEATHER_API_CODE")
        url="https://kztq.market.alicloudapi.com/api/weather/seven/days"
        header={"Authorization":f"APPCODE {api_code}"}
        payload={"city":city}

        try:
            response=requests.post(url=url,data=payload,headers=header)
            return response.json()
        except Exception:
            return {"code":500,"error": "网络似乎有问题"}

    def getCorrelation(self, squestion:str):
        requestRag=self.get_ali_embedding(squestion)
        requry=self.collection.query(
            query_embeddings=[requestRag],
            n_results=3     
        )
        return requry["documents"][0]

    def depositRag(self, knowledge_base:list[str]):
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
                embeddings=[self.get_ali_embedding(i)],
                documents=[i],
                ids=[f"doc__{str(oneNum)}"],
            )
            oneNum+=1
        print(f"入库完成，共{len(knowledge_base)}条")
        return collection

    def get_ali_embedding(self, text: str):
        resp = self.client.embeddings.create(
            model="qwen3.7-text-embedding",
            input=text
        )
        # 返回向量 list
        return resp.data[0].embedding

    def build_knowledge_base(self, manual, chunk_size=100, overlap=20):
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
    def get_response(self, input:str):
            addMessage={
                    "role": "user",
                    "content": f"{input}"
                }
            self.messages.append(addMessage)
            tools=[
                {
                        "type": "function",
                        "function": {
                            "name": "getCorrelation",
                            "description": "在知识库中查询与问题相关的内容",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "question": {
                                        "type": "string",
                                        "description": "用户输入的问题"
                                    }
                                },
                                "required": ["question"]
                            }
                        }
                },
                {
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
            toolName=[]
            while True:
                response=self.client.chat.completions.create(
                    model="qwen-plus-2025-07-28",
                    messages=self.messages,
                    tools=tools,
                    tool_choice="auto"
                )
                msg=response.choices[0].message
                if msg.tool_calls:
                    self.messages.append(msg)
                    for tool_call in msg.tool_calls:
                        args = json.loads(tool_call.function.arguments)
                        tool_name = tool_call.function.name
                        toolName.append(tool_name)
                        if tool_name == "getCorrelation":
                            tool_result = self.getCorrelation(args.get("question"))
                            content = "\n".join(tool_result) 
                        elif tool_name == "getWeather":
                            city = args.get("city")
                            tool_result = self.getWeather(city)
                            content=json.dumps(tool_result, ensure_ascii=False)
                        
                        self.messages.append({
                                                    "role": "tool",
                                                    "tool_call_id": tool_call.id,
                                                    "content": content
                                                })
                            
                else:
                    self.messages.append(msg)
                    return {
                                "code": 200,
                                "message": "success",
                                "data": msg.content,
                                "tool_name": toolName
                            }
               



if __name__ == "__main__":
    two_tools=twoTools()
    try:
        while True:
            user_input=input("请输入问题：")
            if user_input.lower() == "q":
                break
            responseJson=two_tools.get_response(user_input)
            print(f"AI回答:{responseJson.get('data')}")
            
    except Exception as e:
        print(f"发生错误：{e}")