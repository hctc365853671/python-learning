import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
BASE_URL="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
API_KEY=os.getenv("QWEN_KEY")
llm=ChatOpenAI(
    model="qwen3.7-plus",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=0.1,
)
embeddings=OpenAIEmbeddings(
    model="qwen3.7-text-embedding",
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
vectorstore=Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_day33"
)
retriever=vectorstore.as_retriever(search_kwargs={"k":3})

#------------Rag链------------
prompt=ChatPromptTemplate.from_template(
    """你是一个严谨的助手。请仅根据下面提供的上下文回答问题。
如果上下文中没有相关信息，请直接说「根据现有资料无法回答」。

上下文：
{context}

问题：{question}

回答："""
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain=(
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
#-------------测试-------------
if __name__=="__main__":
    question="支持哪些智能运镜模式？"
    print("问题:",question)
    print("回答:",rag_chain.invoke(question))
    
"""
                    手写agent_app               langChain写法
PDF加载              pypdf库循环读取              PyPDFLoader是langchain_community这个里的
切分                 长字符串while循环切分        RecursiveCharacterTextSplitter是langchain_text_splitters里的用split_documents方法
embedding            调用api批量                 OpenAIEmbeddings
向量库                chromadb的collection        Chroma.from_documents+.as_retriever(search_kwargs={"k":3})
检索+生成             自己拼接prompt+调模型        LCEL链{|}
"""
