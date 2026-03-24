import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (인사말 카드 스타일 강화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 16px !important; text-align: center; margin-bottom: 15px; color: #555; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 10px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 10px; padding: 10px 5px; 
        text-align: center; background: #F8F9FA; min-height: 80px;
        display: flex; flex-direction: column; justify-content: center;
    }
    .worker-name { font-size: 14px !important; font-weight: 700; color: #666; margin-bottom: 3px; }
    .status-val { font-size: 17px; font-weight: 900; color: #C04B41; }
    
    /* 큰 인사말 카드 */
    .msg-card-full {
        grid-column: span 2;
        border: 2px solid #2E4077; border-radius: 12px; padding: 30px 20px;
        text-align: center; font-size: 20px; font-weight: 800; line-height: 1.6;
        margin-bottom: 15px;
    }
    .b-header { display: flex; border: 1px solid #dee2e6; border-bottom: none; font-weight: bold; text-align: center; font-size: 14px; }
    .b-section { width: 33.33%; padding: 7px 0; border-right: 1px solid #dee2e6; }
    [data-testid="stTable"] table { width: 100% !important; }
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜 및 근무 판별 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
curr_time_num = now.hour * 60 + now.minute

# 패턴 기준일
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

# 근무 투입일(첫날)인지, 퇴근하는 새벽(둘째날)인지 판별
is_work_start_day = get_workers_by_date(now.date())[0] is not None
is_work_end_dawn = now.hour < 7 and get_workers_by_date((now - timedelta(days=1)).date())[0] is not None

# 근무 데이터 기준일 설정
if now.hour < 7:
    work_date = (now - timedelta(days=1)).date()
else:
    work_date = now.date()

jojang, seonghui, uisanA, uisanB = get_workers_by_date(work_date)
if jojang is None: jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

# --- [3] 시간표 데이터 (생략 없이 유지) ---
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
    c_m = dt.hour * 60 + dt.minute
    if dt.hour < 7: c_m += 1440
    for i, row in df_rt.iterrows():
        sh, sm = map(int, row['From'].split(':'))
        eh, em = map(int, row['To'].split(':'))
        s_m, e_m = sh * 60 + sm, eh * 60 + em
        if sh < 7: s_m += 1440
        if eh < 7 or (eh == 7 and em == 0 and sh < 7): e_m += 1440
        if s_m <= c_m < e_m: return i
    return -1

curr_idx = get_current_idx(now)

# --- [4] UI 렌더링 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    # --- 카드 영역 조건부 표출 로직 ---
    # 상황 1: 근무 투입일(첫날) 새벽 00:00 ~ 07:00
    if is_work_start_day and now.hour < 7:
        st.markdown("""
            <div class="msg-card-full" style="background: #F0FDF4; color: #166534; border-color: #166534;">
                오늘도 즐겁고 보람된<br>하루가 되도록 합시다.
            </div>
        """, unsafe_allow_html=True)
    
    # 상황 2: 근무 퇴근일(둘째날) 새벽 06:40 ~ 07:00
    elif is_work_end_dawn and (now.hour == 6 and now.minute >= 40):
        st.markdown("""
            <div class="msg-card-full" style="background: #EEF2FF; color: #2E4077; border-color: #2E4077;">
                수고하셨습니다.<br>다음 근무 때 뵙겠습니다.
            </div>
        """, unsafe_allow_html=True)

    # 상황 3: 그 외 근무 시간 (카드 표시)
    elif curr_idx != -1:
        curr_row = df_rt.iloc[curr_idx]
        st.markdown(f"""
            <div class="status-container">
                <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr_row[jojang]}</div></div>
                <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr_row[seonghui]}</div></div>
                <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr_row[uisanA]}</div></div>
                <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr_row[uisanB]}</div></div>
            </div>
        """, unsafe_allow_html=True)
    
    # 상황 4: 비번일 등 그 외 시간
    else:
        st.info("현재는 C조 근무 시간이 아닙니다.")

    # --- 시간표 영역 (기존 유지) ---
    show_all = st.checkbox("🕒 지난 시간표 포함 (전체 보기)", value=False)
    st.markdown("""<div class="b-header"><div class="b-header"><div class="b-section">구분 (시간)</div><div class="b-section" style="background:#FFF2CC;">성의회관</div><div class="b-section" style="background:#D9EAD3;">의산연</div></div>""", unsafe_allow_html=True)
    display_df = df_rt if show_all or curr_idx == -1 else df_rt.iloc[curr_idx:]
    st.table(display_df.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold; color: black;']*len(r) if r.name == curr_idx else ['']*len(r), axis=1))

with tab2:
    # [근무 편성표 탭은 이전과 동일하게 유지]
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: start_d = st.date_input("📅 시작일", work_date, key="date_vfinal")
    with c2: dur = st.slider("📆 일수", 7, 60, 31, key="dur_vfinal")
    with c3: focus = st.selectbox("👤 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"], key="focus_vfinal")
    # ... (이후 스타일링 및 데이터프레임 출력 코드는 동일)
