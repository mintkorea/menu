import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (사용자 요청값 유지) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 14px !important; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 요약 카드 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 10px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 10px; padding: 8px 0; 
        text-align: center; background: #F8F9FA;
    }
    .worker-name { font-size: 14px; font-weight: 700; color: #444; }
    .status-val { font-size: 18px; font-weight: 900; color: #C04B41; }
    
    /* 건물 헤더 확대 (14px) */
    .b-header { 
        display: flex; border: 1px solid #dee2e6; border-bottom: none; 
        font-weight: bold; text-align: center; font-size: 14px; background: #eee;
    }
    .b-section { width: 33.33%; padding: 7px 0; border-right: 1px solid #dee2e6; }
    .b-section:last-child { border-right: none; }

    /* 표 중앙 정렬 및 폰트 */
    .stTable { display: flex; justify-content: center; }
    .stTable table { width: 100% !important; font-size: 11px !important; text-align: center; }
    
    /* 버튼 스타일 */
    .stButton > button { width: 100%; height: 3em; border-radius: 8px; font-weight: bold; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 (07시 기준 날짜 및 패턴) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
# 07시 이전이면 '어제' 날짜의 근무로 간주
target_date = (now - timedelta(days=1)).date() if now.hour < 7 else now.date()
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers(d):
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return ["황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")]
        elif ci == 1: return ["황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")]
        else: return ["황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")]
    return ["황재업", "김태언", "이태원", "이정석"] # 기본값

names = get_workers(target_date)
j, s, a, b = names

# 데이터 정의
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
df_all = pd.DataFrame(time_data, columns=["From", "To", "조장", "성희", "의산A", "의산B"])

def get_curr_idx():
    h, m = now.hour, now.minute
    val = h if h >= 7 else h + 24
    if val == 25 and m < 40: return 16 # 01:00 ~ 01:40 처리
    for i, r in enumerate(time_data):
        sh = int(r[0].split(':')[0]); sh = sh if sh >= 7 else sh + 24
        eh = int(r[1].split(':')[0]); eh = eh if eh >= 7 else eh + 24
        if sh <= val < eh: return i
    return 20

curr_idx = get_curr_idx()

# --- [3] 화면 출력 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{target_date.strftime("%m/%d")} ({now.strftime("%H:%M")})</div>', unsafe_allow_html=True)

    # 1. 요약 카드 (이름 이니셜 처리)
    c_row = time_data[curr_idx]
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{j[1:]} (조장)</div><div class="status-val">{c_row[2]}</div></div>
            <div class="status-card"><div class="worker-name">{s[1:]} (성희)</div><div class="status-val">{c_row[3]}</div></div>
            <div class="status-card"><div class="worker-name">{a[1:]} (의산A)</div><div class="status-val">{c_row[4]}</div></div>
            <div class="status-card"><div class="worker-name">{b[1:]} (의산B)</div><div class="status-val">{c_row[5]}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # 2. 전체 시간표 버튼 (Dialog 활용)
    @st.dialog("📅 오늘 전체 시간표")
    def show_full():
        st.markdown(f'<div class="b-header"><div class="b-section">시간</div><div class="b-section" style="background:#FFF2CC;">성의회관</div><div class="b-section" style="background:#D9EAD3;">의산연</div></div>', unsafe_allow_html=True)
        st.table(df_all.style.apply(lambda r: ['background-color:#FFE5E5; font-weight:bold']*6 if r.name == curr_idx else ['']*6, axis=1))

    if st.button("📋 오늘 전체 시간표 크게 보기"):
        show_full()

    # 3. 현재 근무 상세 (건물 헤더 포함)
    st.markdown("**▼ 현재 근무 상세**")
    st.markdown(f'<div class="b-header"><div class="b-section">시간</div><div class="b-section" style="background:#FFF2CC;">성의회관</div><div class="b-section" style="background:#D9EAD3;">의산연</div></div>', unsafe_allow_html=True)
    st.table(df_all.iloc[curr_idx:curr_idx+1])

with tab2:
    # 기존 편성표 로직 유지 (사용자 코드 반영)
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    # ... (생략: 기존 tab2 코드와 동일하게 작동)
