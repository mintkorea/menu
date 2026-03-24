import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2.5rem !important; }
    .unified-title { font-size: 26px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 15px; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 카드 디자인: 높이 최소화 */
    .status-container { 
        display: grid; grid-template-columns: repeat(2, 1fr); 
        gap: 8px; margin-bottom: 20px; 
    }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 10px; 
        padding: 10px 0; text-align: center; background: #F8F9FA;
        min-height: 65px; display: flex; flex-direction: column; justify-content: center;
    }
    .worker-name { font-size: 16px !important; font-weight: 700; color: #444; margin-bottom: 2px; }
    .status-val { font-size: 19px; font-weight: 800; color: #C04B41; }
    
    /* 테이블 가독성 */
    [data-testid="stTable"], [data-testid="stDataFrame"] { font-size: 15px !important; }
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 공통 데이터 및 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
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

j, s, a, b = get_workers_by_date(now.date())
is_work_day = j is not None

# --- [3] 탭 메뉴 구성 ---
tab1, tab2 = st.tabs(["🕒 실시간 근무 현황", "📅 월간 근무 편성표"])

# ---------------------------------------------------------
# TAB 1: 실시간 근무 현황 (현재 시간부터 정렬)
# ---------------------------------------------------------
with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    if not is_work_day:
        st.warning("📅 오늘은 C조 휴무일입니다.")
        j, s, a, b = "황재업", "김태언", "이태원", "이정석"

    # 전체 데이터 준비
    time_raw = [
        ["07:00", "08:00"], ["08:00", "09:00"], ["09:00", "10:00"], ["10:00", "11:00"],
        ["11:00", "12:00"], ["12:00", "13:00"], ["13:00", "14:00"], ["14:00", "15:00"],
        ["15:00", "16:00"], ["16:00", "17:00"], ["17:00", "18:00"], ["18:00", "19:00"],
        ["19:00", "20:00"], ["20:00", "21:00"], ["21:00", "22:00"], ["22:00", "23:00"],
        ["23:00", "01:40"], ["01:40", "02:00"], ["02:00", "05:00"], ["05:00", "06:00"], ["06:00", "07:00"]
    ]
    loc_raw = [
        ["안내실", "로비", "로비", "휴게"], ["안내실", "휴게", "휴게", "로비"],
        ["순찰", "안내실", "휴게", "로비"], ["휴게", "안내실", "로비", "순찰"],
        ["안내실", "중식", "로비", "중식"], ["중식", "안내실", "중식", "로비"],
        ["안내실", "휴게", "순찰", "로비"], ["순찰", "안내실", "로비", "휴게"],
        ["안내실", "휴게", "로비", "휴게"], ["휴게", "안내실", "휴게", "로비"],
        ["안내실", "휴게", "휴게", "로비"], ["안내실", "석식", "로비", "석식"],
        ["안내실", "안내실", "석식", "로비"], ["석식", "안내실", "로비", "휴게"],
        ["안내실", "순찰", "로비", "휴게"], ["순찰", "안내실", "순찰", "로비"],
        ["안내실", "휴게", "휴게", "로비"], ["안내실", "안내실", "로비", "로비"],
        ["휴게", "안내실", "로비", "휴게"], ["안내실", "순찰", "로비", "순찰"], ["안내실", "안내실", "휴게", "로비"]
    ]
    df_full = pd.DataFrame([t + l for t, l in zip(time_raw, loc_raw)], 
                           columns=["From", "To", "조장", "성의", "의생A", "의생B"])

    def get_curr_idx(h, m):
        if h == 1 and m < 40: return 16
        if h == 1 and m >= 40: return 17
        for i, row in df_full.iterrows():
            try:
                sh, eh = int(row['From'].split(':')[0]), int(row['To'].split(':')[0])
                if eh == 0 or eh < sh: eh = 24
                if sh <= h < eh: return i
            except: continue
        return 20

    idx = get_curr_idx(now.hour, now.minute)
    curr_row = df_full.iloc[idx]
    
    # ⭐️ 현재 인덱스부터 끝까지만 노출
    df_display = df_full.iloc[idx:].copy()

    # 상단 카드
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{j}</div><div class="status-val">{curr_row['조장']}</div></div>
            <div class="status-card"><div class="worker-name">{s}</div><div class="status-val">{curr_row['성의']}</div></div>
            <div class="status-card"><div class="worker-name">{a}</div><div class="status-val">{curr_row['의생A']}</div></div>
            <div class="status-card"><div class="worker-name">{b}</div><div class="status-val">{curr_row['의생B']}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # 표 출력 (첫 행 하이라이트)
    st.table(df_display.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == idx and is_work_day else ['']*len(r), axis=1))

# ---------------------------------------------------------
# TAB 2: 월간 근무 편성표
# ---------------------------------------------------------
with tab2:
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1: start_d = st.date_input("📅 시작일", now.date(), key="cal_start")
    with col2: dur = st.slider("📆 일수", 7, 60, 31)
    with col3: focus = st.selectbox("👤 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])

    cal_list = []
    for i in range(dur):
        d = start_d + timedelta(days=i)
        wj, ws, wa, wb = get_workers_by_date(d)
        if wj:
            cal_list.append({"날짜": d.strftime("%m/%d(%a)"), "조장": wj, "성희": ws, "의산A": wa, "의산B": wb})

    if cal_list:
        df_cal = pd.DataFrame(cal_list)
        color_map = {"황재업": "#D1FAE5", "김태언": "#FFF2CC", "이태원": "#E0F2FE", "이정석": "#FEE2E2"}
        def style_cal(row):
            styles = [''] * len(row)
            if 'Sun' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
            elif 'Sat' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
            if focus != "안 함":
                for i, v in enumerate(row):
                    if v == focus: styles[i] = f'background-color: {color_map.get(focus)}; font-weight: bold; color: black;'
            return styles
        st.dataframe(df_cal.style.apply(style_cal, axis=1), use_container_width=True, hide_index=True, height=(len(df_cal)+1)*38)
