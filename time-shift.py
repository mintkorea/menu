import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date() 
hr = now_kst.hour

# 07:00 교대 로직
logic_date = today_kst - timedelta(days=1) if hr < 7 else today_kst

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
    .month-title { text-align: center; font-weight: 900; font-size: 18px; margin: 25px 0 10px 0; color: #333; border-top: 2px solid #eee; padding-top: 15px; }
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; margin-bottom: 10px; background: white; }
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
def get_shift_simple(dt):
    return ["C", "A", "B"][(dt - PATTERN_START).days % 3]

def get_workers(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 != 0: return None
    PATTERNS = [["김태언", "이태원", "이정석"], ["김태언", "이정석", "이태원"], ["이정석", "김태언", "이태원"], ["이정석", "이태원", "김태언"], ["이태원", "김태언", "이정석"], ["이태원", "이정석", "김태언"]]
    return ["황재업", PATTERNS[(diff // 3) % 6][0], PATTERNS[(diff // 3) % 6][1], PATTERNS[(diff // 3) % 6][2]]

data_list = [["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"], ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"], ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"], ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"], ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"], ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"], ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"], ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"], ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"], ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"], ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"], ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"], ["06:00", "07:00", "안내실", "정리", "로비", "정리"]]

tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    w_lbl = ['월','화','수','목','금','토','일']
    st.markdown(f'<div class="date-display">{today_kst.strftime("%Y-%m-%d")}({w_lbl[today_kst.weekday()]})</div>', unsafe_allow_html=True)
    
    if get_shift_simple(logic_date) == "C":
        st.markdown('<div class="status-msg-box">⚡ 오늘은 C조 근무일입니다.</div>', unsafe_allow_html=True)
        names = get_workers(logic_date)
    else:
        st.markdown('<div class="status-msg-box">😴 오늘은 휴무일입니다.</div>', unsafe_allow_html=True)
        names = get_workers(date(2026, 3, 30))
    
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
            wd = d.weekday(); lbl = f"{d.strftime('%m/%d')}({w_lbl[wd]})"
            cls = "sun" if wd==6 else ("sat" if wd==5 else "")
            t_html += f'<tr><td class="{cls}">{lbl}</td>'
            for w in ws:
                bg = "#FFF2CC" if w == focus else ""
                t_html += f'<td style="background:{bg}; font-weight:700;">{w}</td>'
            t_html += '</tr>'
    st.markdown(t_html + '</table></div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="main-title">🏥 성의교정 근무 달력</div>', unsafe_allow_html=True)
    
    options = ["선택 없음", "A", "B", "C"]
    hi = st.selectbox("🎯 강조 조 선택", options, index=3) # C조 기본 강조
    
    B_COLS, S_COLS = {"A":"#FFE0B2","B":"#FFCDD2","C":"#BBDEFB"}, {"A":"#FB8C00","B":"#E53935","C":"#1E88E5"}
    
    # [핵심] 일요일 시작 설정 (firstweekday=6)
    cal_obj = calendar.Calendar(firstweekday=6)
    full_html = ""
    curr = today_kst.replace(day=1)
    
    for _ in range(3): # 3개월치만 먼저 표시 (조절 가능)
        y, m = curr.year, curr.month
        month_weeks = cal_obj.monthdays2calendar(y, m)
        
        full_html += f"<div class='month-title'>{y}년 {m}월</div>"
        full_html += "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        
        for week in month_weeks:
            full_html += "<tr>"
            for day, day_idx in week:
                if day == 0:
                    full_html += "<td class='cal-td'></td>"
                else:
                    d_obj = date(y, m, day)
                    s = get_shift_simple(d_obj)
                    is_hi = (hi == s)
                    
                    s_bg = S_COLS[s] if is_hi else B_COLS[s]
                    d_bg = S_COLS[s] if is_hi else "white"
                    td_cls = "today-border" if d_obj == today_kst else ""
                    # day_idx는 0(일) ~ 6(토)
                    txt_cls = "hi-text" if is_hi else ("sun" if day_idx == 0 else "sat" if day_idx == 6 else "")
                    
                    full_html += f"""
                    <td class='cal-td {td_cls}' style='background:{s_bg};'>
                        <div class='cal-date-part {txt_cls}' style='background:{d_bg};'>{day}</div>
                        <div class='cal-shift-part {txt_cls}'>{s}</div>
                    </td>
                    """
            full_html += "</tr>"
        full_html += "</table>"
        # 다음 달 계산
        if m == 12: curr = date(y+1, 1, 1)
        else: curr = date(y, m+1, 1)
        
    st.markdown(full_html, unsafe_allow_html=True) # <- 여기가 핵심! 렌더링 허용
