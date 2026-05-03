import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Gemini 표 변환기", layout="centered")
st.title("📊 이미지 -> Markdown 변환기")

# 1. API 키 설정 (사이드바 입력 혹은 Secrets)
API_KEY = st.sidebar.text_input("새로 발급받은 API Key를 입력하세요", type="password")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        # 모델명을 'models/' 포함 혹은 '-latest'로 시도
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        uploaded_file = st.file_uploader("이미지 업로드", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file and st.button("변환 시작"):
            img = Image.open(uploaded_file)
            st.image(img, caption="대상 이미지", use_container_width=True)
            
            with st.spinner("분석 중..."):
                prompt = "이 이미지의 표를 Markdown 테이블로 변환해줘. 다른 설명은 하지마."
                response = model.generate_content([prompt, img])
                
                st.success("변환 완료!")
                st.markdown(response.text)
                st.code(response.text, language="markdown")
                
    except Exception as e:
        st.error(f"에러 발생: {e}")
        st.info("AI Studio에서 'New Project'로 키를 다시 생성했는지 확인해주세요.")
else:
    st.info("사이드바에 API 키를 입력해주세요.")
