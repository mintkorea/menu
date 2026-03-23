import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 및 데이터 ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

# --- 2. CSS 스타일 (인덱스 강제 숨기기 및 폰트 확대) ---
st.markdown("""
    <style>
    /* 1. 표의 가장 왼쪽 인덱스(0, 1, 2...) 열을 완전히 숨김 */
    thead tr th:first-child, tbody tr td:first-child { display: none !important; }
    
    /* 2. 전체 폰트 크기 확대 및 중앙 정렬 */
    html, body, [data-testid="stTable"] { font-size: 15px !important; }
    table { width: 100% !important; border-collapse: collapse; }
    th, td { text-align: center !important; padding: 12px 8px !important; border: 1px solid #ccc !important; }
    th { background-color: #f0f2f6; font-weight: bold; }
    
    /* 3. 타이틀 디자인 */
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    .period-text { font-size: 17px; color: #555; text-align: center; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 설정 ---
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    user_name = st.selectbox("👤 본인 성함 강조", ["안 함", "황재업"] + WORKERS)
    duration = st.number_input("📅 조회 기간(개월)", min_value=1, max_value=12, value=1)

# --- 4. 근무표 생성 로직 ---
now = datetime.now().date()
end_date = now + timedelta(days=30 * duration)

st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
st.markdown(f"<div class='period-text'>({now.strftime('%m월 %d일')} ~ {end_date.strftime('%m월 %d일')})</div>", unsafe_allow_html=True)

cal_list = []
curr = now
while curr <= end_date:
    diff = (curr - START_DATE).days
    if diff % 3 == 0:
        s = (diff // 3) % 3
        wd = curr.weekday()
        cal_list.append({
            "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
            "회관": WORKERS[(0+s)%3],
            "의산A": WORKERS[(1+s)%3],
            "의산B": WORKERS[(2+s)%3],
            "조장": "황재업",
            "weekday": wd  # 계산용 (화면에는 숨김)
        })
    curr += timedelta(days=1)

df_cal = pd.DataFrame(cal_list)

# --- 5. 스타일 적용 및 출력 (핵심 수정 부분) ---
def apply_style(row):
    styles = []
    # 주말 색상 설정
    date_color = "black"
    if row['weekday'] == 5: date_color = "#1E88E5" # 토요일 파랑
    elif row['weekday'] == 6: date_color = "#E53935" # 일요일 빨강
    
    for col in df_cal.columns:
        if col == "weekday": 
            styles.append("") 
            continue
            
        bg = "white"
        # 본인 이름 강조
        if user_name != "안 함" and str(row[col]) == user_name:
            bg = WORKER_COLORS.get(user_name, "white")
            
        style = f'background-color: {bg};'
        if col == "날짜":
            style += f' color: {date_color}; font-weight: bold;'
        styles.append(style)
    return styles

# hide(subset=["weekday"])로 weekday 열을 지우고, CSS로 인덱스까지 지워 표를 정렬합니다.
st.table(
    df_cal.style.apply(apply_style, axis=1)
    .hide(axis="columns", subset=["weekday"])
)
