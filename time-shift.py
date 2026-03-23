import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 (3/9 패턴 시작점 고정) ---
# 선임순: 1.김태언, 2.이태원, 3.이정석
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

st.set_page_config(page_title="성의교정 C조 관리", layout="centered")

# --- 2. CSS 스타일 (중앙 정렬) ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    .period-text { font-size: 16px; color: #666; text-align: center; margin-bottom: 25px; }
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
    st.markdown("<div class='period-text'>(3월 9일 패턴 시작 기준)</div>", unsafe_allow_html=True)
    
    cal_list = []
    # 오늘 날짜 기준으로 표를 보여주되, 계산은 3/9부터 수행
    curr = datetime.now().date()
    end_date = curr + timedelta(days=30 * duration)
    
    # 3/9부터의 모든 근무일을 계산하여 리스트화
    check_date = PATTERN_START_DATE
    while check_date <= end_date:
        diff_days = (check_date - PATTERN_START_DATE).days
        if diff_days % 3 == 0:
            shift_count = diff_days // 3  # 3/9부터 몇 번째 근무인지
            cycle_idx = (shift_count // 2) % 3 # 회관 담당자 (2회씩)
            is_second_day = shift_count % 2 == 1 # 2회 중 두 번째 날인지 (A/B 교대)
            
            # 규칙 반영:
            # 1. 회관 순서: 김태언 -> 이정석 -> 이태원
            # 2. 의산연 A/B: 나머지 2명이 첫날은 '선임-후임', 둘째날은 '후임-선임' 교대
            if cycle_idx == 0:
                # 회관: 김태언 / 나머지: 이태원(선), 이정석(후)
                h = "김태언"
                a, b = ("이정석", "이태원") if is_second_day else ("이태원", "이정석")
            elif cycle_idx == 1:
                # 회관: 이정석 / 나머지: 김태언(선), 이태원(후)
                h = "이정석"
                a, b = ("이태원", "김태언") if is_second_day else ("김태언", "이태원")
            else:
                # 회관: 이태원 / 나머지: 김태언(선), 이정석(후)
                h = "이태원"
                a, b = ("이정석", "김태언") if is_second_day else ("김태언", "이정석")
            
            # 오늘 이후의 데이터만 표에 추가
            if check_date >= datetime.now().date():
                wd = check_date.weekday()
                cal_list.append({
                    "날짜": f"{check_date.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                    "조장": "황재업",
                    "성희(회관)": h,
                    "의산(A)": a,
                    "의산(B)": b
                })
        check_date += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)
    
    def style_cells(val):
        if "(토)" in str(val): return 'color: #1E88E5; font-weight: bold;'
        if "(일)" in str(val): return 'color: #E53935; font-weight: bold;'
        if user_name != "안 함" and str(val) == user_name:
            return f'background-color: {WORKER_COLORS.get(user_name, "white")}; color: black;'
        return 'color: black;'

    st.dataframe(df_cal.style.applymap(style_cells), use_container_width=True, hide_index=True)

elif menu == "📍 실시간 상황판":
    st.info("실시간 상황판 메뉴입니다.")
