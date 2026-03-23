import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 (3/27 신규 로테이션 시작) ---
NEW_START_DATE = datetime(2026, 3, 27).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

st.set_page_config(page_title="성의교정 C조 관리", layout="centered")

# --- 2. CSS 스타일 (중앙 정렬 및 UI) ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    [data-testid="stDataFrame"] { justify-content: center; display: flex; }
    .stDataFrame div[data-testid="stTable"] div { text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴", ["📅 교대 근무표", "📍 실시간 상황판"])
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])
    duration = st.number_input("📅 조회 기간(개월)", min_value=1, max_value=6, value=1)

# --- 4. 근무 편성 로직 ---
if menu == "📅 교대 근무표":
    st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    
    cal_list = []
    curr = NEW_START_DATE
    end_date = curr + timedelta(days=30 * duration)
    
    while curr <= end_date:
        diff_days = (curr - NEW_START_DATE).days
        if diff_days % 3 == 0:
            shift_count = diff_days // 3  # 몇 번째 근무일인지
            cycle_idx = (shift_count // 2) % 3 # 회관 담당자 결정을 위한 2회 주기 인덱스
            is_second_day = shift_count % 2 == 1 # 2회 연속 중 두 번째 날인지 여부
            
            # [규칙 1] 회관 순서: 김태언 -> 이정석 -> 이태원 (각 2회 연속)
            # [규칙 2] 의산연 A/B: 나머지 2명이 첫날은 '선임-후임', 둘째날은 '후임-선임'으로 교대
            
            if cycle_idx == 0:
                # 1,2회차 회관: 김태언 / 의산연: 이태원(선임), 이정석(후임)
                h = "김태언"
                a, b = ("이정석", "이태원") if is_second_day else ("이태원", "이정석")
            elif cycle_idx == 1:
                # 3,4회차 회관: 이정석 / 의산연: 김태언(선임), 이태원(후임)
                h = "이정석"
                a, b = ("이태원", "김태언") if is_second_day else ("김태언", "이태원")
            else:
                # 5,6회차 회관: 이태원 / 의산연: 김태언(선임), 이정석(후임)
                h = "이태원"
                a, b = ("이정석", "김태언") if is_second_day else ("김태언", "이정석")
            
            wd = curr.weekday()
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": "황재업",
                "성희(회관)": h,
                "의산(A)": a,
                "의산(B)": b
            })
        curr += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)
    
    def style_cells(val):
        if "(토)" in str(val): return 'color: #1E88E5; font-weight: bold;'
        if "(일)" in str(val): return 'color: #E53935; font-weight: bold;'
        if user_name != "안 함" and str(val) == user_name:
            return f'background-color: {WORKER_COLORS.get(user_name, "white")}; color: black;'
        return 'color: black;'

    st.dataframe(df_cal.style.applymap(style_cells), use_container_width=True, hide_index=True)

elif menu == "📍 실시간 상황판":
    st.write("실시간 상황판 메뉴입니다.")
