import json
import os
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_classic.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
load_dotenv()
BASE_URL="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
API_KEY=os.getenv("QWEN_KEY")
#------------加载llm和embeddings-----------
llm=ChatOpenAI(
    model="qwen3.6-flash",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=0.1,
)
#向量库创建
embeddings=OpenAIEmbeddings(
    model="text-embedding-v4",
    base_url=BASE_URL,
    api_key=API_KEY,
    check_embedding_ctx_length=False,
)
#-------------加载，切分-------------


#------------写入chromadb里----------
persist_directory="./chroma_db"

# 判断向量库目录是否存在
if os.path.exists(persist_directory) and len(os.listdir(persist_directory))>0:
    print("✅ 检测到已有向量库，直接加载，跳过embedding")
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
else:
    loader=PyPDFLoader("./ouput/produce.pdf")
    docs=loader.load()
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n","\n","。","，","！","？"," ",""],
    )
    splits=text_splitter.split_documents(docs)
    print(f"切分后得到{len(splits)}个块")
    print("🆕 向量库不存在，开始向量化并创建")
    vectorstore=Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )

retriever=vectorstore.as_retriever(search_type="mmr",search_kwargs={"k":3,"fetch_k":5})
#------------工具tools------------------------
@tool
def get_weather(city:str)->str:
    """查询当日天气,或者温度，湿度，是否下雨等相关问题时，使用此工具查询"""
    url=f"https://uapis.cn/api/v1/misc/weather?city={city}"
    weather_json=requests.get(url).json()
    return json.dumps(weather_json)
@tool
def search_product_knowledge(query:str)->str:
    """当用户询问产品相关问题时，使用工具查询知识库。"""
    docs=retriever.invoke(query)
    if not docs:
        return "知识库中没有查到相关信息"
    return "\n\n".join( doc.page_content for doc in docs)
tools=[search_product_knowledge,get_weather]
#如果ruturn_messages=false则memory.load_memory_variables为字符串下面agent_prompt就不能现在这个写法

#----------------agent专用的prompt(必须有agent_scratchpad)----------
agent=create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个产品助手。如果遇到天气相关调用工具，如果产品相关问题优先用工具查询知识库，如果其他问题则回答根据相关资料无法回答，不要自己编造",
    
)

def conversation():
    test_questions = [
    "主摄像头是什么？像素和视频规格怎么样？",#命中
    "支持哪些智能运镜模式？",#命中
    "黄石今天天气怎样?",#命中
    "有没有避障？什么水平？",#命中
    "主要适合哪些使用场景？",#命中
    "Mavic 4 Pro 官方售价是多少？",#命中，没有乱编
    "机身是否可折叠？适合怎么携带？",#未命中，中仅提及该机型采用了**“便携机身”**与**“便携设计”**，实际上资料有提到背包携带
    "图传最远距离是多少？用的什么图传系统？",#命中
    
    # ... 其他题目
]
    messages=[]
    for question in test_questions:
        print("输入问题",question)
        user_content=HumanMessage(content=question)
        messages.append(user_content) 
        result=agent.invoke({"messages":messages})
        ai_answen=result["messages"][-1]
        print("AI:",ai_answen.content)
        messages=result["messages"]

if __name__=="__main__":
    conversation()
    
"""
1当前做得好的地方
2主要不足（比如某类问题容易选错工具、回答不够精准等）
3下一步可以优化的方向（1～2 个就够）

1完成了基础的agent开发，用户提问ai会调用tools解决问题
2.回答不够准确，原因主要知识库不够大，一共才切割了5段，k=3也有一定概率不准，如果k=5当然很准确，但是消耗token会怎叫，噪声也会增加
3.提示词还是静态的，没有可以展示的前端
"""
