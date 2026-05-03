import streamlit as st
import google.generativeai as genai
import PIL.Image

# 1. 페이지 설정
st.set_page_config(page_title="Gemini 표 변환기", layout="centered")
st.title("📊 이미지 -> Markdown 표 변환기")

# 2. API 키 설정 (보안을 위해 Secrets 권장, 테스트용으로 직접 입력 가능)
# Streamlit Cloud의 Settings -> Secrets에 GEMINI_API_KEY를 등록했을 경우:
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "AIzaSyCqsMS8czyIpn2pAMiTgScgdBhDHzyN860"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. UI 구성
uploaded_file = st.file_uploader("표가 포함된 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # 이미지 표시
    img = PIL.Image.open(uploaded_file)
    st.image(img, caption="업로드된 이미지", use_container_width=True)
    
    if st.button("표로 변환하기"):
        with st.spinner("제미나이가 표를 읽고 있습니다..."):
            try:
                # 프롬프트 구성
                prompt = "이 이미지의 표 내용을 읽어서 Markdown 형식으로 변환해줘. 데이터 누락 없이 구조를 유지해줘."
                
                # API 호출
                response = model.generate_content([prompt, img])
                
                # 결과 출력 (이 부분이 핵심입니다!)
                st.subheader("✅ 변환 결과")
                st.markdown(response.text)
                
                # 복사하기 편하도록 코드 블록으로도 제공
                with st.expander("Markdown 코드 보기"):
                    st.code(response.text, language="markdown")
                    
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")

else:
    st.info("이미지 파일을 업로드하면 변환이 시작됩니다.")
