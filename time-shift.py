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
    [data-testid="stTable"] table { margin-left: auto; margin-right: auto; width: 100% !important; }
    [data-testid="stTable"] thead tr th { font-size: 10px !important; padding: 4px 1px !important; text-align: center !important; }
    [data-testid="stTable"] td { font-size: 10.5px !important; padding: 4px 1px !important; text-align: center !important; }
    thead tr th:first-child, tbody th { display:none; }
    
    /* 체크박스 영역 중앙 정렬 */
    .view-option { text-align: right; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 (근무일 기준) ---
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
    return None, None, None, None

jojang, seonghui, uisanA, uisanB = get_workers_by_date(work_date)
if jojang is None: jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

# --- [3] 데이터 정의 ---
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
    for i, row in df_rt.iterrows():
        sh, sm = map(int, row['From'].split(':'))
        eh, em = map(int, row['To'].split(':'))
        s_min = sh * 60 + sm
        e_min = eh * 60 + em
        if sh < 7: s_min += 1440
        if eh < 7 or (eh == 7 and em == 0 and sh < 7): e_min += 1440
        if s_min <= curr_min < e_min: return i
    return 0

curr_idx = get_current_idx(now)
curr_row = df_rt.iloc[curr_idx]

# --- [4] UI ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr_row[jojang]}</div></div>
            <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr_row[seonghui]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr_row[uisanA]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr_row[uisanB]}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # 전체 보기 스위치 추가
    show_all = st.checkbox("🕒 지난 시간표 포함 (전체 보기)", value=False)

    st.markdown("""<div class="b-header"><div class="b-section">구분 (시간)</div><div class="b-section" style="background:#FFF2CC;">성의회관</div><div class="b-section" style="background:#D9EAD3;">의산연</div></div>""", unsafe_allow_html=True)
    
    # 로직 선택: show_all이 True면 전체, False면 현재 이후만
    display_df = df_rt if show_all else df_rt.iloc[curr_idx:]
    
    st.table(display_df.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == curr_idx else ['']*len(r), axis=1))

with tab2:
    # 편성표 코드는 이전과 동일 (생략 방지를 위해 유지)
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: start_d = st.date_input("📅 시작일", work_date, key="date_v3")
    with c2: dur = st.slider("📆 일수", 7, 60, 31, key="dur_v3")
    with c3: focus = st.selectbox("👤 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"], key="focus_v3")

    cal_list = []
    weeks = ['월', '화', '수', '목', '금', '토', '일']
    for i in range(dur):
        d = start_d + timedelta(days=i)
        w_j, w_s, w_a, w_b = get_workers_by_date(d)
        if w_j:
            cal_list.append({"날짜": f"{d.strftime('%m/%d')}({weeks[d.weekday()]})", "조장": w_j, "성희": w_s, "의산A": w_a, "의산B": w_b})
    
    if cal_list:
        df_cal = pd.DataFrame(cal_list)
        st.dataframe(df_cal.style.apply(lambda row: ['color: red' if '(일)' in row['날짜'] else 'color: blue' if '(토)' in row['날짜'] else '' for _ in row], axis=1), use_container_width=True, hide_index=True, height=500)
