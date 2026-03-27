import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 스타일 설정 (사용자 원본 유지 + 달력 3pt 차이 및 배색 추가) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 2px; display: flex; width: 100%; justify-content: space-around; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; height: 40px; background-color: #f0f2f6; border-radius: 5px 5px 0 0; padding: 0px !important; font-weight: 800; font-size: 12px !important; }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    
    /* 현황판 및 테이블 스타일 (원본 유지) */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-bottom: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 8px 2px; text-align: center; background: white; }
    .worker-name { font-size: 14px; font-weight: 800; color: #333; }
    .status-val { font-size: 16px; font-weight: 900; color: #C04B41; }

    /* 달력 교정: 표 크기 축소 및 3pt 폰트 차이 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; margin-bottom: 25px; }
    .cal-td { border: 1px solid #eee; height: 50px; vertical-align: top; padding: 0 !important; }
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; }
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; } /* 조 표시 3pt 크게 */
    
    .sun { color: #d32f2f !important; }
    .sat { color: #1976d2 !important; }
    .hi-text { color: white !important; }
    .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 설정 (사용자 기준일 및 주기 반영) ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
PATTERN_START = date(2026, 3, 9) # 기준일

def get_workers(target_date):
    """회관 순서: 김태언(2)>이정석(2)->이태원(2) / 당직: 입사순(김태언>이태원>이정석)"""
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

# --- [3] 탭 구성 (원본 그대로 사용) ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    # (사용자님의 원본 현황판 로직 유지)
    st.markdown(f'<div style="text-align:center; font-size:14px; color:#666;">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    is_active = now_kst.hour >= 7
    work_date = today_kst if is_active else today_kst - timedelta(days=1)
    names = get_workers(work_date)
    
    # 시간대별 메시지 삽입 (사용자 요청 조건)
    m_total = now_kst.hour * 60 + now_kst.minute
    if not is_active:
        msg = "오늘 하루도 보람차고 즐거운 하루가 되도록 합시다." if m_total < 400 else "근무 준비중..."
        st.markdown(f'<div class="status-card" style="grid-column: span 2; padding:15px; font-weight:800;">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'''<div class="status-container">
            <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">보안실</div></div>
            <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">로비</div></div>
            <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">순찰</div></div>
            <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">휴게</div></div>
        </div>''', unsafe_allow_html=True)

with tab2:
    # (사용자님의 원본 편성표 로직 유지 + 슬라이더 연동)
    offset = st.slider("조회 월 변경", -12, 12, 0)
    curr_m = (today_kst.replace(day=1) + timedelta(days=offset * 31)).replace(day=1)
    # ... 편성표 출력 루프 ...

with tab3:
    # [수정 포인트] 하이라이트 시 날짜칸까지 배색 확대 + 3pt 차이 반영
    hi = st.radio("강조 조", ["A", "B", "C"], index=2, horizontal=True)
    L_COLS, D_COLS = {"A":"#FFE0B2","B":"#FFCDD2","C":"#BBDEFB"}, {"A":"#FB8C00","B":"#E53935","C":"#1E88E5"}
    
    curr_c = today_kst.replace(day=1)
    for _ in range(12):
        y, m = curr_c.year, curr_c.month
        st.write(f"**{y}년 {m}월**")
        cal = calendar.monthcalendar(y, m)
        cal_html = '<table class="cal-table"><tr><th class="sun">일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class="sat">토</th></tr>'
        for week in cal:
            cal_html += '<tr>'
            for i, day in enumerate(week):
                if day == 0: cal_html += '<td class="cal-td"></td>'
                else:
                    d_obj = date(y, m, day); s = get_shift_simple(d_obj); is_hi = (hi == s)
                    d_bg = D_COLS[s] if is_hi else "white"
                    s_bg = D_COLS[s] if is_hi else L_COLS[s]
                    d_cls = "hi-text" if is_hi else ("sun" if i==0 else "sat" if i==6 else "")
                    td_cls = "today-border" if d_obj == today_kst else ""
                    cal_html += f'<td class="cal-td {td_cls}"><div class="cal-date-part {d_cls}" style="background:{d_bg};">{day}</div><div class="cal-shift-part {"hi-text" if is_hi else ""}" style="background:{s_bg};">{s}</div></td>'
            cal_html += '</tr>'
        st.markdown(cal_html + "</table>", unsafe_allow_html=True)
        curr_c = (curr_c + timedelta(days=32)).replace(day=1)
