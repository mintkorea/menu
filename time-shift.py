import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 데이터 및 설정 ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

st.set_page_config(page_title="성의교정 C조", layout="centered")

# --- 2. CSS 스타일 (표 및 텍스트 중앙 정렬) ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    .period-text { font-size: 18px; color: #555; text-align: center; margin-bottom: 20px; }
    
    /* 표 전체 중앙 정렬 및 셀 텍스트 중앙 정렬 */
    [data-testid="stDataFrame"] { justify-content: center; display: flex; }
    .stDataFrame div[data-testid="stTable"] div { text-align: center !important; }
    
    /* 사이드바 스타일 */
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

# --- 4. 근무표 로직 ---
now = datetime.now()

if menu == "📅 교대 근무표":
    start_v = now.date()
    end_v = start_v + timedelta(days=30 * duration)
    st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='period-text'>({start_v.strftime('%m월 %d일')} ~ {end_v.strftime('%m월 %d일')})</div>", unsafe_allow_html=True)

    cal_list = []
    curr = start_v
    while curr <= end_v:
        diff = (curr - START_DATE).days
        if diff % 3 == 0:
            s = (diff // 3) % 3
            wd = curr.weekday()
            # weekday 열은 만들지 않고 조장을 날짜 옆으로 배치
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": "황재업",
                "회관": WORKERS[(0+s)%3],
                "의산A": WORKERS[(1+s)%3],
                "의산B": WORKERS[(2+s)%3]
            })
        curr += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)

    # --- 5. 셀 단위 스타일 적용 함수 ---
    def style_cells(val):
        # 1. 주말 색상 (날짜 셀에만 적용)
        if "(토)" in str(val): return 'color: #1E88E5; font-weight: bold; text-align: center;'
        if "(일)" in str(val): return 'color: #E53935; font-weight: bold; text-align: center;'
        
        # 2. 선택한 이름 강조 (해당 셀만 배경색 변경)
        if user_name != "안 함" and str(val) == user_name:
            bg_color = WORKER_COLORS.get(user_name, "white")
            return f'background-color: {bg_color}; color: black; text-align: center;'
        
        return 'color: black; text-align: center;'

    # 열 전체에 스타일 적용 (applymap 사용)
    st.dataframe(
        df_cal.style.applymap(style_cells),
        use_container_width=True,
        hide_index=True # 인덱스 삭제
    )

elif menu == "📍 근무 상황판":
    st.markdown("<div class='main-title'>C조 근무 상황판</div>", unsafe_allow_html=True)
    selected_date = st.date_input("📅 날짜 선택", now.date())
    st.info("선택하신 날짜의 상세 시간표가 준비되었습니다.")
    # 상황판도 위와 동일한 applymap(style_cells) 구조를 사용하면 셀별 강조가 가능합니다.
