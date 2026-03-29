import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 2px; display: flex; width: 100%; justify-content: space-around; }
    .stTabs [data-baseweb="tab"] {
        flex: 1; text-align: center; height: 40px; background-color: #f0f2f6; 
        border-radius: 5px 5px 0 0; font-weight: 800; font-size: 13px !important;
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    
    .main-title { text-align: center; font-size: 20px; font-weight: 900; color: #2E4077; margin-top: 10px; }
    .date-display { text-align: center; font-size: 15px; color: #666; margin-bottom: 15px; }

    /* 2x2 근무 카드 스타일 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
    .status-card { border: 2px solid #2E4077; border-radius: 12px; padding: 12px 5px; text-align: center; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .worker-name { font-size: 14px; font-weight: 700; color: #555; margin-bottom: 4px; }
    .status-val { font-size: 18px; font-weight: 900; color: #E53935; }
    
    /* 메시지 박스 */
    .info-msg { background: #f8f9fa; border-left: 5px solid #2E4077; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 15px; font-weight: 700; }

    /* 테이블 스타일 */
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; margin-bottom: 20px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table th, .custom-table td { border: 1px solid #dee2e6; padding: 10px 2px; }
    .row-highlight { background-color: #FFE5E5 !important; font-weight: 900 !important; color: #D32F2F; }
    
    /* 달력 스타일 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; margin-bottom: 30px; }
    .cal-td { border: 1px solid #eee; height: 60px; vertical-align: top; padding: 0 !important; }
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 12px; }
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; }
    .sun { color: #d32f2f !important; } .sat { color: #1976d2 !important; }
    .hi-text { color: white !important; } .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 및 데이터 ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
PATTERN_START = date(2026, 3, 9)
NEXT_WORK_DATE = date(2026, 3, 30)

def get_workers(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 != 0: return None
    PATTERNS = [
        ["김태언", "이태원", "이정석"], ["김태언", "이정석", "이태원"], 
        ["이정석", "김태언", "이태원"], ["이정석", "이태원", "김태언"], 
        ["이태원", "김태언", "이정석"], ["이태원", "이정석", "김태언"]
    ]
    p_idx = (diff // 3) % 6
    return ["황재업", PATTERNS[p_idx][0], PATTERNS[p_idx][1], PATTERNS[p_idx][2]]

def get_shift_simple(dt):
    return ["C", "A", "B"][(dt - PATTERN_START).days % 3]

data_list = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"],
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"],
    ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"],
    ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"],
    ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"],
    ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"],
    ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"],
    ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"],
    ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"],
    ["06:00", "07:00", "안내실", "정리", "로비", "정리"]
]

# --- [3] 화면 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    # 근무 판정 로직 (07시 교대 기준)
    hr = now_kst.hour
    logic_date = today_kst if hr >= 7 else (today_kst - timedelta(days=1))
    is_c_day = (get_shift_simple(logic_date) == "C")
    
    # 인덱스 찾기 함수
    def find_idx(dt):
        m = dt.hour * 60 + dt.minute
        if dt.hour < 7: m += 1440
        for i, r in enumerate(data_list):
            sh, sm = map(int, r[0].split(':')); eh, em = map(int, r[1].split(':'))
            s_val = (sh+24 if sh<7 else sh)*60+sm
            e_val = (eh+24 if (eh<7 or (eh==7 and em==0)) and sh!=7 else eh)*60+em
            if s_val <= m < e_val: return i
        return -1

    idx = find_idx(now_kst) if is_c_day else -1
    
    if is_c_day and idx != -1:
        # 근무 중: 2x2 카드 출력
        names = get_workers(logic_date)
        st.markdown(f'''<div class="status-container">
            <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">{data_list[idx][2]}</div></div>
            <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">{data_list[idx][3]}</div></div>
            <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">{data_list[idx][4]}</div></div>
            <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">{data_list[idx][5]}</div></div>
        </div>''', unsafe_allow_html=True)
    else:
        # 휴무 또는 대기 중
        msg = "🗓️ 오늘은 휴무일입니다. 충분한 휴식 되세요!"
        if today_kst == NEXT_WORK_DATE and hr < 7:
            msg = "⌛ 곧 근무 투입 예정입니다. (07:00 시작)"
        st.markdown(f'<div class="info-msg">{msg}</div>', unsafe_allow_html=True)
        if not is_c_day:
            st.markdown(f'<div style="text-align:center; margin-bottom:15px;">📍 다음 근무일: <b>{NEXT_WORK_DATE}</b></div>', unsafe_allow_html=True)

    # 근무 테이블 표시
    display_date = logic_date if is_c_day else NEXT_WORK_DATE
    h_names = get_workers(display_date) or ["조장", "성희", "의산A", "의산B"]
    
    rows_html = ""
    for i, r in enumerate(data_list):
        cls = ' class="row-highlight"' if i == idx else ''
        rows_html += f"<tr {cls}><td>{r[0]}~{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>"
    
    st.markdown(f"""
    <div class="table-container">
        <table class="custom-table">
            <tr style="background:#f8f9fa; font-weight:800;">
                <th style="width:25%">시간</th><th>{h_names[0]}</th><th>{h_names[1]}</th><th>{h_names[2]}</th><th>{h_names[3]}</th>
            </tr>
            {rows_html}
        </table>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    # (생략: 기존 편성표 로직 유지)
    st.markdown('<div class="main-title">📅 근무 편성표</div>', unsafe_allow_html=True)
    s_date = st.date_input("조회 시작일", today_kst)
    t_html = '<div class="table-container"><table class="custom-table"><tr style="background:#f8f9fa;"><td>날짜</td><td>조장</td><td>성희</td><td>의산A</td><td>의산B</td></tr>'
    for i in range(20):
        d = s_date + timedelta(days=i)
        ws = get_workers(d)
        if ws:
            wd = d.weekday(); lbl = f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})"
            t_html += f'<tr><td>{lbl}</td><td>{ws[0]}</td><td>{ws[1]}</td><td>{ws[2]}</td><td>{ws[3]}</td></tr>'
    st.markdown(t_html + '</table></div>', unsafe_allow_html=True)

with tab3:
    # (생략: 기존 근무달력 로직 유지)
    st.markdown('<div class="main-title">🏥 성의교정 근무 달력</div>', unsafe_allow_html=True)
    hi = st.selectbox("강조할 조", ["A", "B", "C"], index=2)
    B_COLS, S_COLS = {"A":"#FFE0B2","B":"#FFCDD2","C":"#BBDEFB"}, {"A":"#FB8C00","B":"#E53935","C":"#1E88E5"}
    cal_html = ""; curr = today_kst.replace(day=1)
    for _ in range(3): # 3개월만 표시
        y, m = curr.year, curr.month; cal = calendar.monthcalendar(y, m)
        cal_html += f"<div style='text-align:center; font-weight:bold;'>{y}년 {m}월</div><table class='cal-table'>"
        for week in cal:
            cal_html += "<tr>"
            for i, day in enumerate(week):
                if day == 0: cal_html += "<td></td>"
                else:
                    d_obj = date(y, m, day); s = get_shift_simple(d_obj); is_hi = (hi == s)
                    bg = S_COLS[s] if is_hi else B_COLS[s]
                    cal_html += f"<td class='cal-td' style='background:{bg}'><div class='cal-date-part'>{day}</div><div class='cal-shift-part'>{s}</div></td>"
            cal_html += "</tr>"
        cal_html += "</table>"; curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
    st.markdown(cal_html, unsafe_allow_html=True)
