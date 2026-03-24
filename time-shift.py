import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (완전 통합형 스타일) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 15px !important; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 카드 디자인 (폰트 확대 반영) */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 12px; padding: 15px 5px; 
        text-align: center; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .worker-name { font-size: 17px !important; font-weight: 700; color: #555; margin-bottom: 5px; }
    .status-val { font-size: 21px !important; font-weight: 900; color: #C04B41; }
    
    /* 휴무 안내 카드 */
    .off-card {
        grid-column: span 2; border-radius: 12px; padding: 25px 15px;
        text-align: center; background: #FFF5F5; border: 2px solid #C04B41;
        margin-bottom: 15px;
    }
    .off-title { font-size: 26px !important; font-weight: 900; color: #C04B41; margin-bottom: 10px; }
    .next-info { font-size: 16px; font-weight: 700; color: #333; line-height: 1.6; }

    /* 통합 테이블: 헤더와 본문을 하나로 묶음 */
    .table-wrapper { width: 100%; overflow-x: auto; margin-top: 10px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: center; background: white; }
    .custom-table th, .custom-table td { border: 1px solid #dee2e6; padding: 8px 1px; }
    
    /* 건물 헤더 스타일 */
    .b-header-row { font-weight: bold; font-size: 14px; }
    .col-time { background: #f8f9fa; width: 22%; }
    .col-seonghui { background: #FFF2CC; width: 39%; }
    .col-uisan { background: #D9EAD3; width: 39%; }
    
    /* 행 강조 */
    .highlight-row { background-color: #FFE5E5 !important; font-weight: bold; color: #d00; }
    
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

today = now.date()
is_today_work = get_workers_by_date(today)[0] is not None
is_yesterday_work = get_workers_by_date(today - timedelta(days=1))[0] is not None

# 휴무 판별
is_off_display = (is_yesterday_work and not is_today_work and now.hour >= 7) or (not is_yesterday_work and not is_today_work)

# 다음 근무일 계산
next_work_date = today
while get_workers_by_date(next_work_date)[0] is None:
    next_work_date += timedelta(days=1)
n_j, n_s, n_a, n_b = get_workers_by_date(next_work_date)

# 현재 근무 데이터 기준일
work_date = (today - timedelta(days=1)) if now.hour < 7 else today
jojang, seonghui, uisanA, uisanB = get_workers_by_date(work_date)
if jojang is None: jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

# --- [3] 시간표 데이터 정의 ---
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

def get_current_idx(dt):
    curr_m = dt.hour * 60 + dt.minute
    if dt.hour < 7: curr_m += 1440
    for i, row in enumerate(combined_data):
        sh, sm = map(int, row[0].split(':'))
        eh, em = map(int, row[1].split(':'))
        s_m, e_m = sh * 60 + sm, eh * 60 + em
        if sh < 7: s_m += 1440
        if eh < 7 or (eh == 7 and em == 0 and sh < 7): e_m += 1440
        if s_m <= curr_m < e_m: return i
    return -1

curr_idx = get_current_idx(now)

# --- [4] UI 출력 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    # 상단 카드 영역
    if is_off_display:
        st.markdown(f'<div class="off-card"><div class="off-title">오늘은 휴무입니다.</div><div class="next-info">다음 근무는 {next_work_date.strftime("%m월 %d일")}입니다.<br>성의회관 {n_j}, {n_s}<br>의 산 연 {n_a}, {n_b}</div></div>', unsafe_allow_html=True)
    elif is_today_work and now.hour < 7:
        st.markdown('<div class="msg-card-full" style="background:#F0FDF4; color:#166534;">오늘도 즐겁고 보람된<br>하루가 되도록 합시다.</div>', unsafe_allow_html=True)
    elif is_yesterday_work and (now.hour == 6 and now.minute >= 40):
        st.markdown('<div class="msg-card-full" style="background:#EEF2FF; color:#2E4077;">수고하셨습니다.<br>다음 근무 때 뵙겠습니다.</div>', unsafe_allow_html=True)
    elif curr_idx != -1:
        c_row = combined_data[curr_idx]
        st.markdown(f'<div class="status-container"><div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{c_row[2]}</div></div><div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{c_row[3]}</div></div><div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{c_row[4]}</div></div><div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{c_row[5]}</div></div></div>', unsafe_allow_html=True)

    show_all = st.checkbox("🕒 지난 시간표 포함 (전체 보기)", value=False)

    # [수정 핵심] 통합 HTML 테이블 렌더링
    html_table = f"""
    <div class="table-wrapper">
        <table class="custom-table">
            <tr class="b-header-row">
                <th colspan="2" class="col-time">구분 (시간)</th>
                <th colspan="2" class="col-seonghui">성의회관</th>
                <th colspan="2" class="col-uisan">의산연</th>
            </tr>
            <tr style="background:#eee; font-weight:bold;">
                <td>From</td><td>To</td><td>{jojang}</td><td>{seonghui}</td><td>{uisanA}</td><td>{uisanB}</td>
            </tr>
    """
    
    start_i = 0 if show_all or curr_idx == -1 else curr_idx
    for i in range(start_i, len(combined_data)):
        r = combined_data[i]
        row_cls = "highlight-row" if i == curr_idx else ""
        html_table += f"""
            <tr class="{row_cls}">
                <td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td>
            </tr>
        """
    html_table += "</table></div>"
    
    st.markdown(html_table, unsafe_allow_html=True)

with tab2:
    # 편성표는 기존 로직 유지
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    # ... (생략된 기존 편성표 코드)
