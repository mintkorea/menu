import streamlit as st

# 모바일 전체 화면 사용 및 폰트 최적화
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .main { font-size: 0.8rem; } /* 모바일에서 더 많은 정보를 보기 위해 폰트 축소 */
    .stButton>button { width: 100%; }
    .contact-card { border: 1px solid #ddd; padding: 5px; border-radius: 5px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📞 통합 비상연락망")

tab1, tab2 = st.tabs(["🧹 미화팀 (층별)", "🛡️ 보안팀 (시설별)"])

# --- 미화팀 탭 ---
with tab1:
    st.subheader("건물별 층수 기준")
    # 예시: 의산연/성의회관 선택 필터
    building = st.segmented_control("건물 선택", ["성의회관", "의산연", "별관"])
    
    # 층별 데이터 출력 (사진 포맷 유지)
    # 실제 데이터프레임(df)에서 필터링하여 출력하는 로직 적용
    st.write(f"**{building} 명단**")
    cols = st.columns([1, 2, 1])
    cols[0].write("**위치**")
    cols[1].write("**성명/연락처**")
    cols[2].write("**비고**")
    st.divider()
    # 반복문을 통해 데이터 출력...

# --- 보안팀 탭 ---
with tab2:
    st.subheader("조별/시설별 배치")
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.info("🏫 옴니버스")
        # 옴니버스 보안 요원 명단 (A/B/C조 순서대로)
        st.caption("A조: 홍길동 (조장)")
        st.caption("B조: 김철수")
        
    with right_col:
        st.success("🏥 성의회관/의산연")
        # 성의회관 보안 요원 명단
        st.caption("A조: 이영희 (조장)")
        st.caption("C조: 박명수")

# --- 공통 기능: 신규 추가 ---
with st.sidebar:
    st.header("⚙️ 관리 메뉴")
    if st.button("➕ 신규 직원 등록"):
        # 입력 폼 팝업 또는 페이지 이동
        pass
    if st.button("🖨️ 현재 양식 출력 (PDF)"):
        st.write("사진 속 서식으로 PDF를 생성합니다.")
