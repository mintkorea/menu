import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 스타일 ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2.5rem !important; }
    .unified-title { font-size: 26px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 15px; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 카드 디자인: 높이 최소화 */
    .status-container { 
        display: grid; grid-template-columns: repeat(2, 1fr); 
        gap: 8px; margin-bottom: 20px; 
    }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 10px; 
        padding: 10px 0; text-align: center; background: #F8F9FA;
        min-height: 65px; display: flex; flex-direction: column; justify-content: center;
    }
    .worker-name { font-size: 16px !important; font-weight: 700; color: #444; margin-bottom: 2px; }
    .status-val { font-size: 19px; font-weight: 800; color: #C04B41; }
    
    /* 테이블 가독성 */
    [data-testid="stTable"] { font-size: 15px !important; }
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 데이터 및 시간 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
# 테스트용 시각 설정 (필요 시 주석 해제하여 확인 가능)
# now = now.replace(hour=22, minute=0) 

PATTERN_START = datetime(2026, 3, 9).date()

def get_workers(d):
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

j, s, a, b = get_workers(now.date())
is_work = j is not None

# 전체 시간표 데이터
time_data = [
    ["07:00", "08:00"], ["08:00", "09:00"], ["09:00", "10:00"], ["10:00", "11:00"],
    ["11:00", "12:00"], ["12:00", "13:00"], ["13:00", "14:00"], ["14:00", "15:00"],
    ["15:00", "16:00"], ["16:00", "17:00"], ["17:00", "18:00"], ["18:00", "19:00"],
    ["19:00", "20:00"], ["20:00", "21:00"], ["21:00", "22:00"], ["22:00", "23:00"],
    ["23:00", "01:40"], ["01:40", "02:00"], ["02:00", "05:00"], ["05:00", "06:00"], ["06:00", "07:00"]
]
# 상세 위치 데이터 매핑
details = [
    ["안내실", "로비", "로비", "휴게"], ["안내실", "휴게", "휴게", "로비"],
    ["순찰", "안내실", "휴게", "로비"], ["휴게", "안내실", "로비", "순찰"],
    ["안내실", "중식", "로비", "중식"], ["중식", "안내실", "중식", "로비"],
    ["안내실", "휴게", "순찰", "로비"], ["순찰", "안내실", "로비", "휴게"],
    ["안내실", "휴게", "로비", "휴게"], ["휴게", "안내실", "휴게", "로비"],
    ["안내실", "휴게", "휴게", "로비"], ["안내실", "석식", "로비", "석식"],
    ["안내실", "안내실", "석식", "로비"], ["석식", "안내실", "로비", "휴게"],
    ["안내실", "순찰", "로비", "휴게"], ["순찰", "안내실", "순찰", "로비"],
    ["안내실", "휴게", "휴게", "로비"], ["안내실", "안내실", "로비", "로비"],
    ["휴게", "안내실", "로비", "휴게"], ["안내실", "순찰", "로비", "순찰"], ["안내실", "안내실", "휴게", "로비"]
]

df_full = pd.DataFrame([t + d for t, d in zip(time_data, details)], 
                       columns=["From", "To", "조장", "성의", "의생A", "의생B"])

# --- [3] 현재 행 찾기 및 데이터 재정렬 ---
def get_current_index(h, m):
    if h == 1 and m < 40: return 16 # 23:00 ~ 01:40 행
    if h == 1 and m >= 40: return 17 # 01:40 ~ 02:00 행
    for i, row in df_full.iterrows():
        try:
            sh, eh = int(row['From'].split(':')[0]), int(row['To'].split(':')[0])
            if eh == 0 or eh < sh: eh = 24 # 자정 넘어가면 24시로 처리
            if sh <= h < eh: return i
        except: continue
    return 20

curr_idx = get_current_index(now.hour, now.minute)
curr_row = df_full.iloc[curr_idx]

# ⭐️ 핵심 로직: 현재 인덱스부터 끝까지만 필터링하여 상단에 배치
df_display = df_full.iloc[curr_idx:].copy()

# --- [4] 화면 출력 ---
st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

if not is_work:
    st.warning("📅 오늘은 C조 휴무일입니다.")
    j, s, a, b = "황재업", "김태언", "이태원", "이정석"

# 최상단 하이라이트 카드
st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="worker-name">{j}</div><div class="status-val">{curr_row['조장']}</div></div>
        <div class="status-card"><div class="worker-name">{s}</div><div class="status-val">{curr_row['성의']}</div></div>
        <div class="status-card"><div class="worker-name">{a}</div><div class="status-val">{curr_row['의생A']}</div></div>
        <div class="status-card"><div class="worker-name">{b}</div><div class="status-val">{curr_row['의생B']}</div></div>
    </div>
""", unsafe_allow_html=True)

# 현재 시각 이후의 표만 출력 (첫 줄이 항상 현재 하이라이트 행)
st.table(df_display.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == curr_idx and is_work else ['']*len(r), axis=1))
