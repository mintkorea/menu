import streamlit as st
import pandas as pd
from datetime import datetime

# --- [1] 기본 설정 및 스타일 ---
st.set_page_config(page_title="실시간 근무 현황", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    .status-container { 
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
        gap: 15px; 
        margin-bottom: 25px; 
    }
    .status-card {
        border: 2px solid #2E4077; 
        border-radius: 12px;
        padding: 15px; 
        text-align: center; 
        background-color: #F8F9FA;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .name-label { font-size: 16px; font-weight: 600; color: #555; margin-bottom: 5px; }
    .loc-label { font-size: 24px; font-weight: 800; color: #C04B41; }
    .highlight-row { background-color: #FFE5E5 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 데이터 정의 (24시간 근무표) ---
# 기존 로직에서 변수(h, a, b)를 고정된 이름이나 성함으로 대체하여 단순화했습니다.
# 필요 시 h, a, b 변수 계산 로직을 다시 넣을 수 있으나, 현재는 '실시간 확인'에 집중합니다.
columns = ["시작", "종료", "황재업", "조장", "의산A", "의산B"]
time_data = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "순찰/휴"],
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "순찰/로", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "순찰/로"], ["16:00", "17:00", "휴게", "안내실", "순찰/로", "로비"],
    ["17:00", "18:00", "안내실", "순찰", "로비", "휴게"], ["18:00", "19:00", "안내실", "로비", "휴게", "순찰"],
    ["19:00", "20:00", "순찰", "휴게", "안내실", "로비"], ["20:00", "21:00", "안내실", "순찰", "휴게", "로비"],
    ["21:00", "22:00", "휴게", "안내실", "로비", "순찰"], ["22:00", "23:00", "안내실", "로비", "순찰", "휴게"],
    ["23:00", "00:00", "순찰", "휴게", "로비", "안내실"], ["00:00", "01:00", "안내실", "휴게", "로비", "순찰"],
    ["01:00", "02:00", "휴게", "로비", "순찰", "안내실"], ["02:00", "03:00", "순찰", "안내실", "휴게", "로비"],
    ["03:00", "04:00", "로비", "순찰", "안내실", "휴게"], ["04:00", "05:00", "안내실", "휴게", "로비", "순찰"],
    ["05:00", "06:00", "휴게", "순찰", "안내실", "로비"], ["06:00", "07:00", "로비", "안내실", "순찰", "휴게"]
]
df_time = pd.DataFrame(time_data, columns=columns)

# --- [3] 현재 시간 기준 근무자 위치 추출 ---
now = datetime.now()
now_hour = now.hour
current_row = df_time[df_time['시작'].apply(lambda x: int(x.split(':')[0])) == now_hour].iloc[0]

# --- [4] 상단 실시간 현황판 (UI) ---
st.subheader(f"🕒 현재 시각: {now.strftime('%H:%M')} 근무 현황")
status_html = f"""
    <div class="status-container">
        <div class="status-card"><div class="name-label">황재업</div><div class="loc-label">{current_row['황재업']}</div></div>
        <div class="status-card"><div class="name-label">조장</div><div class="loc-label">{current_row['조장']}</div></div>
        <div class="status-card"><div class="name-label">의산A</div><div class="loc-label">{current_row['의산A']}</div></div>
        <div class="status-card"><div class="name-label">의산B</div><div class="loc-label">{current_row['의산B']}</div></div>
    </div>
"""
st.markdown(status_html, unsafe_allow_html=True)

# --- [5] 전체 타임테이블 및 현재 행 강조 ---
def highlight_current(row):
    if int(row['시작'].split(':')[0]) == now_hour:
        return ['background-color: #FFE5E5; color: black; font-weight: bold'] * len(row)
    return [''] * len(row)

st.markdown("### 📋 전체 근무 시간표")
st.table(df_time.style.apply(highlight_current, axis=1))
