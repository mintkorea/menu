import pandas as pd
import streamlit as st
import re

# --- 1. 데이터 로드 및 파일 매핑 ---
@st.cache_data
def get_file_info():
    # 실제 서버에 존재하는 파일명과 화면에 표시할 이름 매핑
    return {
        '의산연01.csv': '🔬 의산연 본관',
        '대학본관.csv': '🏢 대학 본관',
        '의산연별관.csv': '🧪 의산연 별관',
        '성의회관.csv': '⛪ 성의회관',
        '병원별관.csv': '🏥 병원 별관',
        '옴니버스A.csv': '🍏 옴니버스파크(A)',
        '옴니버스B.csv': '🍎 옴니버스파크(B)',
        '서울성모병원.CSV': '🚑 서울성모병원'
    }

# --- 2. 유틸리티: 층 표시 정규화 ---
def format_floor(floor_val):
    if pd.isna(floor_val): return "-"
    # 숫자, B, L만 추출 (FF 중복 방지)
    clean_floor = re.sub(r'[^0-9BL]', '', str(floor_val).upper())
    return f"{clean_floor}F" if clean_floor else str(floor_val)

# --- 3. 메인 UI ---
def main():
    st.set_page_config(page_title="데이터 관리 도구", layout="centered")
    
    st.markdown("""
        <style>
        .m-title { font-size: 1.2rem; font-weight: bold; color: #1E3A8A; margin-bottom: 20px; }
        .edit-card { 
            background-color: #ffffff; padding: 20px; border-radius: 12px; 
            border: 1px solid #e1e4e8; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 25px;
        }
        .stButton>button { width: 100%; border-radius: 8px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='m-title'>⚙️ 성의교정 원본 데이터 관리자</div>", unsafe_allow_html=True)

    file_map = get_file_info()

    # --- [핵심] 원본 파일 선택 섹션 ---
    st.markdown("### 📥 수정할 파일을 선택하세요")
    
    # 2열로 배치하여 선택하기 편하게 구성
    col1, col2 = st.columns(2)
    files = list(file_map.keys())
    
    # 세션 상태를 이용해 어떤 파일이 선택되었는지 추적
    selected_file = st.radio(
        "파일 목록", 
        options=files, 
        format_func=lambda x: file_map[x],
        label_visibility="collapsed"
    )

    if selected_file:
        st.markdown(f"---")
        with st.container():
            try:
                # 선택된 파일만 읽어오기
                try: df = pd.read_csv(selected_file, encoding='utf-8-sig')
                except: df = pd.read_csv(selected_file, encoding='cp949')
                
                st.success(f"✅ **{file_map[selected_file]}** ({selected_file}) 파일이 선택되었습니다.")
                
                # 다운로드 버튼 생성
                csv_bytes = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                st.download_button(
                    label=f"💾 {selected_file} 다운로드 (엑셀 수정용)",
                    data=csv_bytes,
                    file_name=selected_file,
                    mime='text/csv',
                    type="primary"
                )
                
                # 데이터 미리보기 (상단 5개만)
                with st.expander("👀 데이터 미리보기 (수정 전 내용 확인)"):
                    st.dataframe(df.head(10), use_container_width=True)
                    
            except Exception as e:
                st.error(f"⚠️ {selected_file} 파일을 찾을 수 없습니다. 파일명을 확인해 주세요.")

    st.markdown("---")
    st.info("""
    **💡 데이터 수정 팁:**
    1. 위 버튼으로 파일을 다운로드하여 **엑셀**에서 엽니다.
    2. 'FF' 중복 데이터나 오타를 수정합니다.
    3. 저장할 때 반드시 **CSV(쉼표로 분리)** 형식을 유지해 주세요.
    4. 수정된 파일을 서버의 동일한 위치에 덮어쓰기 하면 앱에 즉시 반영됩니다.
    """)

if __name__ == "__main__":
    main()
