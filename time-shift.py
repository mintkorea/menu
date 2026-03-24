import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 기본 설정 및 디자인 ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 26px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 14px !important; text-align: center; color: #666; margin-bottom: 15px; }
    .worker-card { border: 2px solid #31333f; border-radius: 10px; padding: 8px; text-align: center; margin-bottom: 8px; }
    .worker-name { font-weight: 700; color: #31333f; font-size: 15px; }
    .worker-loc { font-size: 19px; font-weight: 800; color: #a64d79; }
    /* 표 헤더 스타일 */
    thead tr th { background-color: #f0f2f6 !important; font-size: 13px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 07시 기준 날짜 및 근무자 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
target_date = (now - timedelta(days=1)).date() if now.hour < 7 else now.date()
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(d):
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci = (sc // 2) % 3
        if ci == 0: return "재업", "태원", "정석", "태언"
        elif ci == 1: return "재업", "정석", "태언", "태원"
        else: return "재업", "태언", "태원", "정석"
    return "재업", "태원", "정석", "태언"

w1, w2, w3, w4 = get_workers_by_date(target_date)

# --- [3] 데이터프레임 생성 (2단 헤더 구조 재현) ---
# 스크린샷처럼 성의회관(재업, 태원), 의학연구원(정석, 태언) 구조
columns = [
    ('시간', ''), 
    ('성의회관', w1), ('성의회관', w2), 
    ('의학연구원', w3), ('의학연구원', w4)
]
df_columns = pd.MultiIndex.from_tuples(columns)

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
df_rt = pd.DataFrame(time_data, columns=df_columns)

# --- [4] 현재 인덱스 탐색 ---
def get_curr_idx():
    h, m = now.hour, now.minute
    val = h if h >= 7 else h + 24
    if val == 25 and m < 40: return 16
    for i, r in enumerate(time_data):
        start_h = int(r[0].split(':')[0])
        if start_h < 7: start_h += 24
        if start_h <= val: curr = i
    return curr

idx = get_curr_idx()

# --- [5] 메인 화면 출력 ---
st.markdown('<div class="unified-title">C조 실시간 현황</div>', unsafe_allow_html=True)
st.markdown(f'<div class="title-sub">{target_date.strftime("%m/%d")} 근무 ({now.strftime("%H:%M")})</div>', unsafe_allow_html=True)

# 카드 레이아웃
c1, c2 = st.columns(2)
c3, c4 = st.columns(2)
workers = [w1, w2, w3, w4]
locs = time_data[idx][1:]
for i, col in enumerate([c1, c2, c3, c4]):
    col.markdown(f'<div class="worker-card"><div class="worker-name">황{workers[i] if i==0 else workers[i]}</div><div class="worker-loc">{locs[i]}</div></div>', unsafe_allow_html=True)

with st.expander("📋 당일 전체 시간표 보기"):
    st.table(df_rt)

st.markdown("#### ▼ 현재 근무 및 다음 스케줄")
# 현재 시간부터 끝까지(iloc[idx:]) 출력하며 현재 줄 강조
st.table(df_rt.iloc[idx:].style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*5 if r.name == idx else ['']*5, axis=1))
