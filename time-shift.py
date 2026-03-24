import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 기본 설정 및 CSS ---
st.set_page_config(page_title="C조 근무 시스템", layout="wide")
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 14px !important; text-align: center; color: #666; margin-bottom: 20px; }
    .worker-card { border: 2px solid #31333f; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 10px; }
    .worker-name { font-weight: 700; color: #31333f; margin-bottom: 5px; }
    .worker-loc { font-size: 18px; font-weight: 800; color: #a64d79; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 07시 기준 날짜 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
target_date = (now - timedelta(days=1)).date() if now.hour < 7 else now.date()
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(d):
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "이태원", "이정석", "김태언"
        elif ci == 1: return "황재업", "이정석", "김태언", "이태원"
        else: return "황재업", "김태언", "이태원", "이정석"
    return "황재업", "이태원", "이정석", "김태언"

j, s, a, b = get_workers_by_date(target_date)

# --- [3] 시간표 데이터 ---
time_data = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "순찰", "안내실", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "순찰"],
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"],
    ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"],
    ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"],
    ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"],
    ["23:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"],
    ["02:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"],
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"]
]
df_rt = pd.DataFrame(time_data, columns=["From", "To", j, s, a, b])

# --- [4] 현재 인덱스 찾기 ---
def get_curr_idx():
    h, m = now.hour, now.minute
    val = h if h >= 7 else h + 24
    if val == 25 and m < 40: return 16 
    for i, r in enumerate(time_data):
        sh = int(r[0].split(':')[0]); sh = sh if sh >= 7 else sh + 24
        eh = int(r[1].split(':')[0]); eh = eh if eh >= 7 else eh + 24
        if sh <= val < eh: return i
    return 0

curr_idx = get_curr_idx()

# --- [5] 화면 출력 ---
st.markdown(f'<div class="unified-title">C조 실시간 현황</div>', unsafe_allow_html=True)
st.markdown(f'<div class="title-sub">{target_date.strftime("%m/%d")} 근무 ({now.strftime("%H:%M")})</div>', unsafe_allow_html=True)

# 카드형 레이아웃
row1 = st.columns(2)
row2 = st.columns(2)
curr_row = time_data[curr_idx]
workers = [j, s, a, b]
for i, col in enumerate([row1[0], row1[1], row2[0], row2[1]]):
    with col:
        st.markdown(f"""
            <div class="worker-card">
                <div class="worker-name">{workers[i]}</div>
                <div class="worker-loc">{curr_row[i+2]}</div>
            </div>
            """, unsafe_allow_html=True)

# 전체 시간표 확인 버튼
with st.expander("📋 당일 전체 시간표 확인하기"):
    st.table(df_rt)

# 현재 근무 및 다음 스케줄
st.markdown("#### ▼ 현재 근무 및 다음 스케줄")
st.table(df_rt.iloc[curr_idx:].style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == curr_idx else ['']*len(r), axis=1))
