import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 스타일 설정 (달력 크기 및 하이라이트 수정) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    
    /* 달력 표 크기 축소 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; margin-bottom: 30px; }
    .cal-td { border: 1px solid #eee; height: 50px; vertical-align: top; padding: 0 !important; }
    
    /* 날짜 구역 (상단) */
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; }
    
    /* 조 표시 구역 (하단) - 날짜보다 3pt 크게 (16px) */
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; }
    
    .sun { color: #d32f2f !important; }
    .sat { color: #1976d2 !important; }
    .hi-text { color: #FFFFFF !important; } /* 하이라이트 시 흰색 글자 */
    .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 기존 로직 유지 ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
PATTERN_START = date(2026, 3, 9) 

def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    return ["C", "A", "B"][diff % 3]

# --- [3] 탭 구성 (기존 탭 구조 유지) ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

# (tab1, tab2는 기존 사용자 소스 내용 그대로 유지된다고 가정)

with tab3:
    st.markdown('<div class="main-title">🏥 12개월 근무 달력</div>', unsafe_allow_html=True)
    
    # 하이라이트 및 조회 설정
    hi = st.radio("강조 근무조 선택", ["A", "B", "C"], index=2, horizontal=True)
    
    # 색상 정의 (연한 배경 / 진한 배경)
    L_COLS = {"A":"#FFE0B2", "B":"#FFCDD2", "C":"#BBDEFB"} # 평시 조 배경
    D_COLS = {"A":"#FB8C00", "B":"#E53935", "C":"#1E88E5"} # 하이라이트 배경
    
    curr = today_kst.replace(day=1)
    
    for _ in range(12):
        y, m = curr.year, curr.month
        st.write(f"**{y}년 {m}월**")
        cal = calendar.monthcalendar(y, m)
        
        cal_html = '<table class="cal-table"><tr><th class="sun">일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class="sat">토</th></tr>'
        
        for week in cal:
            cal_html += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    cal_html += "<td class='cal-td'></td>"
                else:
                    d_obj = date(y, m, day)
                    s = get_shift_simple(d_obj)
                    is_hi = (hi == s)
                    
                    # 배경색: 하이라이트 시 날짜 구역까지 진한색으로 확대
                    # 하이라이트가 아니면 날짜 구역은 흰색, 조 표시 구역만 연한 배경색
                    date_bg = D_COLS[s] if is_hi else "white"
                    shift_bg = D_COLS[s] if is_hi else L_COLS[s]
                    
                    # 글자색 설정
                    date_color_class = ""
                    if is_hi:
                        date_color_class = "hi-text"
                    else:
                        if i == 0: date_color_class = "sun"
                        elif i == 6: date_color_class = "sat"
                    
                    td_cls = "today-border" if d_obj == today_kst else ""
                    
                    cal_html += f"""
                    <td class='cal-td {td_cls}'>
                        <div class='cal-date-part {date_color_class}' style='background:{date_bg};'>
                            {day}
                        </div>
                        <div class='cal-shift-part {'hi-text' if is_hi else ''}' style='background:{shift_bg};'>
                            {s}
                        </div>
                    </td>"""
            cal_html += "</tr>"
        st.markdown(cal_html + "</table>", unsafe_allow_html=True)
        
        # 다음 달 이동 로직
        curr = (curr + timedelta(days=32)).replace(day=1)
