import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { 
        padding-top: 3.2rem !important; 
        max-width: 500px;
        margin: auto;
    }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 16px !important; text-align: center; margin-bottom: 15px; color: #555; }
    
    /* 카드 영역 스타일 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 10px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 10px; padding: 10px 5px; 
        text-align: center; background: #F8F9FA; min-height: 80px;
        display: flex; flex-direction: column; justify-content: center;
    }
    .worker-name { font-size: 14px !important; font-weight: 700; color: #666; margin-bottom: 3px; }
    .status-val { font-size: 17px; font-weight: 900; color: #C04B41; }
    
    /* 종료/새벽 인사말 카드 스타일 */
    .msg-card {
        grid-column: span 2;
        border: 2px solid #2E4077; border-radius: 10px; padding: 20px;
        text-align: center; background: #EEF2FF; color: #2E4077;
        font-size: 18px; font-weight: 800; line-height: 1.5;
        margin-bottom: 10px;
    }

    .b-header { 
        display: flex; border: 1px solid #dee2e6; border-bottom: none; 
        font-weight: bold; text-align: center; font-size: 14px; 
    }
    .b-section { width: 33.33%; padding: 7px 0; border-right: 1px solid #dee2e6; }
    [data-testid="stTable"] table { width: 100% !important; }
    [data-testid="stTable"] td { font-size: 10.5px !important; padding: 4px 1px !important; text-align: center !important; }
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 설정 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# 근무 기준 시간 설정
is_dawn = now.hour < 7 # 새벽 0시 ~ 7시 여부

if is_dawn:
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

# --- [3] 시간표 데이터 ---
combined = [
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
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"]
]
df_rt = pd.DataFrame(combined, columns=["From", "To", jojang, seonghui, uisanA, uisanB])

def get_current_idx(dt):
    curr_min = dt.hour * 60 + dt.minute
    if dt.hour < 7: curr_min += 1440
    for i, row in df_rt.iterrows():
        sh, sm = map(int, row['From'].split(':'))
        eh, em = map(int, row['To'].split(':'))
        s_min, e_min = sh * 60 + sm, eh * 60 + em
        if sh < 7: s_min += 1440
        if eh < 7 or (eh == 7 and em == 0 and sh < 7): e_min += 1440
        if s_min <= curr_min < e_min: return i
    return -1 # 근무 시간 외

curr_idx = get_current_idx(now)

# --- [4] UI 렌더링 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    # --- 카드 영역 로직 수정 ---
    if curr_idx == -1: # 근무 종료 후 (07:00 ~ 다음 근무 시작 전)
        st.markdown("""
            <div class="msg-card">
                수고하셨습니다.<br>다음 근무 때 뵙겠습니다.
            </div>
        """, unsafe_allow_html=True)
    elif is_dawn: # 당일 새벽 (00:00 ~ 07:00)
        st.markdown("""
            <div class="msg-card" style="background: #F0FDF4; color: #166534; border-color: #166534;">
                오늘도 즐겁고 보람된<br>하루가 되도록 합시다.
            </div>
        """, unsafe_allow_html=True)
        # 새벽에도 누구인지 보여주기 위해 유지
        curr_row = df_rt.iloc[curr_idx]
        st.markdown(f"""
            <div class="status-container">
                <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr_row[jojang]}</div></div>
                <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr_row[seonghui]}</div></div>
                <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr_row[uisanA]}</div></div>
                <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr_row[uisanB]}</div></div>
            </div>
        """, unsafe_allow_html=True)
    else: # 정상 근무 시간 (07:00 ~ 23:59)
        curr_row = df_rt.iloc[curr_idx]
        st.markdown(f"""
            <div class="status-container">
                <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr_row[jojang]}</div></div>
                <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr_row[seonghui]}</div></div>
                <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr_row[uisanA]}</div></div>
                <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr_row[uisanB]}</div></div>
            </div>
        """, unsafe_allow_html=True)

    # --- 시간표 영역 ---
    show_all = st.checkbox("🕒 지난 시간표 포함 (전체 보기)", value=False)
    st.markdown("""<div class="b-header"><div class="b-section">구분 (시간)</div><div class="b-section" style="background:#FFF2CC;">성의회관</div><div class="b-section" style="background:#D9EAD3;">의산연</div></div>""", unsafe_allow_html=True)
    
    if curr_idx == -1: # 근무 종료 후에는 전체 시간표 혹은 다음 스케줄 준비
        display_df = df_rt
    else:
        display_df = df_rt if show_all else df_rt.iloc[curr_idx:]
    
    st.table(display_df.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold; color: black;']*len(r) if r.name == curr_idx else ['']*len(r), axis=1))

with tab2:
    # 편성표 및 강조 로직 (이전과 동일)
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: start_d = st.date_input("📅 시작일", work_date, key="date_vfinal")
    with c2: dur = st.slider("📆 일수", 7, 60, 31, key="dur_vfinal")
    with c3: focus = st.selectbox("👤 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"], key="focus_vfinal")

    cal_list = []
    weeks = ['월', '화', '수', '목', '금', '토', '일']
    for i in range(dur):
        d = start_d + timedelta(days=i)
        w_j, w_s, w_a, w_b = get_workers_by_date(d)
        if w_j:
            cal_list.append({"날짜": f"{d.strftime('%m/%d')}({weeks[d.weekday()]})", "조장": w_j, "성희": w_s, "의산A": w_a, "의산B": w_b})
    
    if cal_list:
        df_cal = pd.DataFrame(cal_list)
        color_map = {"황재업": "background-color: #D1FAE5; color: black;", "김태언": "background-color: #FFF2CC; color: black;", "이태원": "background-color: #E0F2FE; color: black;", "이정석": "background-color: #FEE2E2; color: black;"}
        def style_fn(row):
            styles = [''] * len(row)
            if '(일)' in row['날짜']: styles[0] = 'color: red; font-weight: bold;'
            elif '(토)' in row['날짜']: styles[0] = 'color: blue; font-weight: bold;'
            if focus != "안 함":
                for i in range(len(row)):
                    if row.iloc[i] == focus: styles[i] = color_map.get(focus, '') + " font-weight: bold;"
            return styles
        st.dataframe(df_cal.style.apply(style_fn, axis=1), use_container_width=True, hide_index=True, height=500)
