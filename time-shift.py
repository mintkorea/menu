import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (모바일 최적화 강화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 16px !important; text-align: center; margin-bottom: 15px; color: #555; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 10px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 10px; padding: 10px 0; 
        text-align: center; background: #F8F9FA; min-height: 70px;
    }
    .worker-name { font-size: 14px !important; font-weight: 700; color: #666; margin-bottom: 3px; }
    .status-val { font-size: 20px; font-weight: 900; color: #C04B41; }
    
    /* 표 헤더 디자인 */
    .b-header { 
        display: flex; border: 1px solid #dee2e6; border-bottom: none; 
        font-weight: bold; text-align: center; font-size: 14px; 
    }
    .b-section { width: 33.33%; padding: 8px 0; border-right: 1px solid #dee2e6; }
    .b-section:last-child { border-right: none; }

    /* 표 가독성 및 모바일 대응 */
    [data-testid="stTable"] table { width: 100% !important; border-collapse: collapse; }
    [data-testid="stTable"] thead tr th { font-size: 11px !important; padding: 6px 2px !important; text-align: center !important; background: #f1f3f5 !important; }
    [data-testid="stTable"] td { font-size: 12px !important; padding: 8px 2px !important; text-align: center !important; border: 1px solid #eee !important; }
    thead tr th:first-child, tbody th { display:none; }
    
    /* 강조 행 스타일 */
    .highlight-row { background-color: #FFE5E5 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 (근무일 기준 처리) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

if now.hour < 7:
    work_date = (now - timedelta(days=1)).date()
else:
    work_date = now.date()

PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return "황재업", "김태언", "이태원", "이정석"

jojang, seonghui, uisanA, uisanB = get_workers_by_date(work_date)

# --- [3] 데이터 구성 ---
time_slots = [
    ["07:00", "08:00"], ["08:00", "09:00"], ["09:00", "10:00"], ["10:00", "11:00"],
    ["11:00", "12:00"], ["12:00", "13:00"], ["13:00", "14:00"], ["14:00", "15:00"],
    ["15:00", "16:00"], ["16:00", "17:00"], ["17:00", "18:00"], ["18:00", "19:00"],
    ["19:00", "20:00"], ["20:00", "21:00"], ["21:00", "22:00"], ["22:00", "23:00"],
    ["23:00", "01:40"], ["01:40", "02:00"], ["02:00", "05:00"], ["05:00", "06:00"],
    ["06:00", "07:00"]
]
task_values = [
    ["안내실", "로비", "로비", "휴게"], ["안내실", "휴게", "휴게", "로비"],
    ["순찰", "안내실", "휴게", "로비"], ["휴게", "안내실", "로비", "순찰"],
    ["안내실", "중식", "로비", "중식"], ["중식", "안내실", "중식", "로비"],
    ["안내실", "휴게", "순찰", "로비"], ["순찰", "안내실", "로비", "휴게"],
    ["안내실", "휴게", "로비", "휴게"], ["휴게", "안내실", "휴게", "로비"],
    ["안내실", "휴게", "휴게", "로비"], ["안내실", "석식", "로비", "석식"],
    ["안내실", "안내실", "석식", "로비"], ["석식", "안내실", "로비", "휴게"],
    ["안내실", "순찰", "로비", "휴게"], ["순찰", "안내실", "순찰", "로비"],
    ["안내실", "휴게", "휴게", "로비"], ["안내실", "안내실", "로비", "로비"],
    ["휴게", "안내실", "로비", "휴게"], ["안내실", "순찰", "로비", "순찰"],
    ["안내실", "안내실", "휴게", "로비"]
]

combined = [time_slots[i] + task_values[i] for i in range(len(time_slots))]
df_rt = pd.DataFrame(combined, columns=["From", "To", jojang, seonghui, uisanA, uisanB])

def get_current_idx(dt):
    curr_min = dt.hour * 60 + dt.minute
    if dt.hour < 7: curr_min += 1440
    # 마지막 시간대(06:00~07:00) 예외 처리: 정확히 07:00일 때 0번으로 가도록 함
    if dt.hour == 7 and dt.minute == 0: return 0
    
    for i, row in df_rt.iterrows():
        sh, sm = map(int, row['From'].split(':'))
        eh, em = map(int, row['To'].split(':'))
        s_min, e_min = sh * 60 + sm, eh * 60 + em
        if sh < 7: s_min += 1440
        if eh < 7 or (eh == 7 and em == 0 and sh < 7): e_min += 1440
        if s_min <= curr_min < e_min: return i
    return len(df_rt) - 1 # 범위를 벗어나면 마지막 인덱스 반환

curr_idx = get_current_idx(now)
curr_row = df_rt.iloc[curr_idx]

# --- [4] UI 렌더링 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%m/%d %H:%M")} ({work_date.strftime("%m/%d")} 근무분)</div>', unsafe_allow_html=True)

    # 상단 4인 현황 카드
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr_row[jojang]}</div></div>
            <div class="status-card"><div class="worker-name
