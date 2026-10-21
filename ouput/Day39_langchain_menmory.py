import json
import os
import time
from langchain_core.runnables import RunnablePassthrough
from langchain_classic.memory import ConversationBufferWindowMemory
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
BASE_URL="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
API_KEY=os.getenv("QWEN_KEY")
#------------加载llm和embeddings-----------
llm=ChatOpenAI(
    model="qwen3.6-flash",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=0.1,
)
embeddings=OpenAIEmbeddings(
    model="text-embedding-v4",
    base_url=BASE_URL,
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
#-----------创建memory-----------
memory = ConversationBufferWindowMemory(memory_key="chat_history", k=2,return_messages=True)#如果ruturn_messages=false则memory.load_memory_variables为字符串下面agent_prompt就不能现在这个写法
#----------------agent专用的prompt(必须有agent_scratchpad)----------
agent_prompt=ChatPromptTemplate.from_messages([
    ("system","你是一个产品助手。如果遇到天气相关调用工具，如果产品相关问题优先用过工具查询知识库，如果其他问题则回答根据相关资料无法回答，不要自己编造"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
agent=create_tool_calling_agent(llm,tools,agent_prompt)
agent_executor=AgentExecutor(agent=agent,tools=tools,memory=memory,verbose=True)
if __name__=="__main__":
    agent_executor.invoke({"input":"主摄像头是什么？像素和视频规格怎么样?"})
    time.sleep(2)
    agent_executor.invoke({"input":"告诉我,我上一个问题问的什么？"})
    time.sleep(2)
    agent_executor.invoke({"input":"今天天气怎样"})
    time.sleep(2)
    agent_executor.invoke({"input":"告诉我,我上上一个问题问的什么？"})
"""
1.不同 k 值下的简单对比结论
2.Memory 加上之后，多轮表现如何
3.和手写项目对比：你以前是怎么自己拼历史消息的？框架帮你省了什么？

1.k越大结果越准确，但是上下文占用越大mmn模式适合不涉及到具体数值得抽象问题，默认similarity适合回复具体数值得问题
2.memory加入后，可以记得k论得内容，比我手机while循环代码要简洁
3.用一个列表messages取append。如果要调用工具还得再循环中append{
                                                    "role": "tool",
                                                    "tool_call_id": tool_call.id,
                                                    "content": content
                                                }

"""
