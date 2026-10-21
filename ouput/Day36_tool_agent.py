import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_classic.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
BASE_URL="https://open.bigmodel.cn/api/paas/v4"
BASE_URL_EMBEDDING="https://open.bigmodel.cn/api/paas/v4"
API_KEY=os.getenv("QWEN_KEY")
llm=ChatOpenAI(
    model="glm-5.3-flash",
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
vectorstore=Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_day33"
)
retriever=vectorstore.as_retriever(search_kwargs={"k":3})
@tool
def search_product_knowledge(query:str)->str:
    """当用户询问产品相关问题时，使用工具查询知识库。"""
    docs=retriever.invoke(query)
    if not docs:
        return "知识库中没有查到相关信息"
    return "\n\n".join( doc.page_content for doc in docs)
tools=[search_product_knowledge]

#2.agent专用的prompt(必须有agent_scratchpad)
agent_prompt=ChatPromptTemplate.from_messages([
    ("system","你是一个产品助手。遇到产品相关问题优先使用过工具查询知识库，不要自己编造"),
    ("human","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
agent=create_tool_calling_agent(llm,tools,agent_prompt)
agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)
if __name__=="__main__":
    print(agent_executor.invoke({"input":"主摄像头是什么？像素和视频规格怎么样？"}))
    print(agent_executor.invoke({"input":"今天天气怎么样？"}))
    
    
    
"""
对照笔记
点              手写agent_app                               今天langchain               收获
工具定义         自己写函数+描述写死在function中            @tool定义工具+doc注释里       描述直接按变成function里的describetion
工具选则        functions列表传给tools再通过tool_calls      agent自动决定               框架帮我处理循环
多步推理        自己写whil循环                              AgentExecutor处理           中间过程自动管理


"""

