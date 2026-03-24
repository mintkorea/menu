import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (여백 중간값, 건물명 확대, 중앙 정렬) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    /* 1. 상단 여백 조정 (2.5rem과 4rem의 중간인 3.2rem) */
    .block-container { 
        padding-top: 3.2rem !important; 
        max-width: 500px;
        margin: auto;
    }
    
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 16px !important; text-align: center; margin-bottom: 15px; color: #555; }
    
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 10px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 10px; padding: 6px 0; 
        text-align: center; background: #F8F9FA; min-height: 65px;
    }
    .worker-name { font-size: 15px !important; font-weight: 700; color: #444; }
    .status-val { font-size: 18px; font-weight: 900; color: #C04B41; }
    
    /* 2. 건물 헤더 (폰트 크기 14px로 확대) */
    .b-header { 
        display: flex; border: 1px solid #dee2e6; border-bottom: none; 
        font-weight: bold; text-align: center; font-size: 14px; 
    }
    .b-section { width: 33.33%; padding: 7px 0; border-right: 1px solid #dee2e6; }
    .b-section:last-child { border-right: none; }

    /* 3. 표 중앙 정렬 및 가독성 설정 */
    [data-testid="stTable"] { 
        display: flex;
        justify-content: center;
    }
    [data-testid="stTable"] table {
        margin-left: auto;
        margin-right: auto;
        width: 100% !important;
    }
    [data-testid="stTable"] thead tr th {
        font-size: 10px !important;
        white-space: nowrap !important;
        letter-spacing: -1.0px !important;
        padding: 4px 1px !important;
        text-align: center !important;
    }
    [data-testid="stTable"] td {
        font-size: 10.5px !important;
        white-space: nowrap !important;
        padding: 4px 1px !important;
        text-align: center !important;
    }
    thead tr th:first-child, tbody th { display:none; }

    /* 편성표 높이 고정 */
    .stDataFrame { height: 450px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 (기본 데이터) ---
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
if jojang is None: jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

# --- [3] 화면 구성 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

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
    df_rt = pd.DataFrame(time_data, columns=["From", "To", jojang, seonghui, uisanA, uisanB])

    def get_rt_idx(h, m):
        if h == 1 and m < 40: return 16
        if h == 1 and m >= 40: return 17
        for i, row in df_rt.iterrows():
            try:
                sh, eh = int(row['From'].split(':')[0]), int(row['To'].split(':')[0])
                if eh == 0: eh = 24
                if sh <= h < eh: return i
            except: continue
        return 20

    curr_idx = get_rt_idx(now.hour, now.minute)
    curr_row = df_rt.iloc[curr_idx]

    # 상단 요약 카드
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr_row[jojang]}</div></div>
            <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr_row[seonghui]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr_row[uisanA]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr_row[uisanB]}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # 건물 헤더
    st.markdown(f"""<div class="b-header"><div class="b-section">구분 (시간)</div><div class="b-section" style="background:#FFF2CC;">성의회관</div><div class="b-section" style="background:#D9EAD3;">의산연</div></div>""", unsafe_allow_html=True)
    
    # 실시간 표 중앙 정렬 출력
    st.table(df_rt.iloc[curr_idx:].style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == curr_idx else ['']*len(r), axis=1))

with tab2:
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: start_d = st.date_input("📅 시작일", now.date(), key="d_v7")
    with c2: dur = st.slider("📆 일수", 7, 60, 31, key="s_v7")
    with c3: focus = st.selectbox("👤 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"], key="sb_v7")

    cal_list = []
    for i in range(dur):
        d = start_d + timedelta(days=i)
        w_jojang, w_seong, w_a, w_b = get_workers_by_date(d)
        if w_jojang: cal_list.append({"날짜": d.strftime("%m/%d(%a)"), "조장": w_jojang, "성희": w_seong, "의산A": w_a, "의산B": w_b})
    
    df_cal = pd.DataFrame(cal_list)
    if not df_cal.empty:
        color_map = {"황재업": "#D1FAE5", "김태언": "#FFF2CC", "이태원": "#E0F2FE", "이정석": "#FEE2E2"}
        def style_cal(row):
            styles = [''] * len(row)
            if 'Sun' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
            elif 'Sat' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
            if focus != "안 함":
                for idx, val in enumerate(row):
                    if val == focus: styles[idx] = f'background-color: {color_map.get(focus)}; font-weight: bold;'
            return styles
            
        st.dataframe(df_cal.style.apply(style_cal, axis=1), use_container_width=True, hide_index=True, height=450)

