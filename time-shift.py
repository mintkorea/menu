
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 16px !important; text-align: center; margin-bottom: 15px; color: #555; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 6px 0; text-align: center; background: #F8F9FA; min-height: 65px; }
    .worker-name { font-size: 15px !important; font-weight: 700; color: #444; }
    .status-val { font-size: 18px; font-weight: 900; color: #C04B41; }
    .b-header { display: flex; border: 1px solid #dee2e6; border-bottom: none; font-weight: bold; text-align: center; font-size: 14px; }
    .b-section { width: 33.33%; padding: 7px 0; border-right: 1px solid #dee2e6; }
    [data-testid="stTable"] table { width: 100% !important; }
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직: 날짜 처리 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# 🔥 중요: 새벽 07시 이전까지는 '전날' 근무로 취급
if now.hour < 7:
    target_date = (now - timedelta(days=1)).date()
    display_msg = f"{target_date.strftime('%m/%d')} 야간 근무 중 (익일 07시 종료)"
else:
    target_date = now.date()
    display_msg = f"{target_date.strftime('%m/%d')} 주간 근무 중"

PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(d):
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이정석")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

jojang, seonghui, uisanA, uisanB = get_workers_by_date(target_date)
# 패턴 예외 처리용 (필요시)
if jojang is None: jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

# --- [3] 데이터셋 ---
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
df_rt = pd.DataFrame(time_data, columns=["From", "To", jojang, seonghui, uisanA, uisanB])

def get_rt_idx(h, m):
    # 자정 이후(00~07시) 처리 로직
    actual_h = h if h >= 7 else h + 24
    for i, row in df_rt.iterrows():
        sh = int(row['From'].split(':')[0])
        sh = sh if sh >= 7 else sh + 24
        eh = int(row['To'].split(':')[0])
        eh = eh if eh >= 7 else eh + 24
        if row['From'] == "23:00" and row['To'] == "01:40":
            if 23 <= actual_h < 25.6: return 16
        if row['From'] == "01:40" and row['To'] == "02:00":
            if 25.6 <= (h + m/60 + 24 if h < 7 else h + m/60) < 26: return 17
        if sh <= actual_h < eh: return i
    return 20

curr_idx = get_rt_idx(now.hour, now.minute)
curr_row = df_rt.iloc[curr_idx]

# --- [4] 화면 출력 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{display_msg} ({now.strftime("%H:%M:%S")})</div>', unsafe_allow_html=True)

    # 상단 요약 카드
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr_row[jojang]}</div></div>
            <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr_row[seonghui]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr_row[uisanA]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr_row[uisanB]}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # 건물 헤더
    st.markdown(f"""<div class="b-header"><div class="b-section">구분 (시간)</div><div class="b-section" style="background:#FFF2CC;">성의회관</div><div class="b-section" style="background:#D9EAD3;">의산연</div></div>""", unsafe_allow_html=True)
    
    # 1. 당일 전체 시간표 보기 버튼 (Expander)
    with st.expander("📋 당일 전체 시간표 확인하기", expanded=False):
        st.table(df_rt.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == curr_idx else ['']*len(r), axis=1))

    # 2. 실시간 표 (현재 이후 스케줄만 간략히 표시)
    st.markdown("**▼ 현재 근무 및 다음 스케줄**")
    st.table(df_rt.iloc[curr_idx:curr_idx+5].style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == curr_idx else ['']*len(r), axis=1))

with tab2:
    # [기본 편성표 로직 유지]
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    # ... (생략된 기존 편성표 코드)
