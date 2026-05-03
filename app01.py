import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="Gemini 이미지 표 변환기", layout="centered")
st.title("📊 표 이미지 -> Markdown 변환기")
st.markdown("이미지를 업로드하면 제미나이가 자동으로 Markdown 표 형식을 만들어줍니다.")

---

# 2. API 키 및 모델 설정
# 보안을 위해 Streamlit Secrets 사용을 권장합니다.
# 직접 입력 테스트 시에는 'YOUR_API_KEY' 부분을 실제 키로 바꾼 후 시도하세요.
try:
    API_KEY = st.secrets["AIzaSyCXNQ3b9qcaJjQAGua3-vcgRZ2j0wASaXM"]
except Exception:
    # Secrets에 등록하지 않았을 경우를 위한 입력창
    API_KEY = st.sidebar.text_input("Gemini API Key를 입력하세요", type="password")

if not API_KEY:
    st.warning("API 키가 필요합니다. 사이드바에 입력하거나 Secrets를 설정해주세요.")
    st.stop()

# 모델 초기화 (404 에러 방지를 위해 최신 식별자 사용)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

---

# 3. 사용자 파일 업로드 UI
uploaded_file = st.file_uploader("표가 포함된 이미지를 선택하세요 (PNG, JPG, JPEG)", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # 이미지 열기 및 화면 표시
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드 완료", use_container_width=True)

    # 변환 버튼
    if st.button("표 데이터 추출하기"):
        with st.spinner("제미나이가 데이터를 분석 중입니다..."):
            try:
                # 프롬프트 설정: 명확한 결과물을 위해 페르소나와 형식을 지정합니다.
                prompt = """
                이 이미지에 있는 모든 표 데이터를 읽어서 Markdown 테이블 형식으로 변환해줘.
                1. 텍스트를 누락하지 말 것.
                2. 표의 구조(행과 열)를 최대한 유지할 것.
                3. 마크다운 형식 외에 다른 설명은 생략해줘.
                """
                
                # API 호출
                response = model.generate_content([prompt, image])
                
                # 결과 출력
                if response.text:
                    st.success("변환 성공!")
                    st.subheader("✅ 결과 미리보기")
                    st.markdown(response.text)
                    
                    st.divider()
                    
                    # 텍스트 복사용 코드 블록
                    st.subheader("📝 마크다운 코드")
                    st.code(response.text, language="markdown")
                else:
                    st.error("결과를 생성하지 못했습니다. 이미지를 다시 확인해주세요.")
                    
            except Exception as e:
                # 403, 404 에러 등을 사용자에게 친절하게 표시
                st.error(f"에러가 발생했습니다: {e}")
                st.info("API 키 권한(403)이나 모델 지원 여부(404)를 확인해보세요.")

else:
    st.info("왼쪽 버튼을 눌러 이미지 파일을 업로드해주세요.")
