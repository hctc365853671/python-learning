import streamlit as st
import json
import os
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFium2Loader
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
class Agent:
    def __init__(self):
        load_dotenv()
        BASE_URL="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
        API_KEY=os.getenv("QWEN_KEY")
        self.llm=ChatOpenAI(
            model="qwen3.6-flash",
            base_url=BASE_URL,
            api_key=API_KEY,
            temperature=0.1,
        )
    
    #向量库创建
        self.embeddings=OpenAIEmbeddings(
            model="text-embedding-v4",
            base_url=BASE_URL,
            api_key=API_KEY,
            check_embedding_ctx_length=False,
        )
        self.text_splitter=RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=50,
                separators=["\n\n","\n","。","，","！","？"," ",""],
        )
        #------------写入chromadb里----------
        persist_directory="./chroma_db"
        # 判断向量库目录是否存在
        if os.path.exists(persist_directory) and len(os.listdir(persist_directory))>0:
            print("✅ 检测到已有向量库，直接加载，跳过embedding")
            self.vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
        else:
            loader=PyPDFium2Loader("./produce.pdf")
            docs=loader.load()
            splits=self.text_splitter.split_documents(docs)
            print(f"切分后得到{len(splits)}个块")
            print("🆕 向量库不存在，开始向量化并创建")
            self.vectorstore=Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=persist_directory
            )

        self.retriever=self.vectorstore.as_retriever(search_type="mmr",search_kwargs={"k":3,"fetch_k":10})
        #----------------agent专用的prompt(必须有agent_scratchpad)----------
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
            docs=self.retriever.invoke(query)
            if not docs:
                return "知识库中没有查到相关信息"
            return "\n\n".join( doc.page_content for doc in docs)        
        tools=[search_product_knowledge,get_weather]
        self.agent=create_agent(
            model=self.llm,
            tools=tools,
            system_prompt="你是一个产品助手。如果遇到天气相关调用工具，如果产品相关问题优先用工具查询知识库，如果其他问题则回答根据相关资料无法回答，不要自己编造",
            
        )
        self.messages=[]
    def response(self,question:str):
        print("输入问题",question)
        user_content=HumanMessage(content=question)
        self.messages.append(user_content)
        result=self.agent.invoke({"messages":self.messages})
        ai_answen=result["messages"][-1]
        self.messages=result["messages"]
        return ai_answen.content

    def pdf_to_embedding(self,file_path:str):
        up_pdf=PyPDFium2Loader(file_path)
        docs=up_pdf.load()
        splits=self.text_splitter.split_documents(docs)
        self.vectorstore.add_documents(splits)
        return True
#---------------app----------- 
st.title("产品智能助手")
if "agent" not in  st.session_state:
    st.session_state.agent=Agent()
if "messages" not in st.session_state:
    st.session_state.messages=[]
#侧边栏
with st.sidebar:
    st.title("智能助手使用说明")
    st.markdown("# 📖 使用说明")
    st.divider()
    st.markdown("""
    - 🌤️ **天气查询**
      提问包含城市+天气，会返回天气卡片
      > 示例：鄂州今天天气怎么样？
    - 📦 **产品咨询**
      提问产品相关，返回产品介绍卡片
      > 示例：投影仪参数、投影仪怎么选
    - ✅ 操作
      1. 在输入框输入问题
      2. 点击【发送】获取回答
      3. 点击【清空对话】清空回答内容
    """)
    st.divider()
    st.markdown("💡 提示：一次只提一个问题，识别更准确")
#页面分区
col_chat,col_history= st.columns([6,4])
with col_chat:
    #文件上传
    up_pdf=st.file_uploader("上传PDF拓展知识库",type=["pdf"],max_upload_size=10)
    if up_pdf:
        save_patt=os.path.join("./upload",up_pdf.name)
        with open(save_patt,"wb") as f:
            f.write(up_pdf.read())
        issucc=st.session_state.agent.pdf_to_embedding(save_patt)
        if issucc:
            st.success("添加成功")
        else:
            st.warning("添加失败")
    #中间问答界面
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("请输入您的问题或需求", height=100)
        send_button = st.form_submit_button("发送")
        # ========== 表单区域 end ==========
        if send_button:
            ai_answen_content=st.session_state.agent.response(user_input)
            st.success(ai_answen_content)
            st.session_state.messages.append({user_input:ai_answen_content})
#历史记录展示            
with col_history:
    for mes in  st.session_state.messages:
        for u,a in mes.items():
            st.write(f"用户提问:{u}")
            st.write(f"ai回答:{a}")