import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 ---
# 이미지(1774264605856.png)의 3/24 배치를 기준점으로 설정
START_DATE = datetime(2026, 3, 24).date()
# 고정 순번 (2회 연속 근무를 위해 6일 주기로 구성)
# 순서: (이태원, 이정석, 김태언) -> (이태원, 이정석, 김태언) -> (김태언, 이태원, 이정석) ...
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

st.set_page_config(page_title="성의교정 C조", layout="centered")

# --- 2. CSS 스타일 (중앙 정렬) ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    .period-text { font-size: 18px; color: #555; text-align: center; margin-bottom: 20px; }
    [data-testid="stDataFrame"] { justify-content: center; display: flex; }
    .stDataFrame div[data-testid="stTable"] div { text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정")
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업"] + WORKERS)
    duration = st.number_input("📅 조회 기간(개월)", min_value=1, max_value=6, value=1)

# --- 4. 근무표 로직 (2회 연속 규칙 적용) ---
st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)

start_v = START_DATE
end_v = start_v + timedelta(days=30 * duration)

cal_list = []
curr = start_v
while curr <= end_v:
    diff_days = (curr - START_DATE).days
    if diff_days % 3 == 0:
        # 3일마다 근무가 돌아오므로, 'diff_days // 3'이 근무 차수임
        shift_count = diff_days // 3
        
        # 2회 연속 근무 규칙: 0,1회차 / 2,3회차 / 4,5회차 로테이션
        # 이미지의 3/24(이태원-이정석-김태언)를 0회차로 기준 잡음
        cycle = (shift_count // 2) % 3 
        
        if cycle == 0: # 1, 2회차 연속
            a, b, c = "이태원", "이정석", "김태언"
        elif cycle == 1: # 3, 4회차 연속
            a, b, c = "김태언", "이태원", "이정석"
        else: # 5, 6회차 연속
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

# --- 5. 스타일 적용 및 출력 ---
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
