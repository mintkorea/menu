import streamlit as st
import pandas as pd
from datetime import datetime

# --- [복구] 실시간 상황 및 타임테이블 작업 버전 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표 (실시간)", layout="wide")

# --- [1] CSS: 4칸 박스 및 테이블 디자인 ---
st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    
    /* 실시간 상황판 그리드 */
    .status-container { 
        display: grid; 
        grid-template-columns: 1fr 1fr; 
        gap: 10px; 
        margin-bottom: 20px; 
    }
    .status-card {
        border: 2px solid #2E4077; 
        border-radius: 12px;
        padding: 15px; 
        text-align: center; 
        background-color: white;
    }
    .name-label { font-size: 18px; font-weight: 800; color: #333; margin-bottom: 5px; border-bottom: 1px dotted #ccc; }
    .loc-label { font-size: 22px; font-weight: 800; color: #C04B41; }
    
    /* 시간표 스타일 */
    [data-testid="stTable"] { font-size: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 실시간 근무자 및 시간대 판정 ---
today = datetime(2026, 3, 24).date()
now_hour = datetime.now().hour
days_diff = (today - PATTERN_START).days

# 오늘 근무 명단 계산
sc = days_diff // 3
ci, i2 = (sc // 2) % 3, sc % 2 == 1
if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")

# --- [3] 실시간 근무지 4칸 박스 출력 ---
# 현재 시간(now_hour)에 따른 위치 데이터 (예시 로직)
loc_data = {
    "황재업": "안내실", 
    h: "로비", 
    a: "로비", 
    b: "휴게"
}

st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="name-label">황재업</div><div class="loc-label">{loc_data['황재업']}</div></div>
        <div class="status-card"><div class="name-label">{h}</div><div class="loc-label">{loc_data[h]}</div></div>
        <div class="status-card"><div class="name-label">{a}</div><div class="loc-label">{loc_data[a]}</div></div>
        <div class="status-card"><div class="name-label">{b}</div><div class="loc-label">{loc_data[b]}</div></div>
    </div>
""", unsafe_allow_html=True)

# --- [4] 시간대별 근무표 (Time Table) ---
time_slots = [
    {"F": "07:00", "T": "08:00", "조장": "안내실", "성희": "로비", "의산A": "로비", "의산B": "휴게"},
    {"F": "08:00", "T": "09:00", "조장": "안내실", "성희": "휴게", "의산A": "휴게", "의산B": "로비"},
    {"F": "09:00", "T": "10:00", "조장": "안내실", "성희": "순찰", "의산A": "휴게", "의산B": "로비"},
    {"F": "10:00", "T": "11:00", "조장": "휴게", "성희": "안내실", "의산A": "로비", "의산B": "순찰/휴"},
    {"F": "11:00", "T": "12:00", "조장": "안내실", "성희": "중식", "의산A": "로비", "의산B": "중식"},
    {"F": "12:00", "T": "13:00", "조장": "중식", "성희": "안내실", "의산A": "중식", "의산B": "로비"},
    {"F": "13:00", "T": "14:00", "조장": "안내실", "성희": "휴게", "의산A": "순찰/로", "의산B": "로비"},
    {"F": "14:00", "T": "15:00", "조장": "순찰", "성희": "안내실", "의산A": "로비", "의산B": "휴게"},
]

df_time = pd.DataFrame(time_slots)

# 현재 시간대 강조 색상 적용
def highlight_time(row):
    start_h = int(row['F'].split(':')[0])
    if start_h == now_hour:
        return ['background-color: #FFE5E5'] * len(row)
    return [''] * len(row)

st.table(df_time.style.apply(highlight_time, axis=1))
