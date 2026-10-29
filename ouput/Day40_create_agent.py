import json
import os
from langchain.agents import create_agent
from langchain_classic.memory import ConversationBufferWindowMemory
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

retriever=vectorstore.as_retriever(search_kwargs={"k":3})
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
#-----------创建memory-----------
memory = ConversationBufferWindowMemory(memory_key="chat_history", k=2,return_messages=True)#如果ruturn_messages=false则memory.load_memory_variables为字符串下面agent_prompt就不能现在这个写法
#----------------agent专用的prompt(必须有agent_scratchpad)----------
agent=create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个产品助手。如果遇到天气相关调用工具，如果产品相关问题优先用工具查询知识库，如果其他问题则回答根据相关资料无法回答，不要自己编造",
    
)
def conversation():
    messages=[]
    while True:
        question=input("请输入问题")
        if not question:
            continue
        user_content={"role":"user","content":f"{question}"}
        messages.append(user_content)
        result=agent.invoke({"messages":messages})
        ai_answen=result["messages"][-1]
        print("AI:",ai_answen.content)
        messages.append(ai_answen)

if __name__=="__main__":
    conversation()

"""
对比点          经典写法（create_tool_calling_agent）       新版（create_agent）
导入                langchain_classic                           langchain.agents
Prompt          需要 agent_scratchpad + chat_history        主要用 system_prompt
调用输入            {"input": "..."}                            {"messages": [...]}
Memory          通过 AgentExecutor + Memory 对象    通常用 checkpointer 或手动传 messages
代码量              相对多                                      更简洁
经典写法看的非常明了先干什么后干什么，新写法跟我手写有agent点相似
"""
