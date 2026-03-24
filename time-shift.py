import streamlit as st
import pandas as pd
from datetime import datetime

# --- [복구] 이미지 생성 당시 전체 통합 소스 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 Workplace", layout="wide")

# --- [1] CSS: 4칸 박스 및 테이블 스타일 ---
st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    
    /* 실시간 근무지 4칸 박스 레이아웃 */
    .status-container { 
        display: grid; 
        grid-template-columns: 1fr 1fr; 
        gap: 12px; 
        margin-bottom: 25px; 
    }
    .status-card {
        border: 2px solid #2E4077; 
        border-radius: 12px;
        padding: 15px; 
        text-align: center; 
        background-color: white;
    }
    .name-label { font-size: 18px; font-weight: 800; color: #333; margin-bottom: 5px; border-bottom: 1px dotted #ccc; padding-bottom: 5px; }
    .loc-label { font-size: 24px; font-weight: 800; color: #C04B41; }
    
    /* 테이블 가독성 설정 */
    [data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 실시간 근무자 및 시간대 데이터 로직 ---
# 오늘 날짜 및 현재 시간 추출
today = datetime(2026, 3, 24).date()
now_time = datetime.now().strftime("%H:%M")
now_hour = datetime.now().hour

# 근무 순번 계산
days_diff = (today - PATTERN_START).days
sc = days_diff // 3
ci, i2 = (sc // 2) % 3, sc % 2 == 1

if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")

# 시간대별 근무지 데이터
time_data = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"],
    ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"],
    ["10:00", "11:00", "휴게", "안내실", "로비", "순찰/휴"],
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"],
    ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "순찰/로", "로비"],
    ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "순찰/로"],
    ["16:00", "17:00", "휴게", "안내실", "순찰/로", "로비"],
    ["17:00", "18:00", "안내실", "순찰", "로비", "휴게"],
]
df_time = pd.DataFrame(time_data, columns=["From", "To", "조장", "성희", "의산A", "의산B"])

# --- [3] 현재 시간 기준 근무지 추출 로직 ---
current_locs = {"황재업": "안내실", h: "로비", a: "로비", b: "휴게"} # 기본값

for row in time_data:
    start_h = int(row[0].split(':')[0])
    if start_h == now_hour:
        current_locs = {"황재업": row[2], h: row[3], a: row[4], b: row[5]}
        break

# --- [4] 상단 실시간 4칸 상황판 출력 ---
st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="name-label">황재업</div><div class="loc-label">{current_locs.get('황재업', '안내실')}</div></div>
        <div class="status-card"><div class="name-label">{h}</div><div class="loc-label">{current_locs.get(h, '로비')}</div></div>
        <div class="status-card"><div class="name-label">{a}</div><div class="loc-label">{current_locs.get(a, '로비')}</div></div>
        <div class="status-card"><div class="name-label">{b}</div><div class="loc-label">{current_locs.get(b, '휴게')}</div></div>
    </div>
""", unsafe_allow_html=True)

# --- [5] 하단 타임테이블 출력 (현재 시간 행 강조) ---
def highlight_current(row):
    start_h = int(row['From'].split(':')[0])
    if start_h == now_hour:
        return ['background-color: #FFE5E5; font-weight: bold'] * len(row) # 옅은 빨강 강조
    return [''] * len(row)

st.table(df_time.style.apply(highlight_current, axis=1))
