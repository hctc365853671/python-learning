import streamlit as st
from Day22_multi_tool_agent import twoTools

# 初始化 放在最顶部
if "rag_bot" not in st.session_state:
    st.session_state.rag_bot = twoTools()
    print("rag_bot 已加载")
rag_bot = st.session_state.rag_bot

if "history_session" not in st.session_state:
    st.session_state.history_session = []
col_chat, col_history = st.columns([3, 2])
# ========== 左侧侧边栏：使用说明 ==========
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
try:
    with col_chat:
        st.title("智能助手")
        clear_button = st.button("清空对话")

        # ========== 表单区域 start ==========
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area("请输入您的问题或需求", height=100)
            send_button = st.form_submit_button("发送")
        # ========== 表单区域 end ==========

        if send_button:
            if not user_input.strip():
                st.warning("请输入内容后再发送")
            else:
                st_waiting=st.text("正在处理您的请求，请稍等...")
                responseJson = rag_bot.get_response(user_input)
                ai_answer = responseJson.get('data')
                st.session_state.history_session.append({"user_input": user_input, "ai_answer": ai_answer})
                st_waiting.empty()
                # AI回答框
                print(responseJson.get('tool_name'))
                if "getWeather" in responseJson.get('tool_name'):
                    st.info(ai_answer, icon="🌤️")
                elif "getCorrelation" in responseJson.get('tool_name'):
                    st.success(ai_answer, icon="📦")
                else:
                    st.warning(ai_answer, icon="⚠️")
        # 清空对话按钮逻辑
        if clear_button:
            rag_bot.messages = [{
                "role": "system",
                "content": "你是一个专业的产品助手。如果用户问天气请调用天气查询工具getWeather，如果客户要查产品知识库请调用getCorrelation工具，请严格根据参考资料回答，不要编造。如果资料不足，请回答：根据现有资料无法回答。"
            }]
            st.session_state.history_session = []
            st.rerun()
            
    with col_history:
        st.sidebar.title("对话历史")
        st.divider()
        if st.session_state.history_session:
            for msg in st.session_state.history_session:
                st.markdown(f"**用户问题:** {msg['user_input']}")
                st.divider()
                st.markdown(f"**AI回答:** {msg['ai_answer']}")
                st.divider()
        else:
            st.info("暂无对话历史")

except Exception as e:
    st.error(f"发生错误: {str(e)}")
    

