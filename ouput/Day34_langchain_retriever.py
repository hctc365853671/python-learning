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
# retriever=vectorstore.as_retriever(search_kwargs={"k":5})#字典中k的值是切割段数
# retriever=vectorstore.as_retriever(search_type="mmr",search_kwargs={"k":3,"fetch_k":10,"lambda_mult":0.6})#先取10个，再取3个多样性高的
retriever=vectorstore.as_retriever(search_type="similarity_score_threshold",search_kwargs={"k":3,"score_threshold":0.3})

#------------Rag链------------
prompt=ChatPromptTemplate.from_messages(
    [("system","你是一个严谨的助手。请仅根据下面提供的上下文回答问题。如果上下文中没有相关信息，请直接说「根据现有资料无法回答」"),
     ("human","上下文:\n{context}\n\n问题:{question}")
     ])

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
    question="主摄像头是什么？像素和视频规格怎样？"
    print("问题:",question)
    print("回答:",rag_chain.invoke(question))
    
"""
简单笔记:
retriever这几种写法
1.不写search_type的话，默认值是similarity,返回最相关的k段文档
2.search_type=mmr时，retriever使用mmr算法，该算法除了找到问题相关的片段外，还会找与相关片段差异大的片段
对比默认算法，mmr可以起到降噪的作用，节省上下文，若知识库中出现大量重复描述某个东西的片段适合用mmr，
若对检索结果要求必须精确例如产品价格=100元，这种默认更合适，若是回答某个问题，不要求具体量化，则用mmr更合适
3.第三种写法实际上就是第一种加入阈值，retriever只会再大于这个阈值的范围内找，如果大于这个阈值不足k段，则返回实际段数。甚至可嫩没有
对照笔记
                        手写agent_app           今天langchain                                         收获
检索参数控制            源码写死k自己过滤         as_retriever(search_kwargs={"k":5})                参数统一易切换
mmr                     完全没做               search_type="mmr"                                    改变search_type就行
消息格式           一般是列表嵌套字典，然后拼接     ChatPromptTemplate.from_messages                   更清晰，可扩展性强


"""
