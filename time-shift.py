import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (모바일 레이아웃 최적화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 22px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 14px !important; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 카드 디자인 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }
    .status-card { 
        border: 1.5px solid #2E4077; border-radius: 12px; padding: 12px 5px; 
        text-align: center; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .worker-name { font-size: 13px; font-weight: 600; color: #777; margin-bottom: 4px; }
    .status-val { font-size: 16px; font-weight: 800; color: #C04B41; }
    
    /* 메시지 카드 */
    .msg-card-full {
        grid-column: span 2; border-radius: 12px; padding: 25px 15px;
        text-align: center; font-size: 18px; font-weight: 800; line-height: 1.5;
        margin-bottom: 15px; border: 2px solid #2E4077;
    }

    /* 표 간격 조정 */
    [data-testid="stDataFrame"] { width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜 및 패턴 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# 패턴 기준일 (사용자 데이터 기반)
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

# 현재 근무일 판별 (새벽 7시 기준)
if now.hour < 7:
    work_date = (now - timedelta(days=1)).date()
    is_work_start_day = get_workers_by_date(now.date())[0] is not None
    is_work_end_dawn = get_workers_by_date(work_date)[0] is not None
else:
    work_date = now.date()
    is_work_start_day = get_workers_by_date(work_date)[0] is not None
    is_work_end_dawn = False

jojang, seonghui, uisanA, uisanB = get_workers_by_date(work_date)
if jojang is None: jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

# --- [3] 데이터 정의 ---
combined_data = [
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
df_rt = pd.DataFrame(combined_data, columns=["From", "To", jojang, seonghui, uisanA, uisanB])

def get_current_idx(dt):
    curr_m = dt.hour * 60 + dt.minute
    if dt.hour < 7: curr_m += 1440
    for i, row in df_rt.iterrows():
        sh, sm = map(int, row['From'].split(':'))
        eh, em = map(int, row['To'].split(':'))
        s_m, e_m = sh * 60 + sm, eh * 60 + em
        if sh < 7: s_m += 1440
        if eh < 7 or (eh == 7 and em == 0 and sh < 7): e_m += 1440
        if s_m <= curr_m < e_m: return i
    return -1

curr_idx = get_current_idx(now)

# --- [4] UI ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    # 카드 영역
    if is_work_start_day and now.hour < 7:
        st.markdown('<div class="msg-card-full" style="background:#F0FDF4; color:#166534;">오늘도 즐겁고 보람된<br>하루가 되도록 합시다.</div>', unsafe_allow_html=True)
    elif is_work_end_dawn and (now.hour == 6 and now.minute >= 40):
        st.markdown('<div class="msg-card-full" style="background:#EEF2FF; color:#2E4077;">수고하셨습니다.<br>다음 근무 때 뵙겠습니다.</div>', unsafe_allow_html=True)
    elif curr_idx != -1:
        c_row = df_rt.iloc[curr_idx]
        st.markdown(f"""
            <div class="status-container">
                <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{c_row[jojang]}</div></div>
                <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{c_row[seonghui]}</div></div>
                <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{c_row[uisanA]}</div></div>
                <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{c_row[uisanB]}</div></div>
            </div>
        """, unsafe_allow_html=True)

    show_all = st.checkbox("🕒 지난 시간표 포함", value=False)
    display_df = df_rt if show_all else df_rt.iloc[curr_idx:]
    
    # 표 깨짐 방지를 위해 스타일을 단순화한 dataframe 사용
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: s_date = st.date_input("📅 시작일", work_date)
    with col2: focus_user = st.selectbox("👤 강조 대상", ["안 함", "황재업", "김태언", "이태원", "이정석"])
    
    days = st.slider("📆 확인 일수", 7, 60, 31)
    
    cal_data = []
    w_names = ['월', '화', '수', '목', '금', '토', '일']
    for i in range(days):
        d = s_date + timedelta(days=i)
        w1, w2, w3, w4 = get_workers_by_date(d)
        if w1:
            cal_data.append({"날짜": f"{d.strftime('%m/%d')}({w_names[d.weekday()]})", "조장": w1, "성희": w2, "의산A": w3, "의산B": w4})
    
    if cal_data:
        df_cal = pd.DataFrame(cal_data)
        
        def highlight_focus(s):
            if focus_user != "안 함" and s == focus_user:
                return 'background-color: #FFF2CC; color: black; font-weight: bold'
            return ''

        st.dataframe(df_cal.style.map(highlight_focus), use_container_width=True, hide_index=True, height=500)
    else:
        st.warning("선택한 기간에 C조 근무가 없습니다.")
