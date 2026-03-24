import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 스타일 ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    .unified-title { font-size: 26px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 15px; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 카드 디자인 최적화 (높이 축소 및 고정) */
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
    [data-testid="stTable"] { font-size: 14px !important; }
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 준비 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
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

# 시간표 데이터
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
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"],
]
df_rt = pd.DataFrame(time_data, columns=["From", "To", "조장", "성의", "의생A", "의생B"])

def get_now_row(h, m):
    if h == 1 and m < 40: return df_rt[df_rt['From'] == "23:00"].iloc[0]
    if h == 1 and m >= 40: return df_rt[df_rt['From'] == "01:40"].iloc[0]
    for _, row in df_rt.iterrows():
        try:
            sh, eh = int(row['From'].split(':')[0]), int(row['To'].split(':')[0])
            if eh == 0: eh = 24
            if sh <= h < eh: return row
        except: continue
    return df_rt.iloc[-1]

curr = get_now_row(now.hour, now.minute)

# --- [3] 화면 출력 (하이라이트 카드 상단 고정) ---
st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

# ⭐️ 최상단 하이라이트 카드 영역
if not is_work:
    st.warning("📅 오늘은 C조 휴무일입니다.")
    j, s, a, b = "황재업", "김태언", "이태원", "이정석"

st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="worker-name">{j}</div><div class="status-val">{curr['조장']}</div></div>
        <div class="status-card"><div class="worker-name">{s}</div><div class="status-val">{curr['성의']}</div></div>
        <div class="status-card"><div class="worker-name">{a}</div><div class="status-val">{curr['의생A']}</div></div>
        <div class="status-card"><div class="worker-name">{b}</div><div class="status-val">{curr['의생B']}</div></div>
    </div>
""", unsafe_allow_html=True)

# 하단 전체 시간표 (현재 시간 행 강조)
st.table(df_rt.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.equals(curr) and is_work else ['']*len(r), axis=1))
