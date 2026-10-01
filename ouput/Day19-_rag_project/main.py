from contextlib import asynccontextmanager
from fastapi import FastAPI
from chatRequest import ChatRequest
import rag,llm


knowledge_base=None
collection=None
client=None
product_manual = {
    "产品简介": "小行星便携投影仪是一款面向移动观影和临时办公的微型投影设备。它体积接近一本口袋书，重量约480克，支持自动对焦和梯形校正，适合在卧室、露营或小型会议室使用。",
    
    "核心功能": "设备内置1080P物理分辨率，兼容4K输入，亮度为600 ANSI流明，并支持Wi-Fi 6与蓝牙5.2。用户可以通过手机投屏、U盘播放或HDMI连接电脑，系统内置主流视频应用，开机后无需复杂设置即可使用。",
    
    "操作方式": "长按电源键3秒开机，画面会自动完成对焦和梯形校正。通过遥控器或机身触控区可切换信号源、调整音量和选择应用。首次使用时，建议连接家庭Wi-Fi并登录账号，以便同步观看记录和获取系统更新。",
    
    "使用场景": "它适合在暗光环境下投射40至100英寸画面。露营时可搭配移动电源使用，卧室中可投在天花板或白墙，小型会议中可快速展示PPT。若环境光较强，建议拉上窗帘或使用便携幕布以提升画面清晰度。",
    
    "维护与注意": "请勿在潮湿、高温或多尘环境中长时间使用，清洁镜头时先用气吹去除灰尘，再用超细纤维布轻擦。内置电池充满约需2.5小时，续航约2小时，长期不用时建议每三个月充电一次。若出现异常发热或画面闪烁，请停止使用并联系售后。"
}
@asynccontextmanager
async def lifespan(app:FastAPI):
    global knowledge_base,collection,client
    knowledge_base=rag.build_knowledge_base(product_manual)
    client=llm.createClient()
    collection=rag.depositRag(knowledge_base,client)
    
    yield
    print("执行完毕")

app=FastAPI(lifespan=lifespan)
@app.post("/chat")
def ai_chat(chatRequest:ChatRequest):
    return llm.get_response(chatRequest,collection,client)

@app.post("/add_document")
def add_document(chatRequest:ChatRequest):
    knowledge_base1=rag.build_knowledge_base({"data":chatRequest.content})
    rag.collectionAdd(collection,knowledge_base1,client)
    return {"code":200,"message":"存入成功"}