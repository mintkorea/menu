import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (높이 최소화 및 디자인 최적화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    /* 상단 여백 유지 */
    .block-container { padding-top: 2.5rem !important; }
    
    /* 타이틀 스타일 */
    .unified-title { 
        font-size: 26px !important; 
        font-weight: 800 !important;
        text-align: center; 
        margin-bottom: 5px; 
        color: #1E1E1E; 
    }
    .title-sub { 
        font-size: 15px !important; 
        text-align: center; 
        margin-bottom: 20px; 
        color: #666; 
    }
    
    /* 카드 높이 축소 및 레이아웃 */
    .status-container { 
        display: grid; 
        grid-template-columns: repeat(2, 1fr); 
        gap: 8px; 
        margin-bottom: 15px; 
    }
    .status-card { 
        border: 2px solid #2E4077; 
        border-radius: 10px; 
        padding: 8px 0px; /* 세로 패딩 최소화 */
        text-align: center; 
        background: #F8F9FA; 
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 70px; /* 카드 최소 높이 설정 */
    }
    /* 성함 스타일 */
    .worker-name { 
        font-size: 17px !important; 
        font-weight: 700; 
        color: #444; 
        margin-bottom: 2px; 
    }
    /* 근무 상태 스타일 */
    .status-val { 
        font-size: 20px; 
        font-weight: 800; 
        color: #C04B41; 
    }
    
    /* 테이블 스타일 */
    [data-testid="stTable"], [data-testid="stDataFrame"] { font-size: 15px !important; }
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜/시간 및 근무자 패턴 로직 ---
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

jojang, seonghui, uisanA, uisanB = get_workers_by_date(now.date())
is_work_day = jojang is not None

# --- [3] 탭 구성 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

# ---------------------------------------------------------
# TAB 1: 실시간 근무 현황 (콤팩트 카드)
# ---------------------------------------------------------
with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    if not is_work_day:
        st.warning("📅 오늘은 C조 휴무일입니다.")
        jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

    # 시간표 데이터
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
    df_rt = pd.DataFrame(time_data, columns=["From", "To", "조장", "성의", "의생A", "의생B"])

    def get_rt_row(h, m):
        if h == 1 and m < 40: return df_rt[df_rt['From'] == "23:00"].iloc[0]
        if h == 1 and m >= 40: return df_rt[df_rt['From'] == "01:40"].iloc[0]
        for _, row in df_rt.iterrows():
            try:
                sh, eh = int(row['From'].split(':')[0]), int(row['To'].split(':')[0])
                if eh == 0: eh = 24
                if sh <= h < eh: return row
            except: continue
        return df_rt.iloc[-1]

    curr = get_rt_row(now.hour, now.minute)

    # 현황 카드 (이름과 상태만 표시, 높이 축소)
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr['조장']}</div></div>
            <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr['성의']}</div></div>
            <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr['의생A']}</div></div>
            <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr['의생B']}</div></div>
        </div>
    """, unsafe_allow_html=True)

    st.table(df_rt.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.equals(curr) and is_work_day else ['']*len(r), axis=1))

# ---------------------------------------------------------
# TAB 2: 월간 근무 편성표
# ---------------------------------------------------------
with tab2:
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1: start_d = st.date_input("📅 시작일", now.date())
    with col2: dur = st.slider("📆 일수", 7, 60, 31)
    with col3: focus = st.selectbox("👤 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])

    cal_list = []
    for i in range(dur):
        d = start_d + timedelta(days=i)
        w_jojang, w_seong, w_a, w_b = get_workers_by_date(d)
        if w_jojang:
            cal_list.append({"날짜": d.strftime("%m/%d(%a)"), "조장": w_jojang, "성희": w_seong, "의산A": w_a, "의산B": w_b})

    df_cal = pd.DataFrame(cal_list)
    if not df_cal.empty:
        color_map = {"황재업": "#D1FAE5", "김태언": "#FFF2CC", "이태원": "#E0F2FE", "이정석": "#FEE2E2"}
        def style_cal(row):
            styles = [''] * len(row)
            if 'Sun' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
            elif 'Sat' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
            if focus != "안 함":
                for idx, val in enumerate(row):
                    if val == focus: styles[idx] = f'background-color: {color_map.get(focus)}; font-weight: bold; color: black;'
            return styles
        st.dataframe(df_cal.style.apply(style_cal, axis=1), use_container_width=True, hide_index=True, height=(len(df_cal)+1)*38)
