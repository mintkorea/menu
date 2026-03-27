import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 (사용자 원본 유지) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 2px; display: flex; width: 100%; justify-content: space-around; }
    .stTabs [data-baseweb="tab"] {
        flex: 1; text-align: center; height: 40px; background-color: #f0f2f6; border-radius: 5px 5px 0 0;
        padding: 0px !important; font-weight: 800; font-size: 12px !important;
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    .main-title { text-align: center; font-size: 18px; font-weight: 900; color: #2E4077; margin-top: 5px; }
    .date-display { text-align: center; font-size: 14px; color: #666; margin-bottom: 10px; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-bottom: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 8px 2px; text-align: center; background: white; }
    .worker-name { font-size: 14px; font-weight: 800; color: #333; }
    .status-val { font-size: 16px; font-weight: 900; color: #C04B41; }
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 5px; margin-bottom: 20px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table td { border: 1px solid #dee2e6; padding: 8px 2px; }
    
    /* 달력 스타일 수정: 3pt 차이 및 하이라이트 배색 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; margin-bottom: 35px; }
    .cal-td { border: 1px solid #eee; height: 55px; vertical-align: top; padding: 0 !important; }
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; }
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; } /* 3pt 차이 */
    .sun { color: #d32f2f !important; }
    .sat { color: #1976d2 !important; }
    .hi-text { color: white !important; }
    .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 (사용자 규칙 정교화) ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
PATTERN_START = date(2026, 3, 9)

def get_workers(target_date):
    """사용자 규칙: 김태언(2)->이정석(2)->이태원(2) 회관 순환 / 입사순 당직배정"""
    hall_order = ["김태언", "이정석", "이태원"] 
    seniority = ["김태언", "이태원", "이정석"] 
    diff = (target_date - PATTERN_START).days
    cycle = diff % 6
    hall_worker = hall_order[cycle // 2]
    others = [p for p in seniority if p != hall_worker]
    dj_a, dj_b = (others[0], others[1]) if cycle % 2 == 0 else (others[1], others[0])
    return "황재업", hall_worker, dj_a, dj_b

def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    return ["C", "A", "B"][diff % 3]

# --- [3] 탭 구성 (원본 구조 유지) ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    # 시간 적용: 오전 7시 기준 (원본 로직 보완)
    is_working = now_kst.hour >= 7
    work_date = today_kst if is_working else today_kst - timedelta(days=1)
    names = get_workers(work_date)
    
    # 가~라. 시간대별 메시지 표출 (카드 영역)
    curr_m = now_kst.hour * 60 + now_kst.minute
    if not is_working:
        if curr_m < 400: # 00:00~06:40
            st.markdown('<div class="status-card" style="grid-column: span 2; padding:20px;">오늘 하루도 보람차고 즐거운 하루가 되도록 합시다.</div>', unsafe_allow_html=True)
        elif 400 <= curr_m < 420: # 06:40~07:00
            st.markdown('<div class="status-card" style="grid-column: span 2; padding:20px;">카드 표출 및 근무 준비중...</div>', unsafe_allow_html=True)
        else: # 근무 종료 후 교대 전
            st.markdown('<div class="status-card" style="grid-column: span 2; padding:20px;">오늘도 수고하셨습니다. 다음 근무 때 뵙겠습니다.</div>', unsafe_allow_html=True)
    else:
        # 마. 실시간 카드 표출 (원본 data_list 활용)
        data_list = [["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"], ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"], ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"], ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"], ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"], ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"], ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"], ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"], ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"], ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"], ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"], ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"]]
        def find_idx(dt):
            m = dt.hour * 60 + dt.minute
            if dt.hour < 7: m += 1440
            for i, r in enumerate(data_list):
                sh, sm = map(int, r[0].split(':')); eh, em = map(int, r[1].split(':'))
                s, e = (sh+24 if sh<7 else sh)*60+sm, (eh+24 if (eh<7 or (eh==7 and em==0)) and sh!=7 else eh)*60+em
                if s <= m < e: return i
            return -1
        idx = find_idx(now_kst)
        st.markdown(f'''<div class="status-container">
            <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">{data_list[idx][2] if idx!=-1 else "-"}</div></div>
            <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">{data_list[idx][3] if idx!=-1 else "-"}</div></div>
            <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">{data_list[idx][4] if idx!=-1 else "-"}</div></div>
            <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">{data_list[idx][5] if idx!=-1 else "-"}</div></div>
        </div>''', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="main-title">📅 근무 편성표</div>', unsafe_allow_html=True)
    # 나. 슬라이더 -12~+12개월 (원본 기능 보완)
    offset = st.slider("조회 월 변경", -12, 12, 0)
    base_month = (today_kst.replace(day=1) + timedelta(days=offset * 31)).replace(day=1)
    focus = st.selectbox("강조", ["없음", "황재업", "김태언", "이정석", "이태원"])
    
    t_html = '<div class="table-container"><table class="custom-table"><tr style="background:#f8f9fa;font-weight:800;"><td>날짜</td><td>조장</td><td>회관</td><td>당직A</td><td>당직B</td></tr>'
    for d in range(calendar.monthrange(base_month.year, base_month.month)[1]):
        curr = base_date = base_month + timedelta(days=d)
        w = get_workers(curr)
        wd = curr.weekday(); lbl = f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})"
        cls = "sun" if wd==6 else ("sat" if wd==5 else "")
        t_html += f'<tr><td class="{cls}">{lbl}</td>'
        for n in w:
            bg = "background:#FFF2CC;" if n == focus else ""
            t_html += f'<td style="{bg}">{n}</td>'
        t_html += '</tr>'
    st.markdown(t_html + '</table></div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="main-title">🏥 근무달력 (12개월)</div>', unsafe_allow_html=True)
    hi = st.radio("강조 조", ["A", "B", "C"], index=2, horizontal=True)
    L_COLS, D_COLS = {"A":"#FFE0B2","B":"#FFCDD2","C":"#BBDEFB"}, {"A":"#FB8C00","B":"#E53935","C":"#1E88E5"}
    
    curr_cal = today_kst.replace(day=1)
    for _ in range(12):
        y, m = curr_cal.year, curr_cal.month
        st.write(f"**{y}년 {m}월**")
        cal = calendar.monthcalendar(y, m)
        cal_html = '<table class="cal-table"><tr><th class="sun">일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class="sat">토</th></tr>'
        for week in cal:
            cal_html += "<tr>"
            for i, day in enumerate(week):
                if day == 0: cal_html += "<td class='cal-td'></td>"
                else:
                    d_obj = date(y, m, day); s = get_shift_simple(d_obj); is_hi = (hi == s)
                    # 하이라이트 시 날짜 구역까지 배색 확대
                    d_bg = D_COLS[s] if is_hi else "white"
                    s_bg = D_COLS[s] if is_hi else L_COLS[s]
                    d_cls = ("hi-text" if is_hi else ("sun" if i==0 else "sat" if i==6 else ""))
                    td_cls = "today-border" if d_obj == today_kst else ""
                    cal_html += f'<td class="cal-td {td_cls}"><div class="cal-date-part {d_cls}" style="background:{d_bg};">{day}</div><div class="cal-shift-part {"hi-text" if is_hi else ""}" style="background:{s_bg};">{s}</div></td>'
            cal_html += "</tr>"
        st.markdown(cal_html + "</table>", unsafe_allow_html=True)
        curr_cal = (curr_cal + timedelta(days=32)).replace(day=1)
