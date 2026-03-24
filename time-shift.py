import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- [1] 설정 및 스타일 ---
st.set_page_config(page_title="C조 실시간 근무 현황", layout="wide")

# CSS: 타이틀 폰트 30% 축소, 상단 여백 1cm(약 38px) 확보
st.markdown("""
    <style>
    .block-container { 
        padding-top: 38px !important; 
    }
    .main-title {
        font-size: 1.75rem !important; /* 기존 대비 약 30% 축소 */
        font-weight: 800;
        margin-bottom: 20px;
        text-align: center;
    }
    .status-container { 
        display: grid; 
        grid-template-columns: repeat(2, 1fr); 
        gap: 10px; 
        margin-bottom: 20px; 
    }
    .status-card { 
        border: 2px solid #2E4077; 
        border-radius: 10px; 
        padding: 12px; 
        text-align: center; 
        background: white; 
    }
    .name-label { font-size: 14px; color: #666; margin-bottom: 5px; border-bottom: 1px solid #eee; }
    .loc-label { font-size: 20px; font-weight: 800; color: #C04B41; }
    
    /* 인덱스 열 제거 */
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 한국 표준시(KST) 및 시간 설정 ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
now_time_str = now_kst.strftime("%H:%M")
now_hour = now_kst.hour

# --- [3] 근무 데이터 (오타 수정 및 1시간 단위 분할) ---
# 성희 -> 성의 / 의산 -> 의생(의생명산업연구원)으로 교정
time_data = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"],
    ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"],
    ["10:00", "11:00", "휴게/안", "안/휴", "로비", "순찰/휴"],
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"],
    ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "휴/순", "로비"],
    ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"],
    ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"],
    ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"],
    ["18:00", "19:00", "안내실", "석식", "로비", "석식"],
    ["19:00", "20:00", "안내실", "안내실", "석식", "로비"],
    ["20:00", "21:00", "석식/안", "안내실", "로비", "휴게"],
    ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"],
    ["22:00", "23:00", "순찰/안", "안/순", "순찰/로", "로비/휴"],
    ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"],
    ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"],
    ["01:00", "02:00", "안내실", "휴게", "휴게", "로비"],
    ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"],
    ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"],
    ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"],
    ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"],
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"],
]
df_time = pd.DataFrame(time_data, columns=["From", "To", "조장", "성의", "의생A", "의생B"])

# --- [4] 실시간 위치 추출 ---
curr_row = df_time[df_time['From'].apply(lambda x: int(x.split(':')[0])) == now_hour].iloc[0]

# --- [5] 화면 표시 ---
st.markdown(f'<div class="main-title">🕒 실시간 근무 현황 ({now_time_str})</div>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="name-label">조장 (황재업)</div><div class="loc-label">{curr_row['조장']}</div></div>
        <div class="status-card"><div class="name-label">성의회관</div><div class="loc-label">{curr_row['성의']}</div></div>
        <div class="status-card"><div class="name-label">의생연 A</div><div class="loc-label">{curr_row['의생A']}</div></div>
        <div class="status-card"><div class="name-label">의생연 B</div><div class="loc-label">{curr_row['의생B']}</div></div>
    </div>
""", unsafe_allow_html=True)

# --- [6] 테이블 표시 ---
def styling(row):
    if int(row['From'].split(':')[0]) == now_hour:
        return ['background-color: #FFE5E5; font-weight: bold'] * len(row)
    return [''] * len(row)

st.table(df_time.style.apply(styling, axis=1))
