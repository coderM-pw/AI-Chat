import os
from openai import OpenAI
import streamlit as st

# 1.页面基本设置

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    }
)
st.title("ChatGPT")
system_prompt = "你是一个强大的人工助手,回答问题时要详细且有条理,且不失风趣"
# st.logo("resources/logo.png")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    st.error("未检测到 DEEPSEEK_API_KEY，请先配置环境变量。")
    st.stop()

# 2.创建OpenAI客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 3.保存聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4.显示历史聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5.用户输入并显示
user_input = st.chat_input("分享你的想法给我吧")
if user_input:
    # 显示并保存用户消息
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 6.调用AI大模型并显示回复
    with st.chat_message("assistant"):
        try:
            with st.spinner("思考中..."):
                # 构建包含历史上下文的消息列表
                api_messages = [
                    {"role": "system", "content": system_prompt}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=api_messages,
                    stream=False
                )
            answer = response.choices[0].message.content or ""
            st.markdown(answer)
            # 7.保存AI回复
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"调用AI失败: {e}")
