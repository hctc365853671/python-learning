import json
import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_classic.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests

load_dotenv()
BASE_URL="https://open.bigmodel.cn/api/paas/v4"
BASE_URL_EMBEDDING="https://open.bigmodel.cn/api/paas/v4"
API_KEY=os.getenv("QWEN_KEY")
#------------加载llm和embeddings-----------
llm=ChatOpenAI(
    model="glm-4.7-flash",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=0.1,
)
embeddings=OpenAIEmbeddings(
    model="embedding-2",
    base_url=BASE_URL_EMBEDDING,
    api_key=API_KEY,
    check_embedding_ctx_length=False,
)
#-------------加载，切分-------------
loader=PyPDFLoader("./ouput/produce.pdf")
docs=loader.load()
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80,
    separators=["\n\n","\n","。","，","！","？"," ",""],
)
splits=text_splitter.split_documents(docs)
print(f"切分后得到{len(splits)}个块")

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
    """查询当日天气相关问题时，使用此工具查询"""
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

#----------------agent专用的prompt(必须有agent_scratchpad)----------
agent_prompt=ChatPromptTemplate.from_messages([
    ("system","你是一个产品助手。如果遇到天气相关调用工具，如果产品相关问题优先用过工具查询知识库，如果其他问题则回答根据相关资料无法回答，不要自己编造"),
    ("human","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
agent=create_tool_calling_agent(llm,tools,agent_prompt)
agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)

#-----------------启动----------------
if __name__=="__main__":
    print(agent_executor.invoke({"input":"主摄像头是什么？像素和视频规格怎么样?"}))
    # print(agent_executor.invoke({"input":"黄石今天天气如何?"}))
    # print(agent_executor.invoke({"input":"黄石明天会下雨吗?"}))
    # print(agent_executor.invoke({"input":"dota痛苦女王英雄介绍?"}))
    
    
"""
问题
1.手写function Calling和langChain agent最大区别

2.工具表示(docstring)对最终效果影响有多大？

3.什么场景你更愿意继续手写？什么场景使用框架

4.如果要把这个Agent摸到原来的streamlit agent_app，你会怎么改
回答
1.手写的每个tool得写一长串由字符串组成得列表字典，显得十分臃肿langchain
用装饰器装饰得函数，通过docstring，args来schema
2.感觉不大，我查天气，docstring只写了123依然查出来了
3.学习底层知识得时候手写，做项目得时候用框架
4.另外写一个app.py作为stereamlit得ui，再app.py里将mian实例化该实例主要提供调用大模型得返回值
"""

    