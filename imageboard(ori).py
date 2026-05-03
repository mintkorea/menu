import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("🚀 제미나이 통합 테스트")

# 사이드바에서 키 입력
api_key = st.sidebar.text_input("새로 발급받은 API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # [중요] 내 키가 사용할 수 있는 모델 리스트를 가져옵니다.
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not models:
            st.error("이 API 키로 사용할 수 있는 모델이 없습니다.")
        else:
            # 1.5-flash가 있으면 우선 선택, 없으면 목록의 첫 번째 선택
            target_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models else models[0]
            st.info(f"현재 연결된 모델: {target_model}")
            
            model = genai.GenerativeModel(target_model)
            
            uploaded_file = st.file_uploader("표 이미지 업로드", type=['png', 'jpg', 'jpeg'])
            
            if uploaded_file and st.button("변환 시작"):
                img = Image.open(uploaded_file)
                st.image(img, use_container_width=True)
                
                with st.spinner("분석 중..."):
                    response = model.generate_content(["이미지의 표를 마크다운으로 변환해줘", img])
                    st.markdown(response.text)
                    
    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.info("사이드바에 API 키를 입력하면 시작합니다.")
