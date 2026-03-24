import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (표 높이 고정 및 개행 방지) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; }
    
    /* 🚨 편성표(Tab 2) 내부 스크롤 강제 고정 🚨 */
    /* 표가 일정 높이 이상 커지면 내부에서 스크롤이 생기도록 함 */
    div[data-testid="stDataFrame"] > div:first-child {
        height: 400px !important; 
        overflow-y: auto !important;
    }

    /* 표 헤더 이름 깨짐 방지 (김태언 한 줄 유지) */
    [data-testid="stTable"] thead tr th {
        font-size: 10px !important;
        white-space: nowrap !important;
        letter-spacing: -1.0px !important;
        padding: 4px 1px !important;
    }
    
    [data-testid="stTable"] td {
        font-size: 10.5px !important;
        white-space: nowrap !important;
        padding: 4px 1px !important;
    }

    .unified-title { font-size: 22px !important; font-weight: 800; text-align: center; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-top: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 5px 0; text-align: center; background: #F8F9FA; }
    
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 (기존 동일) ---
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
    st.markdown('<div class="unified-title">C조 실시간 현황</div>', unsafe_allow_html=True)
    time_data = [["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"], ["09:00", "10:00", "순찰", "안내실", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "순찰"], ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"], ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"], ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"], ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"], ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"], ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"], ["23:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"], ["02:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"], ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"]]
    df_rt = pd.DataFrame(time_data, columns=["From", "To", jojang, seonghui, uisanA, uisanB])
    
    st.table(df_rt) # 실시간 표는 현재 시간 강조 없이 전체 출력

with tab2:
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    
    # 설정 컨트롤러
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: start_d = st.date_input("📅 시작일", now.date(), key="d_v5")
    with c2: dur = st.slider("📆 일수", 7, 60, 31, key="s_v5")
    with c3: focus = st.selectbox("👤 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"], key="sb_v5")

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
            
        # ⭐️ height 설정을 통해 표 내부 스크롤 활성화
        st.dataframe(df_cal.style.apply(style_cal, axis=1), use_container_width=True, hide_index=True, height=400)
