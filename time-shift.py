import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 기본 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    /* 상단 여백 축소 */
    .block-container { padding-top: 1.5rem !important; }
    
    /* 타이틀 폰트 크기 동일하게 (28px) */
    .unified-title { 
        font-size: 28px !important; 
        font-weight: 800 !important;
        text-align: center; 
        margin-bottom: 5px; 
        color: #1E1E1E; 
    }
    .title-sub { font-size: 16px !important; font-weight: 400; text-align: center; margin-bottom: 20px; color: #666; }
    
    /* 카드 디자인: 이름 크기 강조 */
    .status-container { 
        display: grid; 
        grid-template-columns: repeat(2, 1fr); 
        gap: 10px; 
        margin-bottom: 20px; 
    }
    .status-card { 
        border: 2px solid #2E4077; 
        border-radius: 12px; 
        padding: 12px 5px; 
        text-align: center; 
        background: #F8F9FA; 
    }
    .name-label { font-size: 19px !important; font-weight: 800; color: #333; margin-bottom: 5px; }
    .loc-label { font-size: 20px; font-weight: 800; color: #C04B41; }
    
    .off-day-banner {
        background-color: #FFF3CD; color: #856404; padding: 10px;
        border-radius: 10px; text-align: center; font-weight: bold;
        margin-bottom: 15px; border: 1px solid #FFEEBA;
    }

    [data-testid="stTable"], [data-testid="stDataFrame"] { font-size: 16px !important; }
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜 및 시간/패턴 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
PATTERN_START = datetime(2026, 3, 9).date()

# 근무자 자동 추출 함수 (조회 시점의 날짜 기준)
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
tab1, tab2 = st.tabs(["🕒 실시간 근무 현황", "📅 월간 근무 편성표"])

# ---------------------------------------------------------
# TAB 1: 실시간 근무 현황
# ---------------------------------------------------------
with tab1:
    st.markdown(f'<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y년 %m월 %d일 %H:%M:%S")}</div>', unsafe_allow_html=True)

    if not is_work_day:
        st.markdown('<div class="off-day-banner">📅 오늘은 C조 휴무일입니다.</div>', unsafe_allow_html=True)
        # 휴무일인 경우 가장 최근/다음 근무자 정보를 예시로 표시하거나 공란 처리 가능
        jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

    # 근무 데이터 (1시간 단위)
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

    # 근무 현황 카드 (실제 이름 연동)
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="name-label">조장 ({jojang})</div><div class="loc-label">{curr['조장']}</div></div>
            <div class="status-card"><div class="name-label">성의회관 ({seonghui})</div><div class="loc-label">{curr['성의']}</div></div>
            <div class="status-card"><div class="name-label">의생연 A ({uisanA})</div><div class="loc-label">{curr['의생A']}</div></div>
            <div class="status-card"><div class="name-label">의생연 B ({uisanB})</div><div class="loc-label">{curr['의생B']}</div></div>
        </div>
    """, unsafe_allow_html=True)

    st.table(df_rt.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.equals(curr) and is_work_day else ['']*len(r), axis=1))

# ---------------------------------------------------------
# TAB 2: 월간 근무 편성표
# ---------------------------------------------------------
with tab2:
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1: start_d = st.date_input("📅 시작 날짜", now.date(), key="cal_start")
    with col2: dur = st.slider("📆 조회 일수", 7, 100, 31)
    with col3: focus = st.selectbox("👤 강조 인원", ["안 함", "황재업", "김태언", "이태원", "이정석"])

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
