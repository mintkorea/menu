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
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; height: 40px; background-color: #f0f2f6; border-radius: 5px 5px 0 0; padding: 0px !important; font-weight: 800; font-size: 12px !important; }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    .main-title { text-align: center; font-size: 18px; font-weight: 900; color: #2E4077; margin-top: 5px; }
    .date-display { text-align: center; font-size: 14px; color: #666; margin-bottom: 10px; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-bottom: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 8px 2px; text-align: center; background: white; min-height: 60px; display: flex; flex-direction: column; justify-content: center; }
    .worker-name { font-size: 13px; font-weight: 800; color: #333; }
    .status-val { font-size: 15px; font-weight: 900; color: #C04B41; }
    .msg-card { grid-column: span 2; padding: 20px; font-weight: 800; color: #2E4077; border: 2px solid #2E4077; background: #f9f9f9; font-size: 14px; text-align: center; }
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 5px; margin-bottom: 20px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table td { border: 1px solid #dee2e6; padding: 8px 2px; }
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; margin-bottom: 35px; }
    .cal-td { border: 1px solid #eee; height: 60px; vertical-align: top; padding: 0 !important; }
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 15px; background: white; }
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 12px; }
    .sun { color: #d32f2f !important; } .sat { color: #1976d2 !important; }
    .hi-text { color: white !important; font-weight: 900; }
    .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 (근무 규칙 절대 준수) ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()

# 기준일 (김태언 회관근무 시작일 예시)
PATTERN_START = date(2026, 3, 9) 

def get_workers(target_date):
    """
    1) 조장: 황재업 (회관 고정)
    2) 회관 순서: 김태언(2회) -> 이정석(2회) -> 이태원(2회) (6일 주기)
    3) 당직 A/B: 나머지 2명 중 선임(입사순: 김태언 > 이태원 > 이정석) 순서
       - 첫째날 선임이 당직A, 둘째날 선임이 당직B
    """
    hall_order = ["김태언", "이정석", "이태원"] # 회관 도는 순서 (사용자 지정)
    seniority = ["김태언", "이태원", "이정석"] # 입사순 (당직 A/B 결정용)
    
    diff = (target_date - PATTERN_START).days
    cycle = diff % 6
    
    # 1. 회관 근무자 결정
    hall_worker = hall_order[cycle // 2]
    
    # 2. 당직 A/B 결정 (나머지 2명을 입사순으로 정렬)
    others = [p for p in seniority if p != hall_worker]
    # others[0]이 더 선임
    if cycle % 2 == 0: # 첫 번째 날
        dj_a, dj_b = others[0], others[1]
    else: # 두 번째 날
        dj_a, dj_b = others[1], others[0] # 선임이 당직B로 이동
        
    return "황재업", hall_worker, dj_a, dj_b

def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    return ["C", "A", "B"][diff % 3]

# --- [3] 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

# 1. 근무 현황판
with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    # 오전 7시 기준 투입/철수 로직
    is_work_active = now_kst.hour >= 7
    display_date = today_kst if is_work_active else today_kst - timedelta(days=1)
    names = get_workers(display_date)
    
    total_min = now_kst.hour * 60 + now_kst.minute
    
    # 가~라 메시지 및 카드 표출
    if not is_work_active:
        if 0 <= total_min < 400: # 00:00 ~ 06:40
            st.markdown('<div class="status-container"><div class="msg-card">오늘 하루도 보람차고 즐거운 하루가 되도록 합시다.</div></div>', unsafe_allow_html=True)
        elif 400 <= total_min < 420: # 06:40 ~ 07:00
            st.markdown('<div class="status-container"><div class="msg-card">카드 표출 및 근무 준비중...</div></div>', unsafe_allow_html=True)
        else: # 07:00 이전 (전일 근무 종료 시점)
            st.markdown('<div class="status-container"><div class="msg-card">오늘도 수고하셨습니다. 다음 근무 때 뵙겠습니다.</div></div>', unsafe_allow_html=True)
    else:
        # 실시간 근무자 카드 (마)
        st.markdown(f'''<div class="status-container">
            <div class="status-card"><div class="worker-name">성의(조장): {names[0]}</div><div class="status-val">보안실</div></div>
            <div class="status-card"><div class="worker-name">성의(회관): {names[1]}</div><div class="status-val">로비</div></div>
            <div class="status-card"><div class="worker-name">의산연(A): {names[2]}</div><div class="status-val">순찰</div></div>
            <div class="status-card"><div class="worker-name">의산연(B): {names[3]}</div><div class="status-val">휴게</div></div>
        </div>''', unsafe_allow_html=True)

# 2. 근무 편성표
with tab2:
    st.markdown('<div class="main-title">📅 C조 근무 편성표</div>', unsafe_allow_html=True)
    # 슬라이더 -12 ~ +12개월
    month_move = st.slider("조회 월 선택", -12, 12, 0)
    # 날짜 계산: 오늘로부터 n개월 후의 1일
    target_month = (today_kst.replace(day=1) + timedelta(days=month_move * 31)).replace(day=1)
    
    focus_name = st.selectbox("본인 강조", ["없음", "황재업", "김태언", "이태원", "이정석"])
    
    t_html = '<div class="table-container"><table class="custom-table"><tr style="background:#f8f9fa;font-weight:800;"><td>날짜</td><td>조장</td><td>회관</td><td>당직A</td><td>당직B</td></tr>'
    for d in range(calendar.monthrange(target_month.year, target_month.month)[1]):
        curr = target_month + timedelta(days=d)
        w = get_workers(curr)
        wd = curr.weekday()
        cls = "sun" if wd == 6 else ("sat" if wd == 5 else "")
        t_html += f'<tr><td class="{cls}">{curr.strftime("%m/%d")}({["월","화","수","목","금","토","일"][wd]})</td>'
        for n in w:
            bg = "background:#D1E7DD;" if n == focus_name else ""
            t_html += f'<td style="{bg}">{n}</td>'
        t_html += '</tr>'
    st.markdown(t_html + "</table></div>", unsafe_allow_html=True)

# 3. 근무 달력
with tab3:
    st.markdown('<div class="main-title">🏥 12개월 근무 달력</div>', unsafe_allow_html=True)
    hi_group = st.radio("강조 근무조", ["A", "B", "C"], index=2, horizontal=True)
    B_COLS, S_COLS = {"A":"#FFE0B2","B":"#FFCDD2","C":"#BBDEFB"}, {"A":"#FB8C00","B":"#E53935","C":"#1E88E5"}
    
    curr_cal_date = today_kst.replace(day=1)
    for _ in range(12):
        st.write(f"**{curr_cal_date.year}년 {curr_cal_date.month}월**")
        cal = calendar.monthcalendar(curr_cal_date.year, curr_cal_date.month)
        cal_html = '<table class="cal-table"><tr><th class="sun">일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class="sat">토</th></tr>'
        for week in cal:
            cal_html += '<tr>'
            for i, day in enumerate(week):
                if day == 0: cal_html += '<td class="cal-td"></td>'
                else:
                    d_obj = date(curr_cal_date.year, curr_cal_date.month, day)
                    shift = get_shift_simple(d_obj)
                    is_hi = (shift == hi_group)
                    bg = S_COLS[shift] if is_hi else B_COLS[shift]
                    td_cls = "today-border" if d_obj == today_kst else ""
                    # 폰트 3pt 차이 (15px vs 12px)
                    cal_html += f'<td class="cal-td {td_cls}" style="background:{bg};"><div class="cal-date-part {("sun" if i==0 else "sat" if i==6 else "") if not is_hi else "hi-text"}">{day}</div><div class="cal-shift-part {"hi-text" if is_hi else ""}">{shift}</div></td>'
            cal_html += '</tr>'
        st.markdown(cal_html + "</table>", unsafe_allow_html=True)
        # 다음 달로 이동
        curr_cal_date = (curr_cal_date + timedelta(days=32)).replace(day=1)
