import streamlit as st
import pandas as pd
from datetime import datetime

# --- [1] 설정 및 스타일 ---
st.set_page_config(page_title="C조 실시간 근무 현황", layout="wide")

st.markdown("""
    <style>
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 15px; text-align: center; background: white; }
    .name-label { font-size: 16px; color: #666; margin-bottom: 5px; border-bottom: 1px solid #eee; }
    .loc-label { font-size: 22px; font-weight: 800; color: #C04B41; }
    .highlight { background-color: #FFF2F2 !important; font-weight: bold; border-left: 5px solid red !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 이미지 기반 근무 데이터 정밀 재구성 ---
# 이미지의 From ~ To 시간을 분 단위까지 고려하여 리스트업
time_data = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"],
    ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"],
    ["10:00", "11:00", "휴게", "안내실", "로비", "순찰/휴"], # 10:30분 교대 반영
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"],
    ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "휴게/순", "로비"], # 13:30분 순찰 반영
    ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"],
    ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"],
    ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"],
    ["18:00", "19:00", "안내실", "석식", "로비", "석식"], # 석식 로테이션
    ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], # 석식 로테이션
    ["20:00", "21:00", "석식/안내", "안내실", "로비", "휴게"],
    ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"],
    ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"], # 22:30 교대 포함
    ["23:00", "01:40", "안내실", "휴게", "휴게", "로비"], # 심야 롱타임
    ["01:40", "02:00", "안내실", "안내실", "로비", "로비"], 
    ["02:00", "05:00", "휴게", "안내실", "로비", "휴게"], # 새벽 롱타임
    ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"],
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"],
]
df_time = pd.DataFrame(time_data, columns=["From", "To", "조장", "대원", "당직A", "당직B"])

# --- [3] 실시간 위치 판단 ---
now_time = datetime.now().strftime("%H:%M")

def get_current_row(now_str):
    for idx, row in df_time.iterrows():
        # 23:00 ~ 01:40 같은 익일 처리 포함 로직
        start, end = row['From'], row['To']
        if end == "00:00": end = "24:00"
        if start <= now_str < end or (start > end and (now_str >= start or now_str < end)):
            return row
    return df_time.iloc[0] # 예외 시 첫 행

curr = get_current_row(now_time)

# --- [4] 화면 표시 ---
st.subheader(f"🕒 현재 시각: {now_time} 근무 현황")

st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="name-label">조장 (황재업)</div><div class="loc-label">{curr['조장']}</div></div>
        <div class="status-card"><div class="name-label">대원 (성희)</div><div class="loc-label">{curr['대원']}</div></div>
        <div class="status-card"><div class="name-label">당직 A (의산)</div><div class="loc-label">{curr['당직A']}</div></div>
        <div class="status-card"><div class="name-label">당직 B (의산)</div><div class="loc-label">{curr['당직B']}</div></div>
    </div>
""", unsafe_allow_html=True)

# --- [5] 테이블 표시 (현재 시간 강조) ---
def styling(row):
    start, end = row['From'], row['To']
    if end == "00:00": end = "24:00"
    if start <= now_time < end or (start > end and (now_time >= start or now_time < end)):
        return ['background-color: #FFE5E5'] * len(row)
    return [''] * len(row)

st.table(df_time.style.apply(styling, axis=1))
