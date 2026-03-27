import streamlit as st
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

# [필수] 한국 표준시(KST) 고정
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
hr, mn = now_kst.hour, now_kst.minute

# 07:00 교대 로직: 새벽 07시 이전이면 '실질적 전날' 조로 판단
logic_date = today_kst - timedelta(days=1) if hr < 7 else today_kst

st.markdown("""
    <style>
    .block-container { padding-top: 50px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; font-weight: 700; }
    .main-title { text-align: center; font-size: 20px; font-weight: 900; color: #2E4077; }
    .status-msg-box { background: #2E4077; color: white; padding: 20px; border-radius: 15px; text-align: center; font-weight: 800; margin-bottom: 15px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; }
    .custom-table th { background: #F2F4F7; border: 1px solid #dee2e6; padding: 8px; }
    .custom-table td { border: 1px solid #dee2e6; padding: 10px; }
    .row-highlight { background-color: #FFE5E5 !important; font-weight: 900; border: 2px solid #E53935; }
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    .cal-td { border: 1px solid #eee; height: 60px; vertical-align: top; }
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; }
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; }
    .sun { color: #d32f2f; } .sat { color: #1976d2; }
    .hi-text { color: white !important; } .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 설정 ---
PATTERN_START = date(2026, 3, 9) # C조 시작 기준일

def get_shift_simple(dt):
    return ["C", "A", "B"][(dt - PATTERN_START).days % 3]

def get_workers(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 != 0: return None
    P = [["김태언", "이태원", "이정석"], ["김태언", "이정석", "이태원"], ["이정석", "김태언", "이태원"], ["이정석", "이태원", "김태언"], ["이태원", "김태언", "이정석"], ["이태원", "이정석", "김태언"]]
    return ["황재업", P[(diff // 3) % 6][0], P[(diff // 3) % 6][1], P[(diff // 3) % 6][2]]

data_list = [["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"], ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"], ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"], ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"], ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"], ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"], ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"], ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"], ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"], ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"], ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"], ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"], ["06:00", "07:00", "안내실", "정리", "로비", "정리"]]

# --- [3] 화면 탭 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown(f'<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    w_list = ['월','화','수','목','금','토','일']
    st.markdown(f'<div style="text-align:center; font-weight:700;">{now_kst.strftime("%Y-%m-%d")}({w_list[now_kst.weekday()]}) {now_kst.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    
    curr_logic_shift = get_shift_simple(logic_date)
    is_c_day = (curr_logic_shift == "C")
    status_msg = "😴 오늘은 휴무일입니다. 편안한 휴식 되세요."
    highlight_idx = -1

    if is_c_day:
        if 6 <= hr < 7:
            status_msg = "수고하셨습니다. 교대를 준비하십시오." if mn < 40 else "근무교대 시간입니다."
            highlight_idx = 24
        elif hr == 7: status_msg = "✨ 안전하게 퇴근하십시오!"
        else: status_msg = "🛡️ 현재 C조 근무 중입니다."
        h_date = today_kst
    else:
        h_date = date(2026, 3, 30) # 휴무 시 다음 C조 투입일

    st.markdown(f'<div class="status-msg-box">{status_msg}</div>', unsafe_allow_html=True)
    
    ws = get_workers(h_date) or ["조장", "성희", "당직A", "당직B"]
    rows_html = "".join([f"<tr{' class=\"row-highlight\"' if i==highlight_idx else ''}><td>{r[0]}~{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(data_list)])
    st.markdown(f'<table class="custom-table"><tr><th>시간</th><th>{ws[0]}</th><th>{ws[1]}</th><th>{ws[2]}</th><th>{ws[3]}</th></tr>{rows_html}</table>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="main-title">🏥 성의교정 근무 달력</div>', unsafe_allow_html=True)
    
    # [요일 고정 핵심] 일요일 시작(6)으로 캘린더 생성
    c = calendar.Calendar(firstweekday=6)
    hi = st.selectbox("🎯 강조 조", ["A", "B", "C"], index=["A", "B", "C"].index(curr_logic_shift))
    
    B_COLS, S_COLS = {"A":"#FFE0B2","B":"#FFCDD2","C":"#BBDEFB"}, {"A":"#FB8C00","B":"#E53935","C":"#1E88E5"}
    cal_date = today_kst.replace(day=1)
    
    for _ in range(2): # 2개월치 표시
        y, m = cal_date.year, cal_date.month
        st.markdown(f"<div style='text-align:center; font-weight:900; margin-top:10px;'>{y}년 {m}월</div>", unsafe_allow_html=True)
        html = "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        
        for week in c.monthdayscalendar(y, m):
            html += "<tr>"
            for i, day in enumerate(week):
                if day == 0: html += "<td class='cal-td'></td>"
                else:
                    d_obj = date(y, m, day)
                    s = get_shift_simple(d_obj)
                    is_hi = (hi == s)
                    s_bg = S_COLS[s] if is_hi else B_COLS[s]
                    d_bg = S_COLS[s] if is_hi else "white"
                    td_cls = "today-border" if d_obj == today_kst else ""
                    txt_cls = "hi-text" if is_hi else ("sun" if i==0 else "sat" if i==6 else "")
                    html += f"<td class='cal-td {td_cls}' style='background:{s_bg};'><div class='cal-date-part {txt_cls}' style='background:{d_bg};'>{day}</div><div class='cal-shift-part {txt_cls}'>{s}</div></td>"
            html += "</tr>"
        st.markdown(html + "</table>", unsafe_allow_html=True)
        cal_date = (cal_date + timedelta(days=32)).replace(day=1)
