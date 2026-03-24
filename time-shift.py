import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 ---
st.set_page_config(page_title="C조 근무 시스템", layout="wide")

# --- [2] 07시 기준 날짜 및 근무자 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
# 07시 이전이면 어제 날짜로 고정
target_date = (now - timedelta(days=1)).date() if now.hour < 7 else now.date()
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers(d):
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci = (sc // 2) % 3
        if ci == 0: return "재업", "태원", "정석", "태언"
        elif ci == 1: return "재업", "정석", "태언", "태원"
        else: return "재업", "태언", "태원", "정석"
    return "재업", "태원", "정석", "태언"

w1, w2, w3, w4 = get_workers(target_date)

# --- [3] 데이터프레임 구성 (스크린샷의 2단 헤더) ---
# 성의회관과 의학연구원으로 명확히 구분된 구조
header = pd.MultiIndex.from_tuples([
    ('시간', ''), 
    ('성의회관', w1), ('성의회관', w2), 
    ('의학연구원', w3), ('의학연구원', w4)
])

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
df = pd.DataFrame(time_data, columns=header)

# --- [4] 현재 시간 인덱스 계산 ---
h = now.hour
val = h if h >= 7 else h + 24
curr_idx = 0
for i, r in enumerate(time_data):
    sh = int(r[0].split(':')[0])
    if sh < 7: sh += 24
    if sh <= val: curr_idx = i

# --- [5] 화면 출력 ---
st.title("C조 실시간 근무 현황")
st.write(f"기준 날짜: {target_date} ({now.strftime('%H:%M')})")

if st.button("📋 전체 시간표 보기"):
    st.table(df)

st.markdown("### 🔽 현재 근무")
# 스크린샷 00:03분 버전처럼 현재 시간대만 깔끔하게 강조된 표
st.table(df.iloc[[curr_idx]].style.set_properties(**{'background-color': '#FFE5E5', 'font-weight': 'bold'}))

st.markdown(f"### 🗓 내일 근무 예정 ({ (target_date + timedelta(days=1)).strftime('%m/%d') })")
# 내일 근무 첫 시간대 미리보기
st.table(df.iloc[:2])
