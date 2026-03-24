import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- [1] 설정 및 스타일 ---
st.set_page_config(page_title="성의교정 근무 현황", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 38px !important; }
    
    /* 타이틀 두 줄 디자인 */
    .title-main { font-size: 1.8rem !important; font-weight: 800; text-align: center; margin-bottom: 5px; color: #2E4077; }
    .title-sub { font-size: 1.1rem !important; font-weight: 400; text-align: center; margin-bottom: 25px; color: #666; }
    
    /* 카드 크기 축소 및 내부 텍스트 최적화 */
    .status-container { 
        display: grid; 
        grid-template-columns: repeat(2, 1fr); 
        gap: 8px; 
        margin-bottom: 20px; 
    }
    .status-card { 
        border: 2px solid #2E4077; 
        border-radius: 12px; 
        padding: 10px 5px; 
        text-align: center; 
        background: #F8F9FA; 
    }
    .name-label { 
        font-size: 16px !important; /* 이름 크기 키움 */
        font-weight: 700; 
        color: #333; 
        margin-bottom: 5px; 
    }
    .loc-label { 
        font-size: 18px; 
        font-weight: 800; 
        color: #C04B41; 
    }
    
    /* 휴무일 알림 스타일 */
    .off-day-banner {
        background-color: #FFF3CD;
        color: #856404;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
        border: 1px solid #FFEEBA;
    }

    /* 테이블 인덱스 제거 */
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 시간 및 날짜 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
date_str = now.strftime("%Y년 %m월 %d일")
time_str = now.strftime("%H:%M:%S")
now_hour = now.hour
now_minute = now.minute

# 휴무일 판별 (예: C조 기준 3월은 3의 배수일 근무, 그 외 휴무)
is_work_day = (now.day % 3 == 0) 

# --- [3] 근무 데이터 (1시간 단위 & 01:40 교대) ---
time_data = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"],
    ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "순찰", "안내실", "휴게", "로비"],
    ["10:00", "11:00", "휴게", "안내실", "로비", "순찰"],
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"],
    ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"],
    ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"],
    ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"],
    ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"],
    ["18:00", "19:00", "안내실", "석식", "로비", "석식"],
    ["19:00", "20:00", "안내실", "안내실", "석식", "로비"],
    ["20:00", "21:00", "석식", "안내실", "로비", "휴게"],
    ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"],
    ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"],
    ["23:00", "01:40", "안내실", "휴게", "휴게", "로비"],
    ["01:40", "02:00", "안내실", "안내실", "로비", "로비"],
    ["02:00", "05:00", "휴게", "안내실", "로비", "휴게"],
    ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"],
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"],
]
df_time = pd.DataFrame(time_data, columns=["From", "To", "조장", "성의", "의생A", "의생B"])

# --- [4] 실시간 위치 추출 함수 ---
def get_current_row(h, m):
    if h == 1 and m < 40: return df_time[df_time['From'] == "23:00"].iloc[0]
    if h == 1 and m >= 40: return df_time[df_time['From'] == "01:40"].iloc[0]
    for i, row in df_time.iterrows():
        try:
            start_h = int(row['From'].split(':')[0]); end_h = int(row['To'].split(':')[0])
            if end_h == 0: end_h = 24
            if start_h <= h < end_h: return row
        except: continue
    return df_time.iloc[-1]

curr = get_current_row(now_hour, now_minute)

# --- [5] 화면 표시 ---
# 타이틀 두 줄 및 날짜/시간
st.markdown(f'<div class="title-main">C조 당직 근무 현황</div>', unsafe_allow_html=True)
st.markdown(f'<div class="title-sub">{date_str} {time_str}</div>', unsafe_allow_html=True)

# 휴무일 알림 (휴무일일 때만 표출)
if not is_work_day:
    st.markdown('<div class="off-day-banner">📅 오늘은 C조 휴무일입니다. (비상연락망을 확인하세요)</div>', unsafe_allow_html=True)

# 실시간 현황 카드 (휴무일이라도 현재 시간 기준 위치 표출)
st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="name-label">조장 (황재업)</div><div class="loc-label">{curr['조장']}</div></div>
        <div class="status-card"><div class="name-label">성의회관</div><div class="loc-label">{curr['성의']}</div></div>
        <div class="status-card"><div class="name-label">의생연 A</div><div class="loc-label">{curr['의생A']}</div></div>
        <div class="status-card"><div class="name-label">의생연 B</div><div class="loc-label">{curr['의생B']}</div></div>
    </div>
""", unsafe_allow_html=True)

# 근무 시간표는 항상 표출
st.subheader("📅 전체 근무 시간표")
def styling(row):
    if row.equals(curr) and is_work_day:
        return ['background-color: #FFE5E5; font-weight: bold'] * len(row)
    return [''] * len(row)

st.table(df_time.style.apply(styling, axis=1))
