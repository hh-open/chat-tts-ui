import streamlit as st
import requests
from io import BytesIO

st.title('ChatTTS-UI')

# 配置侧边栏
st.sidebar.image('img/logo.png', use_column_width=True)
st.sidebar.subheader("参数配置")
temperature = st.sidebar.slider("temperature", min_value=0.01, max_value=1.0, value=0.5, step=0.01)
top_k = st.sidebar.slider("top_k", min_value=0, max_value=20, value=20, step=1)
top_p = st.sidebar.slider("top_p", min_value=0.0, max_value=1.0, value=0.8, step=0.01)

# 主界面文本输入
input_text = st.text_area('输入文本', placeholder='请输入文本...', height=150)
if st.button('生成'):
    if input_text:
        with st.spinner('正在生成音频文件...'):
            try:
                response = requests.post(
                    "http://127.0.0.1:8806/text-to-speech/",
                    json={"text": input_text, "temperature": temperature, "top_k": top_k, "top_p": top_p},
                    timeout=1000000
                )
                if response.status_code == 200:
                    bytes_data = response.content
                    st.audio(BytesIO(bytes_data), format='audio/wav')
                    st.download_button('下载音频', bytes_data, file_name="output.wav", mime='audio/wav')
                else:
                    st.error(f'生成失败，状态码：{response.status_code}')
            except requests.exceptions.RequestException as e:
                st.error(f"请求失败: {str(e)}")
    else:
        st.warning('请输入文本生成语音。')