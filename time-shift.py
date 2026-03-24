import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 15px !important; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 카드 디자인 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 12px; padding: 15px 5px; 
        text-align: center; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .worker-name { font-size: 17px !important; font-weight: 700; color: #555; margin-bottom: 5px; }
    .status-val { font-size: 21px !important; font-weight: 900; color: #C04B41; }
    
    /* 휴무 안내 카드 (붉은색 큰 글씨) */
    .off-card {
        grid-column: span 2; border-radius: 12px; padding: 25px 15px;
        text-align: center; background: #FFF5F5; border: 2px solid #C04B41;
        margin-bottom: 15px;
    }
    .off-title { font-size: 26px !important; font-weight: 900; color: #C04B41; margin-bottom: 10px; }
    .next-info { font-size: 16px; font-weight: 700; color: #333; line-height: 1.6; }

    /* 건물 구분 헤더 */
    .b-header { 
        display: flex; border: 1px solid #dee2e6; border-bottom: none; 
        font-weight: bold; text-align: center; font-size: 15px; margin-top: 10px;
    }
    .b-section { width: 33.33%; padding: 8px 0; border-right: 1px solid #dee2e6; }
    .b-section:last-child { border-right: none; }

    /* 일반 메시지 카드 */
    .msg-card-full {
        grid-column: span 2; border-radius: 12px; padding: 30px 20px;
        text-align: center; font-size: 21px; font-weight: 800; line-height: 1.5;
        margin-bottom: 15px; border: 2px solid #2E4077;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜 및 패턴 로직 ---
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

# 휴무 및 근무 판별
today = now.date()
is_today_work = get_workers_by_date(today)[0] is not None
is_yesterday_work = get_workers_by_date(today - timedelta(days=1))[0] is not None

# 휴무 안내 표출 조건: 
# 1. 어제 근무했고 오늘 오전 7시 이후 (퇴근 날 휴무 시작)
# 2. 어제 근무 안 했고 오늘 근무 안 함 (완전한 휴무일)
is_off_display = False
if is_yesterday_work and not is_today_work and now.hour >= 7:
    is_off_display = True
elif not is_yesterday_work and not is_today_work:
    is_off_display = True

# 다음 근무일 찾기
next_work_date = today
while get_workers_by_date(next_work_date)[0] is None:
    next_work_date += timedelta(days=1)
n_j, n_s, n_a, n_b = get_workers_by_date(next_work_date)

# 현재 근무 데이터 기준일 (새벽 7시 이전이면 어제 날짜 데이터 사용)
work_date = (today - timedelta(days=1)) if now.hour < 7 else today
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
    if is_off_display:
        st.markdown(f"""
            <div class="off-card">
                <div class="off-title">오늘은 휴무입니다.</div>
                <div class="next-info">
                    다음 근무는 {next_work_date.strftime('%m월 %d일')}입니다.<br>
                    성의회관 {n_j}, {n_s}<br>
                    의 산 연 {n_a}, {n_b}
                </div>
            </div>
        """, unsafe_allow_html=True)
    elif is_today_work and now.hour < 7:
        st.markdown('<div class="msg-card-full" style="background:#F0FDF4; color:#166534;">오늘도 즐겁고 보람된<br>하루가 되도록 합시다.</div>', unsafe_allow_html=True)
    elif is_yesterday_work and (now.hour == 6 and now.minute >= 40):
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

    # 시간표 헤더 및 표
    st.markdown('<div class="b-header"><div class="b-section">구분 (시간)</div><div class="b-section" style="background:#FFF2CC;">성의회관</div><div class="b-section" style="background:#D9EAD3;">의산연</div></div>', unsafe_allow_html=True)
    display_df = df_rt if st.checkbox("🕒 지난 시간표 포함", value=False) else df_rt.iloc[curr_idx:] if curr_idx != -1 else df_rt
    st.dataframe(display_df.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold;' if r.name == curr_idx else '' for _ in r], axis=1), use_container_width=True, hide_index=True)

with tab2:
    # (편성표 로직은 이전과 동일)
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_date = st.date_input("📅 시작일", today, key="tab2_d")
    with c2: focus_u = st.selectbox("👤 강조 대상", ["안 함", "황재업", "김태언", "이태원", "이정석"], key="tab2_u")
    days = st.slider("📆 확인 일수", 7, 60, 31, key="tab2_s")
    cal_data = [{"날짜": f"{(s_date+timedelta(days=i)).strftime('%m/%d')}({['월','화','수','목','금','토','일'][(s_date+timedelta(days=i)).weekday()]})", "조장": get_workers_by_date(s_date+timedelta(days=i))[0], "성희": get_workers_by_date(s_date+timedelta(days=i))[1], "의산A": get_workers_by_date(s_date+timedelta(days=i))[2], "의산B": get_workers_by_date(s_date+timedelta(days=i))[3]} for i in range(days) if get_workers_by_date(s_date+timedelta(days=i))[0]]
    if cal_data: st.dataframe(pd.DataFrame(cal_data).style.map(lambda s: 'background-color: #FFF2CC; font-weight: bold' if focus_u != "안 함" and s == focus_u else ''), use_container_width=True, hide_index=True, height=500)
