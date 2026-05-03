import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime
import os

# 1. 저장용 폴더 생성
for folder in ["db_images", "db_texts"]:
    os.makedirs(folder, exist_ok=True)

# 2. 페이지 설정 및 제목
st.set_page_config(page_title="AI 식단 관리 시스템", layout="wide")
st.title("🚀 AI 식단표 분석 및 아카이브 게시판")

# 3. 사이드바 API 설정 (보안 및 유연성)
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.info("키를 입력하면 시스템이 활성화됩니다.")

# 4. 메인 로직
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # [핵심] 현재 API 키가 지원하는 모델 목록 자동 확인 (404 에러 방지)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            st.error("❌ 이 API 키로 사용할 수 있는 모델이 없습니다.")
        else:
            # 1.5-flash 우선 선택, 없으면 첫 번째 가용 모델 선택
            target_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
            model = genai.GenerativeModel(target_model)
            st.success(f"✅ 연결된 모델: {target_model}")

            # 파일 업로드 섹션
            uploaded_file = st.file_uploader("식단표 이미지를 선택하세요", type=['png', 'jpg', 'jpeg'])

            if uploaded_file:
                img = Image.open(uploaded_file)
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📸 업로드 이미지")
                    st.image(img, use_container_width=True)

                if st.button("📊 분석 및 게시판 저장", use_container_width=True):
                    with st.spinner("AI가 데이터를 추출 중입니다..."):
                        try:
                            # 분석 요청
                            response = model.generate_content(["이미지의 식단표를 마크다운 표 형식으로 상세히 정리해줘. 다른 설명은 생략해.", img])
                            result_text = response.text

                            # 파일 저장 (고유 ID 생성)
                            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            img.save(f"db_images/{now}.png")
                            with open(f"db_texts/{now}.txt", "w", encoding="utf-8") as f:
                                f.write(result_text)

                            with col2:
                                st.subheader("📝 분석 결과")
                                st.markdown(result_text)
                                st.balloons()
                        except Exception as e:
                            st.error(f"분석 중 오류 발생: {e}")

    except Exception as e:
        st.error(f"시스템 오류: {e}")
else:
    st.warning("👈 사이드바에 API 키를 입력해 주세요.")

# 5. 게시판 섹션 (저장된 기록 불러오기)
st.divider()
st.subheader("📂 저장된 식단표 기록")

if os.path.exists("db_texts"):
    records = sorted([f for f in os.listdir("db_texts") if f.endswith(".txt")], reverse=True)
    
    if not records:
        st.write("아직 저장된 기록이 없습니다.")
    else:
        for record in records:
            file_id = record.replace(".txt", "")
            # 날짜 가독성 처리
            display_date = f"{file_id[:4]}-{file_id[4:6]}-{file_id[6:8]} {file_id[9:11]}:{file_id[11:13]}"
            
            with st.expander(f"📅 기록 확인: {display_date}"):
                exp_col1, exp_col2 = st.columns([1, 2])
                
                img_path = f"db_images/{file_id}.png"
                if os.path.exists(img_path):
                    with exp_col1:
                        st.image(img_path, use_container_width=True)
                
                with exp_col2:
                    with open(f"db_texts/{record}", "r", encoding="utf-8") as f:
                        st.markdown(f.read())
