import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (기존 유지) ---
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
    .b-section:last-child { border-right: none; }
    [data-testid="stTable"] { display: flex; justify-content: center; }
    [data-testid="stTable"] table { width: 100% !important; }
    [data-testid="stTable"] thead tr th { font-size: 10px !important; padding: 4px 1px !important; text-align: center !important; }
    [data-testid="stTable"] td { font-size: 10.5px !important; padding: 4px 1px !important; text-align: center !important; }
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 (근무일 기준 수정) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# 중요: 새벽 00:00 ~ 06:59까지는 '어제' 근무일로 처리
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
    return None, None, None, None

jojang, seonghui, uisanA, uisanB = get_workers_by_date(work_date)
# 데이터 없을 시 기본값
if jojang is None: jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

# --- [3] 데이터 정의 ---
time_data = [
    ["07:00", "08:00"], ["08:00", "09:00"], ["09:00", "10:00"], ["10:00", "11:00"],
    ["11:00", "12:00"], ["12:00", "13:00"], ["13:00", "14:00"], ["14:00", "15:00"],
    ["15:00", "16:00"], ["16:00", "17:00"], ["17:00", "18:00"], ["18:00", "19:00"],
    ["19:00", "20:00"], ["20:00", "21:00"], ["21:00", "22:00"], ["22:00", "23:00"],
    ["23:00", "01:40"], ["01:40", "02:00"], ["02:00", "05:00"], ["05:00", "06:00"],
    ["06:00", "07:00"]
]
# 상세 근무 위치 데이터 연합
task_data = [
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

combined_data = []
for i in range(len(time_data)):
    combined_data.append(time_data[i] + task_data[i])

df_rt = pd.DataFrame(combined_data, columns=["From", "To", jojang, seonghui, uisanA, uisanB])

# 인덱스 추출 함수 개선
def get_rt_idx(now_dt):
    h, m = now_dt.hour, now_dt.minute
    # 모든 시간을 '분' 단위로 변환하여 비교
    curr_total_min = h * 60 + m
    
    # 만약 새벽(00:00~06:59)이라면 시간을 24시간 이후로 처리 (비교 용이성)
    if h < 7:
        curr_total_min += 24 * 60

    for i, row in df_rt.iterrows():
        start_h, start_m = map(int, row['From'].split(':'))
        end_h, end_m = map(int, row['To'].split(':'))
        
        start_total = start_h * 60 + start_m
        end_total = end_h * 60 + end_m
        
        # 시작 시간이 0~6시 사이면 24시간 더함
        if start_h < 7: start_total += 24 * 60
        # 종료 시간이 0~7시 사이면 24시간 더함
        if end_h <= 7 and end_h > 0 or (end_h == 0): 
            if not (end_h == 7 and end_m == 0 and start_h >= 7): # 아침 7시 정각 예외처리
                end_total += 24 * 60
        if end_h == 7 and end_m == 0: end_total = 31 * 60 # 다음날 07시

        if start_total <= curr_total_min < end_total:
            return i
    return 0

curr_idx = get_rt_idx(now)
curr_row = df_rt.iloc[curr_idx]

# --- [4] 화면 출력 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    # 요약 카드
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr_row[jojang]}</div></div>
            <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr_row[seonghui]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr_row[uisanA]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr_row[uisanB]}</div></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""<div class="b-header"><div class="b-section">구분 (시간)</div><div class="b-section" style="background:#FFF2CC;">성의회관</div><div class="b-section" style="background:#D9EAD3;">의산연</div></div>""", unsafe_allow_html=True)
    
    # 현재 시간 이후만 표출
    st.table(df_rt.iloc[curr_idx:].style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == curr_idx else ['']*len(r), axis=1))

with tab2:
    # (편성표 로직은 기존과 동일하되 work_date 기준 권장)
    st.write("📅 날짜별 근무 조원 확인")
    # ... (생략된 기존 편성표 코드)
