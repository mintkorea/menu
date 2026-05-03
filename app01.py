import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("🚀 제미나이 최종 테스트")

api_key = st.sidebar.text_input("API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # 404 에러를 피하기 위해 가장 안정적인 모델명 사용
    # 최신 SDK에서는 'gemini-1.5-flash'가 표준입니다.
    model_name = 'gemini-1.5-flash' 
    
    try:
        model = genai.GenerativeModel(model_name)
        
        # 테스트용 간단한 텍스트 생성 시도
        if st.button("모델 연결 확인"):
            response = model.generate_content("Hello, are you working?")
            st.success(f"연결 성공! 응답: {response.text}")
            
    except Exception as e:
        st.error(f"모델 호출 실패: {e}")
        st.info("requirements.txt에서 google-generativeai 버전을 확인해주세요.")
