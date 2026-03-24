import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [복구] 사이드바 포함 이미지 생성 당시 전체 통합 소스 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 Workplace", layout="wide")

# --- [1] CSS: 원본 스타일 유지 ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    .status-container { 
        display: grid; 
        grid-template-columns: 1fr 1fr; 
        gap: 10px; 
        margin-bottom: 20px; 
    }
    .status-card {
        border: 2px solid #2E4077; 
        border-radius: 10px;
        padding: 12px; 
        text-align: center; 
        background-color: white;
    }
    .name-label { font-size: 18px; font-weight: 800; color: #333; margin-bottom: 5px; border-bottom: 1px dotted #ccc; }
    .loc-label { font-size: 22px; font-weight: 800; color: #C04B41; }
    [data-testid="stTable"] { font-size: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 사이드바 설정 영역 ---
with st.sidebar:
    st.header("⚙️ 설정")
    today = datetime(2026, 3, 24).date()
    start_date = st.date_input("📅 조회 시작 날짜", today)
    duration = st.slider("📆 조회 일수", 7, 100, 31)
    user_focus = st.selectbox("👤 강조할 성함", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [3] 실시간 데이터 및 근무자 판정 로직 ---
now_hour = datetime.now().hour
days_diff = (today - PATTERN_START).days
sc = days_diff // 3
ci, i2 = (sc // 2) % 3, sc % 2 == 1

if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")

# 시간대별 근무 데이터
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
df_time = pd.DataFrame(time_data, columns=["F", "T", "조장", "성희", "의산A", "의산B"])

# 현재 시간 기준 장소 추출
current_locs = {"황재업": "안내실", h: "로비", a: "로비", b: "휴게"}
for row in time_data:
    if int(row[0].split(':')[0]) == now_hour:
        current_locs = {"황재업": row[2], h: row[3], a: row[4], b: row[5]}
        break

# --- [4] 메인 화면: 실시간 4칸 상황판 ---
st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="name-label">황재업</div><div class="loc-label">{current_locs['황재업']}</div></div>
        <div class="status-card"><div class="name-label">{h}</div><div class="loc-label">{current_locs.get(h, '로비')}</div></div>
        <div class="status-card"><div class="name-label">{a}</div><div class="loc-label">{current_locs.get(a, '로비')}</div></div>
        <div class="status-card"><div class="name-label">{b}</div><div class="loc-label">{current_locs.get(b, '휴게')}</div></div>
    </div>
""", unsafe_allow_html=True)

# --- [5] 메인 화면: 하단 타임테이블 ---
def highlight_row(row):
    if int(row['F'].split(':')[0]) == now_hour:
        return ['background-color: #FFE5E5; font-weight: bold'] * len(row)
    return [''] * len(row)

st.table(df_time.style.apply(highlight_row, axis=1))
