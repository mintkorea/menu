import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (조장님 원본의 성의회관/의산연 구분 디자인 유지) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; color: #1E3A8A; margin-bottom: 5px; }
    .title-sub { font-size: 14px !important; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 상단 4인 실시간 카드 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 12px; padding: 10px 0; 
        text-align: center; background: white;
    }
    .worker-name { font-size: 15px !important; font-weight: 700; color: #444; }
    .status-val { font-size: 18px; font-weight: 900; color: #C04B41; }

    /* 성의회관/의산연 구분 헤더 (조장님 원본 스타일) */
    .b-header { 
        display: flex; border: 1px solid #dee2e6; border-bottom: none; 
        font-weight: bold; text-align: center; font-size: 14px; background: #f8f9fa;
    }
    .b-section { width: 33.33%; padding: 8px 0; border-right: 1px solid #dee2e6; }
    .b-section:last-child { border-right: none; }

    /* 표 스타일 (모바일 최적화) */
    [data-testid="stTable"] table { width: 100% !important; border-collapse: collapse; }
    [data-testid="stTable"] td { font-size: 12px !important; padding: 8px 2px !important; text-align: center !important; border: 1px solid #eee !important; }
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜 및 근무자 판정 로직 (조장님 원본 100% 복구) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
# 새벽 0~7시는 전날 근무일로 취급 (조장님 로직)
work_date = (now - timedelta(days=1)).date() if now.hour < 7 else now.date()
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        # 조장, 성희, 의산A, 의산B 순서
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return "황재업", "김태언", "이태원", "이정석"

jojang, seonghui, uisanA, uisanB = get_workers_by_date(work_date)

# --- [3] 근무 데이터 (조장님 원본 구조) ---
time_slots = [
    ["07:00", "08:00"], ["08:00", "09:00"], ["09:00", "10:00"], ["10:00", "11:00"],
    ["11:00", "12:00"], ["12:00", "13:00"], ["13:00", "14:00"], ["14:00", "15:00"],
    ["15:00", "16:00"], ["16:00", "17:00"], ["17:00", "18:00"], ["18:00", "19:00"],
    ["19:00", "20:00"], ["20:00", "21:00"], ["21:00", "22:00"], ["22:00", "23:00"],
    ["23:00", "01:40"], ["01:40", "02:00"], ["02:00", "05:00"], ["05:00", "06:00"],
    ["06:00", "07:00"]
]
tasks = [
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

combined = [time_slots[i] + tasks[i] for i in range(len(time_slots))]
df_rt = pd.DataFrame(combined, columns=["From", "To", jojang, seonghui, uisanA, uisanB])

def get_current_idx():
    m = now.hour * 60 + now.minute
    if now.hour < 7: m += 1440
    for i, row in enumerate(time_slots):
        sh, sm = map(int, row[0].split(':'))
        eh, em = map(int, row[1].split(':'))
        s, e = sh*60 + sm, eh*60 + em
        if sh < 7: s += 1440
        if eh < 7 or (eh==7 and em==0 and sh < 7): e += 1440
        if s <= m < e: return i
    return 0

curr_idx = get_current_idx()
curr_row = df_rt.iloc[curr_idx]

# --- [4] UI 출력 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{work_date.strftime("%m/%d")} 근무 (현재 {now.strftime("%H:%M")})</div>', unsafe_allow_html=True)

    # 상단 4인 카드
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr_row[jojang]}</div></div>
            <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr_row[seonghui]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr_row[uisanA]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr_row[uisanB]}</div></div>
        </div>
    """, unsafe_allow_html=True)

    show_all = st.checkbox("지난 시간표 포함 전체 보기", value=False)
    
    st.markdown(f"""<div class="b-header">
        <div class="b-section">시간</div>
        <div class="b-section" style="background:#FFF2CC;">성의회관</div>
        <div class="b-section" style="background:#D9EAD3;">의학연구원</div>
    </div>""", unsafe_allow_html=True)
    
    display_df = df_rt if show_all else df_rt.iloc[curr_idx:]
    st.table(display_df.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold; color: black;']*6 if r.name == curr_idx else ['']*6, axis=1))

with tab2:
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: start_d = st.date_input("📅 시작일", work_date, key="p_start")
    with c2: dur = st.slider("📆 일수", 7, 60, 31, key="p_dur")
    with c3: focus = st.selectbox("👤 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"], key="p_focus")

    cal_list = []
    weeks = ['월', '화', '수', '목', '금', '토', '일']
    for i in range(dur):
        d = start_d + timedelta(days=i)
        w_j, w_s, w_a, w_b = get_workers_by_date(d)
        cal_list.append({"날짜": f"{d.strftime('%m/%d')}({weeks[d.weekday()]})", "조장": w_j, "성희": w_s, "의산A": w_a, "의산B": w_b})
    
    df_cal = pd.DataFrame(cal_list)
    def style_cal(row):
        styles = [''] * len(row)
        if '(일)' in row['날짜']: styles[0] = 'color: red; font-weight: bold;'
        elif '(토)' in row['날짜']: styles[0] = 'color: blue; font-weight: bold;'
        if focus != "안 함":
            for i, v in enumerate(row):
                if v == focus: styles[i] = 'background-color: #FFF2CC; color: black; font-weight: bold;'
        return styles
    st.dataframe(df_cal.style.apply(style_cal, axis=1), use_container_width=True, hide_index=True, height=500)
