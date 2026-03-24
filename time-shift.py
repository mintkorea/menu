import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- [1] 설정 및 CSS (표 폰트 축소 및 줄간격 최적화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    /* 상단 여백: 기존(2.5)과 직전(3.5)의 중간인 3.0으로 조정 */
    .block-container { padding-top: 3.0rem !important; } 
    
    /* 링크 메뉴 스타일 */
    .tab-menu { display: flex; justify-content: center; gap: 20px; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .tab-item { font-size: 15px; font-weight: bold; color: #888; text-decoration: none; }
    .tab-active { color: #C04B41; border-bottom: 3px solid #C04B41; padding-bottom: 10px; }

    /* 타이틀 및 시간 (+2pt 유지) */
    .title-area { text-align: center; margin-bottom: 15px; }
    .main-title { font-size: 25px !important; font-weight: 800; margin-bottom: 5px; }
    .sub-date { font-size: 17.5px !important; color: #555; font-weight: 500; }

    /* 카드 부분 (슬림 높이) */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 5px 0; text-align: center; background: #fff; }
    .card-name { font-size: 16px !important; font-weight: 700; color: #555; }
    .card-status { font-size: 18px !important; font-weight: 900; color: #C04B41; }

    /* 표 내부 폰트 및 줄간격 (성명 폰트 축소) */
    [data-testid="stTable"] td { 
        padding: 2px 0 !important; 
        font-size: 12px !important; /* ⭐️ 표 내 성명 폰트를 12px로 줄임 */
        line-height: 1.0 !important;
        height: 28px !important;
        text-align: center !important; 
    }
    .b-header { display: flex; border: 1px solid #dee2e6; border-bottom: none; font-weight: bold; text-align: center; font-size: 13px; }
    .b-section { width: 33.33%; padding: 6px 0; border-right: 1px solid #dee2e6; }
    
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 데이터 및 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
date_str = now.strftime("%Y-%m-%d %H:%M:%S")

names = ["황재업", "이태원", "이정석", "김태언"]
time_raw = [["07:00", "08:00"], ["08:00", "09:00"], ["09:00", "10:00"], ["10:00", "11:00"], ["11:00", "12:00"], ["12:00", "13:00"], ["13:00", "14:00"], ["14:00", "15:00"], ["15:00", "16:00"], ["16:00", "17:00"], ["17:00", "18:00"], ["18:00", "19:00"], ["19:00", "20:00"], ["20:00", "21:00"], ["21:00", "22:00"], ["22:00", "23:00"], ["23:00", "01:40"], ["01:40", "02:00"], ["02:00", "05:00"], ["05:00", "06:00"], ["06:00", "07:00"]]
loc_raw = [["안내실", "로비", "로비", "휴게"], ["안내실", "휴게", "휴게", "로비"], ["순찰", "안내실", "휴게", "로비"], ["휴게", "안내실", "로비", "순찰"], ["안내실", "중식", "로비", "중식"], ["중식", "안내실", "중식", "로비"], ["안내실", "휴게", "순찰", "로비"], ["순찰", "안내실", "로비", "휴게"], ["안내실", "휴게", "로비", "휴게"], ["휴게", "안내실", "휴게", "로비"], ["안내실", "휴게", "휴게", "로비"], ["안내실", "석식", "로비", "석식"], ["안내실", "안내실", "석식", "로비"], ["석식", "안내실", "로비", "휴게"], ["안내실", "순찰", "로비", "휴게"], ["순찰", "안내실", "순찰", "로비"], ["안내실", "휴게", "휴게", "로비"], ["안내실", "안내실", "로비", "로비"], ["휴게", "안내실", "로비", "휴게"], ["안내실", "순찰", "로비", "순찰"], ["안내실", "안내실", "휴게", "로비"]]

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

# --- [3] 화면 출력 ---

# 1. 상단 링크 메뉴 (⭐️ 기존 링크 주소로 복구됨)
st.markdown(f"""
    <div class="tab-menu">
        <a href="https://mintkoreatimeshift.streamlit.app" class="tab-item tab-active">🕒 실시간 근무 현황</a>
        <a href="https://mintkoreatimeshift.streamlit.app" class="tab-item">📅 월간 근무 편성표</a>
    </div>
""", unsafe_allow_html=True)

# 2. 타이틀 및 확대된 시간
st.markdown(f"""
    <div class="title-area">
        <div class="main-title">C조 실시간 근무 현황</div>
        <div class="sub-date">{date_str}</div>
    </div>
""", unsafe_allow_html=True)

# 3. 요약 카드
st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="card-name">{names[0]}</div><div class="card-status">{curr_row[names[0]]}</div></div>
        <div class="status-card"><div class="card-name">{names[1]}</div><div class="card-status">{curr_row[names[1]]}</div></div>
        <div class="status-card"><div class="card-name">{names[2]}</div><div class="card-status">{curr_row[names[2]]}</div></div>
        <div class="status-card"><div class="card-name">{names[3]}</div><div class="card-status">{curr_row[names[3]]}</div></div>
    </div>
""", unsafe_allow_html=True)

# 4. 건물 헤더 및 표
st.markdown(f"""
    <div class="b-header">
        <div class="b-section" style="background:#fff;">구분 (시간)</div>
        <div class="b-section" style="background:#FFF2CC;">성의회관</div>
        <div class="b-section" style="background:#D9EAD3;">의산연</div>
    </div>
""", unsafe_allow_html=True)

st.table(df_full.iloc[idx:].style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == idx else ['']*len(r), axis=1))
