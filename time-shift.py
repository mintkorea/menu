import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [v1.01] 실시간 상황 및 버전 업데이트 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표 v1.01", layout="wide")

# --- [1] CSS: 사용자님 소스 및 여백 유지 (헤더 미포함) ---
st.markdown("""
    <style>
    /* 타이틀 가독성을 위한 상단 여백 설정 */
    .block-container { padding-top: 3.5rem !important; }
    
    .fixed-title { 
        font-size: 28px !important; 
        font-weight: 800 !important;
        margin-bottom: 10px !important;
        color: #1E1E1E !important; 
        padding: 5px 0;
    }
    
    /* 실시간 상황판 스타일 */
    .status-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #007bff;
    }
    
    [data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# [타이틀 및 버전 v1.01 표시]
st.markdown('<div class="fixed-title">📅 C조 근무 편성표 <span style="font-size:16px; color:gray; font-weight:normal;">v1.01</span></div>', unsafe_allow_html=True)

# --- [2] 실시간 근무 상황 로직 ---
today = datetime.now().date()
days_diff = (today - PATTERN_START).days
is_workday = (days_diff % 3 == 0)

# 오늘 근무자 계산
if is_workday:
    sc = days_diff // 3
    ci, i2 = (sc // 2) % 3, sc % 2 == 1
    if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
    elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
    else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    status_msg = f"🚨 **오늘({today.strftime('%m/%d')})은 C조 근무일입니다!**<br>👉 근무자: 황재업, {h}, {a}, {b}"
else:
    next_work = today + timedelta(days=(3 - (days_diff % 3)))
    status_msg = f"✅ 오늘은 비번입니다. **다음 근무는 {next_work.strftime('%m/%d')}**입니다."

st.markdown(f'<div class="status-box">{status_msg}</div>', unsafe_allow_html=True)

# --- [3] 조회 설정 (사용자님 3단 컬럼 소스 유지) ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    start_date = st.date_input("📅 조회 시작 날짜", datetime(2026, 3, 16).date())
with col2:
    duration = st.slider("📆 조회 일수", 7, 100, 31)
with col3:
    user_focus = st.selectbox("👤 강조할 성함", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 데이터 생성 및 스타일 로직 ---
# 이미지 기반 색상값 유지
color_map = {
    "황재업": "#D1FAE5", "김태언": "#FFF2CC", "이태원": "#E0F2FE", "이정석": "#FEE2E2"
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
    # 토/일요일 색상 강조
    if 'Sun' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
    elif 'Sat' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
    
    if user_focus != "안 함":
        bg_color = color_map.get(user_focus, "#FFF2CC")
        for i, val in enumerate(row):
            if val == user_focus:
                styles[i] = f'background-color: {bg_color}; font-weight: bold; color: black;'
    return styles

# --- [5] 표 출력 (스크롤 방지) ---
if not df.empty:
    st.dataframe(
        df.style.apply(apply_style, axis=1),
        use_container_width=True,
        hide_index=True,
        height=(len(df) + 1) * 38 
    )
