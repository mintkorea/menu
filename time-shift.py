import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 및 데이터 (3/24 기준점 고정) ---
# 이미지의 3/24 배치를 0회차로 기준 설정
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

# [이미지 기반] 시간표 패턴 (실시간 상황판용)
BASE_PATTERN = [
    {"시간": "07:00", "조": "안내실", "회": "로비", "A": "휴게", "B": "로비"},
    {"시간": "08:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴게"},
    {"시간": "09:00", "조": "안내실", "회": "순찰", "A": "로비", "B": "휴게"},
    {"시간": "10:00", "조": "휴게", "회": "안내실", "A": "순찰/휴", "B": "로비"},
    {"시간": "11:00", "조": "안내실", "회": "중식", "A": "중식", "B": "로비"},
    {"시간": "12:00", "조": "중식", "회": "안내실", "A": "로비", "B": "중식"},
    {"시간": "13:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴/순"},
    {"시간": "14:00", "조": "순찰", "회": "안내실", "A": "휴게", "B": "로비"},
    {"시간": "15:00", "조": "안내실", "회": "휴게", "A": "휴게", "B": "로비"},
    {"시간": "16:00", "조": "휴게", "회": "안내실", "A": "로비", "B": "휴게"},
    {"시간": "17:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴게"},
    {"시간": "18:00", "조": "안내실", "회": "휴게", "A": "휴게", "B": "로비"},
    {"시간": "19:00", "조": "안내실", "회": "석식", "A": "로비", "B": "석식"},
    {"시간": "20:00", "조": "안내실", "회": "안내실", "A": "석식", "B": "로비"},
    {"시간": "21:00", "조": "석식", "회": "안내실", "A": "로비", "B": "휴게"},
    {"시간": "22:00", "조": "안내실", "회": "순찰", "A": "로비", "B": "휴게"},
    {"시간": "23:00", "조": "순찰", "회": "취침", "A": "순찰", "B": "로비"},
    {"시간": "00:00", "조": "안내실", "회": "취침", "A": "취침", "B": "로비"},
    {"시간": "03:00", "조": "취침", "회": "회관근무", "A": "로비", "B": "취침"},
    {"시간": "06:00", "조": "안내실", "회": "회관근무", "A": "로비", "B": "순찰"},
]

st.set_page_config(page_title="성의교정 C조", layout="centered")

# --- 2. CSS 스타일 (중앙 정렬 및 시각 최적화) ---
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

# --- 3. 사이드바 메뉴 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴 선택", ["📅 교대 근무표", "📍 실시간 상황판"])
    user_name = st.selectbox("👤 이름 강조 (본인 선택)", ["안 함", "황재업"] + WORKERS)
    duration = st.number_input("📅 조회 기간(개월)", min_value=1, max_value=6, value=1)

# --- 4. 메인 로직 ---
now = datetime.now()

if menu == "📅 교대 근무표":
    st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    
    cal_list = []
    curr = START_DATE
    end_date = curr + timedelta(days=30 * duration)
    
    while curr <= end_date:
        diff_days = (curr - START_DATE).days
        if diff_days % 3 == 0:
            # 2회 연속 근무 규칙 적용 (6일 주기 로테이션)
            shift_idx = (diff_days // 3) // 2 % 3
            
            if shift_idx == 0: # 1, 2회차 (이태원-이정석-김태언)
                a, b, c = "이태원", "이정석", "김태언"
            elif shift_idx == 1: # 3, 4회차 (김태언-이태원-이정석)
                a, b, c = "김태언", "이태원", "이정석"
            else: # 5, 6회차 (이정석-김태언-이태원)
                a, b, c = "이정석", "김태언", "이태원"
            
            wd = curr.weekday()
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": "황재업",
                "성희(A)": a,
                "의산(B)": b,
                "의산(C)": c
            })
        curr += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)

    def style_cal(val):
        if "(토)" in str(val): return 'color: #1E88E5; font-weight: bold;'
        if "(일)" in str(val): return 'color: #E53935; font-weight: bold;'
        if user_name != "안 함" and str(val) == user_name:
            return f'background-color: {WORKER_COLORS.get(user_name, "white")}; color: black;'
        return 'color: black;'

    st.dataframe(df_cal.style.applymap(style_cal), use_container_width=True, hide_index=True)

elif menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>C조 실시간 근무 상황판</div>", unsafe_allow_html=True)
    selected_date = st.date_input("📅 날짜 선택", now.date())
    
    diff = (selected_date - START_DATE).days
    if diff % 3 == 0:
        shift_idx = (diff // 3) // 2 % 3
        names = [("이태원", "이정석", "김태언"), ("김태언", "이태원", "이정석"), ("이정석", "김태언", "이태원")][shift_idx]
        
        st.success(f"✅ {selected_date.strftime('%Y-%m-%d')} 근무일입니다.")
        df_board = pd.DataFrame([
            {"시간": r["시간"], "황재업(조)": r["조"], f"{names[0]}(A)": r["회"], f"{names[1]}(B)": r["A"], f"{names[2]}(C)": r["B"]}
            for r in BASE_PATTERN
        ])
        st.dataframe(df_board, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ 선택하신 날짜는 C조 비번(휴무)입니다.")
