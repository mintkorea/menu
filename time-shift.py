import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- [1] CSS: 모든 열 1/6 균등 배분 및 중앙 정렬 ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; }
    
    /* 1. 타이틀 스타일 */
    .main-title { font-size: 26px !important; font-weight: 800; text-align: center; margin-bottom: 15px; }

    /* 2. 카드 디자인 (성함/상태) */
    .status-container { 
        display: grid; grid-template-columns: repeat(2, 1fr); 
        gap: 10px; margin-bottom: 20px; 
    }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 12px; 
        padding: 10px 0; text-align: center; background: #fff;
    }
    .card-name { font-size: 14px; font-weight: 600; color: #666; }
    .card-status { font-size: 19px; font-weight: 800; color: #C04B41; }

    /* 3. 건물명 헤더 (균등 비율 33.3%씩 분할) */
    .b-header {
        display: flex; margin-top: 10px; border: 1px solid #dee2e6; border-bottom: none;
        font-weight: bold; text-align: center; font-size: 14px;
    }
    .b-section { width: 33.33%; padding: 10px 0; border-right: 1px solid #dee2e6; }
    .b-section:last-child { border-right: none; }

    /* 4. 표 모든 셸 너비 균등 고정 (100% / 6열 = 16.66%) */
    [data-testid="stTable"] { width: 100% !important; table-layout: fixed !important; }
    [data-testid="stTable"] th, [data-testid="stTable"] td { 
        width: 16.66% !important; 
        text-align: center !important; 
        vertical-align: middle !important;
        padding: 10px 0 !important;
        word-break: keep-all !important; /* 이름 안 잘리게 */
    }

    /* 표 헤더 인덱스 숨기기 */
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 데이터 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
names = ["황재업", "이태원", "이정석", "김태언"]

time_raw = [
    ["07:00", "08:00"], ["08:00", "09:00"], ["09:00", "10:00"], ["10:00", "11:00"],
    ["11:00", "12:00"], ["12:00", "13:00"], ["13:00", "14:00"], ["14:00", "15:00"],
    ["15:00", "16:00"], ["16:00", "17:00"], ["17:00", "18:00"], ["18:00", "19:00"],
    ["19:00", "20:00"], ["20:00", "21:00"], ["21:00", "22:00"], ["22:00", "23:00"],
    ["23:00", "01:40"], ["01:40", "02:00"], ["02:00", "05:00"], ["05:00", "06:00"], ["06:00", "07:00"]
]
loc_raw = [
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

df_full = pd.DataFrame([t + l for t, l in zip(time_raw, loc_raw)], columns=["From", "To"] + names)

def get_curr_idx(h, m):
    if h == 1 and m < 40: return 16
    if h == 1 and m >= 40: return 17
    for i, row in df_full.iterrows():
        sh, eh = int(row['From'].split(':')[0]), int(row['To'].split(':')[0])
        if eh == 0 or eh < sh: eh = 24
        if sh <= h < eh: return i
    return 0

idx = get_curr_idx(now.hour, now.minute)
curr_row = df_full.iloc[idx]
df_display = df_full.iloc[idx:].copy()

# --- [3] 화면 출력 ---
st.markdown('<div class="main-title">🕒 C조 실시간 근무 현황</div>', unsafe_allow_html=True)

# 1. 요약 카드 (중앙 정렬 확인용)
st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="card-name">{names[0]}</div><div class="card-status">{curr_row[names[0]]}</div></div>
        <div class="status-card"><div class="card-name">{names[1]}</div><div class="card-status">{curr_row[names[1]]}</div></div>
        <div class="status-card"><div class="card-name">{names[2]}</div><div class="card-status">{curr_row[names[2]]}</div></div>
        <div class="status-card"><div class="card-name">{names[3]}</div><div class="card-status">{curr_row[names[3]]}</div></div>
    </div>
""", unsafe_allow_html=True)

# 2. 균등 건물명 헤더 (33.3%씩)
st.markdown(f"""
    <div class="b-header">
        <div class="b-section" style="background:#fff;">구분 (시간)</div>
        <div class="b-section" style="background:#FFF2CC;">성의회관</div>
        <div class="b-section" style="background:#D9EAD3;">의산연</div>
    </div>
""", unsafe_allow_html=True)

# 3. 균등 표 (모든 열 16.6% 및 중앙 정렬)
st.table(df_display.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == idx else ['']*len(r), axis=1))
