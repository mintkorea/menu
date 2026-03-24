import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [복구] 다 버리라고 하기 직전의 원본 소스 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표", layout="wide")

# --- [1] CSS: 사용자 정의 스타일 (28px 타이틀 및 여백) ---
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; }
    .fixed-title { 
        font-size: 28px !important; 
        font-weight: 800 !important;
        margin-bottom: 10px !important;
        color: #1E1E1E !important; 
    }
    [data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="fixed-title">📅 C조 근무 편성표</div>', unsafe_allow_html=True)

# --- [2] 조회 설정: 가로 3단 컬럼 배치 ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    start_date = st.date_input("📅 조회 시작 날짜", datetime(2026, 3, 16).date())
with col2:
    duration = st.slider("📆 조회 일수", 7, 100, 31)
with col3:
    user_focus = st.selectbox("👤 강조할 성함", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [3] 데이터 및 색상 로직 ---
color_map = {
    "황재업": "#D1FAE5", 
    "김태언": "#FFF2CC", 
    "이태원": "#FFE5D9", 
    "이정석": "#FDE2E2"
}

cal_data = []
for i in range(duration):
    d = start_date + timedelta(days=i)
    diff = (d - PATTERN_START).days
    
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
        
        cal_data.append({
            "날짜": d.strftime("%m/%d(%a)"),
            "조장": "황재업", "성희": h, "의산A": a, "의산B": b
        })

df = pd.DataFrame(cal_data)

def apply_style(row):
    styles = [''] * len(row)
    if 'Sun' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
    elif 'Sat' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
    
    if user_focus != "안 함":
        bg_color = color_map.get(user_focus, "#FFF2CC")
        for i, val in enumerate(row):
            if val == user_focus:
                styles[i] = f'background-color: {bg_color}; font-weight: bold; color: black;'
    return styles

# --- [4] 데이터 출력 ---
if not df.empty:
    st.dataframe(
        df.style.apply(apply_style, axis=1),
        use_container_width=True,
        hide_index=True,
        height=(len(df) + 1) * 38 
    )
