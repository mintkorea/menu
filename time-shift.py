import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 데이터 및 설정 ---
START_DATE = datetime(2026, 3, 24).date()
# 이미지 규칙에 따른 6일 주기 로테이션 설정 (2회 연속 근무 반영)
# 순서: 회관(후) -> 회관(전) -> 의산A(후) -> 의산A(전) -> 의산B(후) -> 의산B(전)
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

st.set_page_config(page_title="성의교정 C조", layout="centered")

# --- 2. CSS 스타일 (중앙 정렬 및 폰트 확대) ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    .period-text { font-size: 18px; color: #555; text-align: center; margin-bottom: 20px; }
    [data-testid="stDataFrame"] { justify-content: center; display: flex; }
    .stDataFrame div[data-testid="stTable"] div { text-align: center !important; }
    [data-testid="stSidebar"] { font-size: 18px !important; }
    [data-testid="stSidebar"] .stRadio > label, [data-testid="stSidebar"] .stSelectbox label { 
        font-size: 18px !important; font-weight: bold !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴", ["📅 교대 근무표", "📍 근무 상황판"])
    user_name = st.selectbox("👤 이름 강조 (셀 색상)", ["안 함", "황재업"] + WORKERS)
    if menu == "📅 교대 근무표":
        duration = st.number_input("📅 조회 기간(개월)", min_value=1, max_value=6, value=1)

# --- 4. 근무표 로직 (새로운 규칙 적용) ---
now = datetime.now()

if menu == "📅 교대 근무표":
    start_v = now.date()
    end_v = start_v + timedelta(days=30 * duration)
    st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='period-text'>({start_v.strftime('%m월 %d일')} ~ {end_v.strftime('%m월 %d일')})</div>", unsafe_allow_html=True)

    cal_list = []
    curr = start_v
    while curr <= end_v:
        # 3일 간격 근무는 유지하되, 내부 로테이션은 2회 연속 규칙 적용
        diff_days = (curr - START_DATE).days
        if diff_days % 3 == 0:
            cycle_idx = (diff_days // 3) % 6  # 6번(2회씩 3개조)의 순환 주기
            
            # 규칙: ABC 근무를 각 2회씩 연속 수행
            # 0,1: 회관 / 2,3: 의산A / 4,5: 의산B (예시 순서)
            if cycle_idx < 2:
                positions = {"회관": WORKERS[0], "의산A": WORKERS[1], "의산B": WORKERS[2]}
            elif cycle_idx < 4:
                positions = {"회관": WORKERS[1], "의산A": WORKERS[2], "의산B": WORKERS[0]}
            else:
                positions = {"회관": WORKERS[2], "의산A": WORKERS[0], "의산B": WORKERS[1]}
                
            wd = curr.weekday()
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": "황재업",
                "회관": positions["회관"],
                "의산A": positions["의산A"],
                "의산B": positions["의산B"]
            })
        curr += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)

    # 셀 단위 스타일 적용 함수 (weekday/인덱스 없이 날짜 텍스트로 판단)
    def style_cells(val):
        if "(토)" in str(val): return 'color: #1E88E5; font-weight: bold;'
        if "(일)" in str(val): return 'color: #E53935; font-weight: bold;'
        if user_name != "안 함" and str(val) == user_name:
            return f'background-color: {WORKER_COLORS.get(user_name, "white")}; color: black;'
        return 'color: black;'

    st.dataframe(
        df_cal.style.applymap(style_cells),
        use_container_width=True,
        hide_index=True 
    )

elif menu == "📍 근무 상황판":
    st.markdown("<div class='main-title'>C조 근무 상황판</div>", unsafe_allow_html=True)
    selected_date = st.date_input("📅 날짜 선택", now.date())
    st.info("새로운 순서 규칙이 적용된 상세 시간표입니다.")
    # 상황판 로직에도 동일한 로테이션 규칙 적용 가능
