import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime
import os
import re

# 1. 저장용 폴더 생성 (이미지 및 텍스트 데이터 보관)
for folder in ["db_images", "db_texts"]:
    os.makedirs(folder, exist_ok=True)

# 2. 페이지 설정 및 디자인
st.set_page_config(page_title="AI 식단 관리 시스템", layout="wide")
st.title("🍱 AI 식단표 분석 및 디지털 아카이브")
st.markdown("---")

# 3. 사이드바 설정 (API 키 입력 및 모델 상태 확인)
with st.sidebar:
    st.header("⚙️ 시스템 설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.info("API 키를 입력하면 AI 분석 기능이 활성화됩니다.")

# 4. 메인 분석 로직
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 가용 모델 리스트 확인 (환경별 404 에러 방지)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            st.error("❌ 해당 API 키로 지원되는 모델을 찾을 수 없습니다.")
        else:
            # 1.5-flash 모델을 우선적으로 연결
            target_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
            model = genai.GenerativeModel(target_model)
            st.success(f"✅ 연결됨: {target_model}")

            # 파일 업로드 섹션
            uploaded_file = st.file_uploader("식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

            if uploaded_file:
                img = Image.open(uploaded_file)
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.subheader("📸 원본 이미지")
                    st.image(img, use_container_width=True)

                if st.button("📊 AI 분석 및 기록 저장", use_container_width=True):
                    with st.spinner("AI가 표 구조를 정밀 분석 중입니다..."):
                        try:
                            # [핵심] OCR 정확도 향상을 위한 정밀 프롬프트
                            prompt = """
                            이 식단표 이미지의 데이터를 추출하여 마크다운 표(Markdown Table)로 변환해줘.
                            
                            지시사항:
                            1. <br>, <br/> 등 모든 HTML 태그를 제거하고 순수 텍스트만 추출해.
                            2. '간편식'과 '중식' 메뉴가 서로 겹치거나 중복되지 않도록 이미지의 가로 구분선을 엄격히 지켜서 분류해.
                            3. 줄바꿈이 필요한 경우 마크다운 표 안에서 공백 두 번으로 처리해.
                            4. 날짜별, 구분별(조식, 간편식, 중식 등)로 칸을 정확히 맞춰줘.
                            5. 다른 설명 없이 표 데이터만 출력해.
                            """
                            
                            response = model.generate_content([prompt, img])
                            raw_text = response.text

                            # [추가 정제] 남아있을 수 있는 HTML 태그 강제 제거
                            clean_text = re.sub(r'<[^>]*>', ' ', raw_text)

                            # 데이터 저장 (ID: 일시)
                            file_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            img.save(f"db_images/{file_id}.png")
                            with open(f"db_texts/{file_id}.txt", "w", encoding="utf-8") as f:
                                f.write(clean_text)

                            with col2:
                                st.subheader("📝 AI 분석 결과")
                                st.markdown(clean_text)
                                st.balloons()
                        except Exception as e:
                            st.error(f"분석 실패: {e}")

    except Exception as e:
        st.error(f"시스템 오류: {e}")
else:
    st.warning("👈 사이드바에 API 키를 입력하여 시작하세요.")

# 5. 아카이브 게시판 (저장된 데이터 표시)
st.markdown("---")
st.subheader("📂 식단 기록 저장소")

if os.path.exists("db_texts"):
    records = sorted([f for f in os.listdir("db_texts") if f.endswith(".txt")], reverse=True)
    
    if not records:
        st.info("아직 저장된 식단 기록이 없습니다.")
    else:
        for record in records:
            timestamp = record.replace(".txt", "")
            # 타임스탬프를 읽기 좋은 형식으로 변환
            display_time = f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}"
            
            with st.expander(f"📅 기록 일시: {display_time}"):
                row_col1, row_col2 = st.columns([1, 2])
                
                img_path = f"db_images/{timestamp}.png"
                if os.path.exists(img_path):
                    with row_col1:
                        st.image(img_path, caption="원본 이미지", use_container_width=True)
                
                with row_col2:
                    with open(f"db_texts/{record}", "r", encoding="utf-8") as f:
                        st.markdown(f.read())
