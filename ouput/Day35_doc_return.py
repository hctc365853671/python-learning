import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough,RunnableParallel
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
retriever=vectorstore.as_retriever(search_kwargs={"k":3})#字典中k的值是切割段数
# retriever=vectorstore.as_retriever(search_type="mmr",search_kwargs={"k":3,"fetch_k":10,"lambda_mult":0.6})#先取10个，再取3个多样性高的
# retriever=vectorstore.as_retriever(search_type="similarity_score_threshold",search_kwargs={"k":3,"score_threshold":0.3})

#------------Rag链------------
prompt=ChatPromptTemplate.from_messages(
    [("system","你是一个严谨的助手。请仅根据下面提供的上下文回答问题。如果上下文中没有相关信息，请直接说「根据现有资料无法回答」"),
     ("human","上下文:\n{context}\n\n问题:{question}")
     ])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# rag_chain=(
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )
rag_chain_with_source=(
    RunnableParallel(
        {
            "context":retriever | format_docs,
            "question": RunnablePassthrough(),
            "docs":retriever,#保留原始Document列表
        }
    )
        | RunnablePassthrough.assign(
            answer=prompt | llm | StrOutputParser()
        )
    )

chat_history = []   # 存放 (question, answer) 元组

def ask(question: str):
    # 把历史简单拼进当前问题（最朴素的方式）
    history_text = ""
    for q, a in chat_history[-3:]:   # 只保留最近 3 轮，防止太长
        history_text += f"用户：{q}\n助手：{a}\n\n"
    
    full_question = history_text + f"用户：{question}" if history_text else question
    
    result = rag_chain_with_source.invoke(full_question)  # 或直接用原链
    answer = result["answer"] if isinstance(result, dict) else result
    
    chat_history.append((question, answer))
    return answer

allMessages=[]
def mutil_turn_conversation():
    while True:
        question=input("请输入问题:")
        prompt_temp=ChatPromptTemplate.from_messages(
        [("system","你是一个严谨的助手。请仅根据下面提供的上下文回答问题。如果上下文中没有相关信息，请直接说「根据现有资料无法回答」"),
        ("human","上下文:\n{context}\n\n问题:{question}")
        ])
        new_rag_chain=(
            RunnableParallel(
        {
            "context":retriever | format_docs,
            "question": RunnablePassthrough(),
            "docs":retriever,#保留原始Document列表
        }
        )
        | RunnablePassthrough.assign(
            answer=prompt_temp | llm | StrOutputParser()
        )
        )
        result=new_rag_chain.invoke(question)
        prompt_temp_str=prompt_temp.format(context=result["context"],question=result["question"])
        allMessages.append(prompt_temp_str)
        ai_answer="AI:"+result["answer"]
        allMessages.append(ai_answer)
        next_context="\n".join(allMessages)
        # print(next_context)
        prompt_temp=ChatPromptTemplate.from_messages(
        [
            ("human",f"上下文:{next_context}"+"\n{context}\n\n问题:{question}")
        ])
        print(ai_answer)
        
    

#-------------测试-------------
if __name__=="__main__":
    # question="主摄像头是什么？像素和视频规格怎样？"
    # result=rag_chain_with_source.invoke(question)
    # print("问题:",question)
    # print("回答:",result["answer"])
    # print("\n-----------检索到的文档------------")
    # for i,doc in enumerate(result["docs"],1):
    #     print(f"[{i}]{doc.page_content[:150]}")
    # print(ask("主摄像头是什么？像素和视频规格怎样？"))
    # print(ask("那它支持哪些智能运镜模式？"))   # 看是否能利用上一轮信息,结论用不了
    mutil_turn_conversation()
    
    
    
"""
四、对照笔记建议
点                  手写 agent_app                  今天 LangChain                  收获
返回答案+文档           自己返回 dict              RunnableParallel + assign        结构清晰，易扩展
多轮历史            自己维护列表 / 会话             先手写拼接                         理解 Memory 要解决什么问题

RunnableParallel()并行处理给字典的每个key赋值 输出dict
RunnablePassthrough()原样穿透不处理  和输入一模一样
RunnablePassthrough.assin()保留原有字段，追加新字段，在原字典基础上扩容的 dict
"""
