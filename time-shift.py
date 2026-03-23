import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [v1.03] 실시간 오늘 날짜 동기화 버전 ---
# 기준일 설정
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표 v1.03", layout="wide")

# --- [1] CSS: 사용자 황금 레이아웃 보존 ---
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; }
    
    .fixed-title { 
        font-size: 28px !important; 
        font-weight: 800 !important;
        margin-bottom: 5px !important;
        color: #1E1E1E !important; 
        padding: 5px 0;
    }
    
    .status-line {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 20px;
        border-left: 5px solid #007bff;
        font-size: 16px;
        line-height: 1.5;
    }
    
    [data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# [타이틀 및 버전 표시]
st.markdown('<div class="fixed-title">📅 C조 근무 편성표 <small style="font-size:14px; color:gray; font-weight:normal;">v1.03</small></div>', unsafe_allow_html=True)

# --- [2] 실시간 오늘 날짜 및 근무 로직 (수정됨) ---
# 서버 시간이 아닌 사용자 현지 시간 기준 오늘 날짜 호출
now = datetime.now()
today = now.date() 
current_time = now.strftime("%H:%M")

days_diff = (today - PATTERN_START).days
is_workday = (days_diff % 3 == 0)

if is_workday:
    sc = days_diff // 3
    ci, i2 = (sc // 2) % 3, sc % 2 == 1
    if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
    elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
    else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    
    status_msg = f"📍 **오늘({today.strftime('%m/%d %a')})은 근무일입니다.** (현재 {current_time})<br>👤 **근무자:** 황재업, {h}, {a}, {b}"
else:
    next_work_days = 3 - (days_diff % 3)
    next_work_date = today + timedelta(days=next_work_days)
    status_msg = f"✅ **오늘({today.strftime('%m/%d %a')})은 비번입니다.** (현재 {current_time})<br>🗓️ **다음 근무:** {next_work_date.strftime('%m/%d(%a)')} ({next_work_days}일 후)"

st.markdown(f'<div class="status-line">{status_msg}</div>', unsafe_allow_html=True)

# --- [3] 조회 설정 (사용자 3단 레이아웃 유지) ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    # 조회 시작 날짜 기본값을 오늘로 설정하여 편의성 증대
    start_date = st.date_input("📅 조회 시작 날짜", today)
with col2:
    duration = st.slider("📆 조회 일수", 7, 100, 31)
with col3:
    user_focus = st.selectbox("👤 강조할 성함", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 데이터 및 색상 로직 (이미지 기준 정확한 색상) ---
color_map = {
    "황재업": "#D1FAE5", 
    "김태언": "#FFF2CC", # 노랑
    "이태원": "#FFE5D9", # 살구
    "이정석": "#FDE2E2"  # 연분홍
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

# --- [5] 표 출력 ---
if not df.empty:
    st.dataframe(
        df.style.apply(apply_style, axis=1),
        use_container_width=True,
        hide_index=True,
        height=(len(df) + 1) * 38 
    )
