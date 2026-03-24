import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 모바일 최적화 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 22px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 14px !important; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 상단 4인 현황 카드 (스크린샷 23:52 스타일 반영) */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 12px; padding: 12px 0; 
        text-align: center; background: white;
    }
    .worker-name { font-size: 14px !important; font-weight: 700; color: #444; margin-bottom: 4px; }
    .status-val { font-size: 18px; font-weight: 900; color: #C04B41; }

    /* 표 가독성 및 헤더 숨기기 */
    [data-testid="stTable"] table { width: 100% !important; border-collapse: collapse; }
    [data-testid="stTable"] thead tr th { font-size: 11px !important; padding: 6px 2px !important; text-align: center !important; background-color: #f8f9fa !important; }
    [data-testid="stTable"] td { font-size: 12px !important; padding: 8px 2px !important; text-align: center !important; }
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜 및 근무자 로직 (07시 기준) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
# 07시 이전이면 전날 근무일로 고정
work_date = (now - timedelta(days=1)).date() if now.hour < 7 else now.date()
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers(d):
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "재업", "태언", ("정석" if i2 else "태원"), ("태원" if i2 else "정석")
        elif ci == 1: return "재업", "정석", ("태원" if i2 else "태언"), ("태언" if i2 else "태원")
        else: return "재업", "태원", ("정석" if i2 else "태언"), ("태언" if i2 else "정석")
    return "재업", "태언", "태원", "정석"

w1, w2, w3, w4 = get_workers(work_date)

# --- [3] 시간표 데이터 및 현재 인덱스 추출 ---
time_data = [
    ["07:00~08:00", "안내실", "로비", "로비", "휴게"], ["08:00~09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00~10:00", "순찰", "안내실", "휴게", "로비"], ["10:00~11:00", "휴게", "안내실", "로비", "순찰"],
    ["11:00~12:00", "안내실", "중식", "로비", "중식"], ["12:00~13:00", "중식", "안내실", "중식", "로비"],
    ["13:00~14:00", "안내실", "휴게", "순찰", "로비"], ["14:00~15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00~16:00", "안내실", "휴게", "로비", "휴게"], ["16:00~17:00", "휴게", "안내실", "휴게", "로비"],
    ["17:00~18:00", "안내실", "휴게", "휴게", "로비"], ["18:00~19:00", "안내실", "석식", "로비", "석식"],
    ["19:00~20:00", "안내실", "안내실", "석식", "로비"], ["20:00~21:00", "석식", "안내실", "로비", "휴게"],
    ["21:00~22:00", "안내실", "순찰", "로비", "휴게"], ["22:00~23:00", "순찰", "안내실", "순찰", "로비"],
    ["23:00~01:40", "안내실", "휴게", "휴게", "로비"], ["01:40~02:00", "안내실", "안내실", "로비", "로비"],
    ["02:00~05:00", "휴게", "안내실", "로비", "휴게"], ["05:00~06:00", "안내실", "순찰", "로비", "순찰"],
    ["06:00~07:00", "안내실", "안내실", "휴게", "로비"]
]

# 2단 헤더 구성 (스크린샷 00:03 재현)
header = pd.MultiIndex.from_tuples([
    ('시간', '구분'), 
    ('성의회관', w1), ('성의회관', w2), 
    ('의학연구원', w3), ('의학연구원', w4)
])
df_rt = pd.DataFrame(time_data, columns=header)

def get_current_idx():
    h = now.hour
    val = h if h >= 7 else h + 24
    for i, row in enumerate(time_data):
        sh = int(row[0].split(':')[0])
        if sh < 7: sh += 24
        eh = int(row[0].split('~')[1].split(':')[0])
        if eh <= 7: eh += 24
        if sh <= val < eh: return i
    return 0

curr_idx = get_current_idx()
curr_tasks = time_data[curr_idx][1:]

# --- [4] 화면 출력 ---
st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
st.markdown(f'<div class="title-sub">{work_date.strftime("%m/%d")} 근무 기준 (현재 {now.strftime("%H:%M")})</div>', unsafe_allow_html=True)

# 4인 현황 카드 (스크린샷 23:52 스타일)
st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="worker-name">{w1}</div><div class="status-val">{curr_tasks[0]}</div></div>
        <div class="status-card"><div class="worker-name">{w2}</div><div class="status-val">{curr_tasks[1]}</div></div>
        <div class="status-card"><div class="worker-name">{w3}</div><div class="status-val">{curr_tasks[2]}</div></div>
        <div class="status-card"><div class="worker-name">{w4}</div><div class="status-val">{curr_tasks[3]}</div></div>
    </div>
""", unsafe_allow_html=True)

if st.button("📋 당일 전체 시간표 보기"):
    st.table(df_rt)

st.markdown("### ▼ 현재 근무 상세")
# 현재 시간대 강조 표 (스크린샷 00:03 스타일의 표 형태)
st.table(df_rt.iloc[[curr_idx]].style.set_properties(**{'background-color': '#FFE5E5', 'font-weight': 'bold', 'color': 'black'}))
