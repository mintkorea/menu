import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- [1] 설정 및 CSS (셀 높이 축소 및 중앙 정렬 강화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    
    /* 타이틀 및 날짜 스타일 */
    .title-area { text-align: center; margin-bottom: 10px; }
    .main-title { font-size: 24px !important; font-weight: 800; margin-bottom: 5px; }
    .sub-date { font-size: 14px; color: #666; margin-bottom: 15px; }

    /* 탭 메뉴 스타일 (링크 느낌) */
    .tab-menu { display: flex; justify-content: center; gap: 20px; border-bottom: 2px solid #ddd; padding-bottom: 5px; margin-bottom: 20px; }
    .tab-item { cursor: pointer; font-size: 14px; font-weight: bold; color: #666; text-decoration: none; }
    .tab-active { color: #C04B41; border-bottom: 3px solid #C04B41; padding-bottom: 5px; }

    /* 카드 디자인 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 6px 0; text-align: center; background: #fff; }
    .card-name { font-size: 13px; font-weight: 600; color: #666; }
    .card-status { font-size: 17px; font-weight: 800; color: #C04B41; }

    /* 건물명 헤더 (균등 33.3%) */
    .b-header { display: flex; border: 1px solid #dee2e6; border-bottom: none; font-weight: bold; text-align: center; font-size: 13px; }
    .b-section { width: 33.33%; padding: 8px 0; border-right: 1px solid #dee2e6; }
    .b-section:last-child { border-right: none; }

    /* 표 셀 높이 축소 및 균등 배분 */
    [data-testid="stTable"] { width: 100% !important; table-layout: fixed !important; }
    [data-testid="stTable"] th, [data-testid="stTable"] td { 
        width: 16.66% !important; 
        text-align: center !important; 
        vertical-align: middle !important;
        padding: 4px 0 !important; /* 셸 높이 대폭 축소 */
        font-size: 13px !important;
        line-height: 1.1 !important;
    }
    
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 데이터 및 시간 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
date_str = now.strftime("%Y년 %m월 %d일 %H:%M:%S")

names = ["황재업", "이태원", "이정석", "김태언"]

# 근무 데이터 (기존 동일)
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

# 1. 탭 메뉴 (링크 부분 복구)
st.markdown(f"""
    <div class="tab-menu">
        <div class="tab-item tab-active">🕒 실시간 근무 현황</div>
        <div class="tab-item">📅 월간 근무 편성표</div>
    </div>
""", unsafe_allow_html=True)

# 2. 타이틀 및 실시간 시간 (누락 부분 복구)
st.markdown(f"""
    <div class="title-area">
        <div class="main-title">🕒 C조 실시간 근무 현황</div>
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

# 4. 건물명 헤더
st.markdown(f"""
    <div class="b-header">
        <div class="b-section" style="background:#fff;">구분 (시간)</div>
        <div class="b-section" style="background:#FFF2CC;">성의회관</div>
        <div class="b-section" style="background:#D9EAD3;">의산연</div>
    </div>
""", unsafe_allow_html=True)

# 5. 균등 표 (높이 축소 버전)
st.table(df_full.iloc[idx:].style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == idx else ['']*len(r), axis=1))
