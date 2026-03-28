import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

# 한국 표준시(KST) 설정
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()  # 2026-03-28 (토요일)
hr, mn = now_kst.hour, now_kst.minute

# 07:00 교대 로직
if hr < 7:
    logic_date = today_kst - timedelta(days=1)
else:
    logic_date = today_kst

st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] { 
        flex: 1; text-align: center; height: 45px; background-color: #f8f9fa; 
        border: 1px solid #eee; border-radius: 10px 10px 0 0; padding: 5px !important; font-weight: 700; color: #888;
    }
    .stTabs [aria-selected="true"] { background-color: #ffffff !important; color: #2E4077 !important; border-bottom: 3px solid #2E4077 !important; }
    .main-title { text-align: center; font-size: 20px; font-weight: 900; color: #2E4077; margin-bottom: 10px; }
    .date-display { text-align: center; font-size: 18px; color: #333; margin-bottom: 15px; font-weight: 700; }
    .status-msg-box { background: #2E4077; color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 17px; font-weight: 800; margin-bottom: 15px; line-height: 1.5; }
    
    /* 달력 스타일 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; }
    .cal-td { border: 1px solid #eee; height: 65px; vertical-align: top; padding: 0 !important; position: relative; }
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; }
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; }
    .sun { color: #d32f2f !important; } 
    .sat { color: #1976d2 !important; }
    .hi-text { color: white !important; } 
    .today-border { outline: 4px solid #333 !important; outline-offset: -4px; z-index: 10; }
    
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; margin-bottom: 15px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table th { background: #F2F4F7; color: #333; padding: 10px 2px; border: 1px solid #dee2e6; font-size: 11px; font-weight: 800; }
    .custom-table td { border: 1px solid #dee2e6; padding: 12px 2px; }
    .time-col { width: 90px !important; font-weight: 700; background: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 설정 ---
PATTERN_START = date(2025, 1, 1)
NEXT_WORK_DATE = date(2026, 3, 30)
WEEKDAYS_LBL = ['월','화','수','목','금','토','일']

def get_shift_simple(dt):
    return ["C", "A", "B"][(dt - PATTERN_START).days % 3]

def get_workers(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 != 0: return None
    PATTERNS = [
        ["김태언", "이태원", "이정석"], ["김태언", "이정석", "이태원"], 
        ["이정석", "김태언", "이태원"], ["이정석", "이태원", "김태언"], 
        ["이태원", "김태언", "이정석"], ["이태원", "이정석", "김태언"]
    ]
    return ["황재업", PATTERNS[(diff // 3) % 6][0], PATTERNS[(diff // 3) % 6][1], PATTERNS[(diff // 3) % 6][2]]

data_list = [["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"], ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"], ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"], ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"], ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"], ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"], ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"], ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"], ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"], ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"], ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"], ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"], ["06:00", "07:00", "안내실", "정리", "로비", "정리"]]

# --- [3] 화면 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{today_kst.strftime("%Y-%m-%d")}({WEEKDAYS_LBL[today_kst.weekday()]})</div>', unsafe_allow_html=True)
    
    # 휴무 여부 판별 (C조 기준)
    curr_shift = get_shift_simple(logic_date)
    if curr_shift == "C":
        st.markdown('<div class="status-msg-box">⚡ 오늘은 C조 근무일입니다.<br>안전에 유의하세요!</div>', unsafe_allow_html=True)
        names = get_workers(logic_date)
    else:
        st.markdown('<div class="status-msg-box">😴 오늘은 휴무일입니다.<br>편안한 휴식 되세요.</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center; font-weight:700; margin-bottom:10px;">📍 다음 근무는 <b>2026-03-30(월)</b>입니다.</div>', unsafe_allow_html=True)
        names = get_workers(NEXT_WORK_DATE)
    
    h_names = names if names else ["조장", "성희", "당직A", "당직B"]
    rows_html = "".join([f"<tr><td class='time-col'>{r[0]}~{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for r in data_list])
    st.markdown(f'<div class="table-container"><table class="custom-table"><tr><th class="time-col" rowspan="2">시간</th><th colspan="2">성의회관</th><th colspan="2">의과학산업연구원</th></tr><tr><th>{h_names[0]}</th><th>{h_names[1]}</th><th>{h_names[2]}</th><th>{h_names[3]}</th></tr>{rows_html}</table></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="main-title">📅 근무 편성표</div>', unsafe_allow_html=True)
    s_date = st.date_input("조회 시작일", today_kst)
    focus = st.selectbox("🎯 강조할 성함", ["없음", "황재업", "김태언", "이태원", "이정석"])
    t_html = '<div class="table-container"><table class="custom-table"><tr><th>날짜</th><th>조장</th><th>성희</th><th>의산A</th><th>의산B</th></tr>'
    for i in range(30):
        d = s_date + timedelta(days=i)
        ws = get_workers(d)
        if ws:
            wd = d.weekday(); lbl = f"{d.strftime('%m/%d')}({WEEKDAYS_LBL[wd]})"
            cls = "sun" if wd==6 else ("sat" if wd==5 else "")
            t_html += f'<tr><td class="{cls}">{lbl}</td>'
            for w in ws:
                bg = "#FFF2CC" if w == focus else ""
                t_html += f'<td style="background:{bg}; font-weight:700;">{w}</td>'
            t_html += '</tr>'
    st.markdown(t_html + '</table></div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="main-title">🏥 성의교정 근무 달력</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        sel_month = st.selectbox("📅 월 선택", range(1, 13), index=today_kst.month - 1)
    with c2:
        hi_shift = st.selectbox("🎯 강조 조", ["A", "B", "C", "없음"], index=2)
    
    year = 2026
    # 해당 월의 첫 요일(월0~일6)과 마지막 날짜 계산
    first_weekday, last_day = calendar.monthrange(year, sel_month)
    # 일요일 시작(0)으로 인덱스 보정
    start_idx = (first_weekday + 1) % 7
        
    B_COLS, S_COLS = {"A":"#FFE0B2","B":"#FFCDD2","C":"#BBDEFB"}, {"A":"#FB8C00","B":"#E53935","C":"#1E88E5"}
    
    cal_html = f"<div style='text-align:center; font-weight:900; margin-bottom:10px;'>{year}년 {sel_month}월</div>"
    cal_html += "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr><tr>"
    
    # 시작 빈칸
    for _ in range(start_idx):
        cal_html += "<td class='cal-td'></td>"
        
    curr_col = start_idx
    for day in range(1, last_day + 1):
        if curr_col == 7:
            cal_html += "</tr><tr>"
            curr_col = 0
            
        d_obj = date(year, sel_month, day)
        s = get_shift_simple(d_obj)
        is_hi = (hi_shift == s)
        
        s_bg = S_COLS[s] if is_hi else B_COLS[s]
        d_bg = S_COLS[s] if is_hi else "white"
        td_cls = "today-border" if d_obj == today_kst else ""
        txt_cls = "hi-text" if is_hi else ("sun" if curr_col == 0 else "sat" if curr_col == 6 else "")
        
        cal_html += f"""
        <td class='cal-td {td_cls}' style='background:{s_bg};'>
            <div class='cal-date-part {txt_cls}' style='background:{d_bg};'>{day}</div>
            <div class='cal-shift-part {txt_cls}'>{s}</div>
        </td>
        """
        curr_col += 1
        
    while curr_col < 7:
        cal_html += "<td class='cal-td'></td>"
        curr_col += 1
        
    st.markdown(cal_html + "</tr></table>", unsafe_allow_html=True)
