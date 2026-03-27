import streamlit as st
from datetime import datetime, date, timedelta, timezone
import calendar

# 1. KST 및 로직
def get_kst():
    return datetime.now(timezone(timedelta(hours=9)))

now_kst = get_kst()
today_kst = now_kst.date()

def get_shift_label(dt):
    return ["B", "C", "A"][(dt - date(2026, 1, 1)).days % 3]

# 2. CSS 스타일 (배색 및 모바일 한 화면 최적화)
st.set_page_config(page_title="C조 통합 근무", layout="wide")
st.markdown("""
    <style>
    /* 전체 여백 줄여서 한 화면에 모으기 */
    .block-container { padding: 10px !important; max-width: 450px; margin: auto; }
    
    /* 달력 테이블 스타일 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ddd; }
    .cal-td { border: 1px solid #fff; height: 55px; vertical-align: middle; padding: 0 !important; text-align: center; }
    
    /* 글자 크기 키우기 */
    .date-num { font-size: 11px; font-weight: 700; display: block; margin-top: 2px; }
    .shift-name { font-size: 20px; font-weight: 900; display: block; margin-bottom: 2px; }
    
    .sun { color: #d32f2f; } .sat { color: #1976d2; }
    .today-border { border: 3px solid #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 탭 구성 (현황/편성표 생략하고 달력 집중)
tab1, tab2, tab3 = st.tabs(["🕒 현황", "📅 리스트", "🏥 달력"])

with tab3:
    hi = st.selectbox("🎯 강조 조", ["없음", "A", "B", "C"], index=3)
    
    # 조별 배경색 (은은한 색 / 강조 시 진한 색)
    # 강조되지 않았을 때도 셸에 기본 배색이 들어갑니다.
    COLOR_MAP = {
        "A": {"bg": "#FFF4E5", "hi": "#FB8C00", "txt": "#FB8C00"}, # 주황
        "B": {"bg": "#FFEBEE", "hi": "#E53935", "txt": "#E53935"}, # 빨강
        "C": {"bg": "#E3F2FD", "hi": "#1E88E5", "txt": "#1E88E5"}  # 파랑
    }
    
    curr = today_kst.replace(day=1)
    # 한 화면에 다 나오도록 이번 달, 다음 달 2개월만 표시 (필요시 조정)
    for _ in range(2):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        st.markdown(f"<div style='text-align:center; font-weight:bold; margin-top:10px;'>{y}년 {m}월</div>", unsafe_allow_html=True)
        
        html = "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            html += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    html += "<td style='background:#f4f4f4;'></td>"
                else:
                    d_obj = date(y, m, day)
                    s_lbl = get_shift_label(d_obj)
                    is_hi = (hi == s_lbl)
                    
                    # 셸 배경색: 강조 시 진한색, 평소엔 연한색 (무조건 배경색 들어감)
                    bg = COLOR_MAP[s_lbl]["hi"] if is_hi else COLOR_MAP[s_lbl]["bg"]
                    # 글자색: 강조 시 흰색, 평소엔 조별 고유색
                    t_color = "#fff" if is_hi else COLOR_MAP[s_lbl]["txt"]
                    # 날짜색: 강조 시 흰색, 평소엔 요일색
                    d_color = "#fff" if is_hi else ("#d32f2f" if i==0 else ("#1976d2" if i==6 else "#666"))
                    
                    today_cls = "today-border" if d_obj == today_kst else ""
                    
                    html += f"""
                    <td class='cal-td {today_cls}' style='background-color:{bg};'>
                        <span class="date-num" style="color:{d_color};">{day}</span>
                        <span class="shift-name" style="color:{t_color};">{s_lbl}</span>
                    </td>"""
            html += "</tr>"
        st.markdown(html + "</table>", unsafe_allow_html=True)
        curr = (curr + timedelta(days=32)).replace(day=1)
