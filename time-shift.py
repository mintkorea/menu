import streamlit as st
from datetime import datetime, date, timedelta, timezone
import calendar

# 1. 기본 설정 및 시간 (고정)
def get_kst():
    return datetime.now(timezone(timedelta(hours=9)))

now_kst = get_kst()
today_kst = now_kst.date()

def get_shift_label(dt):
    return ["B", "C", "A"][(dt - date(2026, 1, 1)).days % 3]

# 2. CSS 스타일 (셸 전체 배색 및 강조 로직)
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")
st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 0px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; height: 45px; font-weight: 800; }
    
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ddd; }
    .cal-td { border: 1px solid #eee; height: 70px; vertical-align: top; padding: 0 !important; }
    
    /* 날짜 부분: 기본은 항상 흰색 배경 */
    .date-part { height: 30%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; background-color: white; border-bottom: 0.5px solid #eee; }
    
    /* 조 이름 부분: 기본적으로 옅은 배경색(셸 배색) */
    .shift-part { height: 70%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 18px; }
    
    .sun { color: #d32f2f; } .sat { color: #1976d2; }
    .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab3:
    st.markdown("<h3 style='text-align:center;'>🏥 성의교정 근무달력</h3>", unsafe_allow_html=True)
    hi = st.selectbox("🎯 강조할 조 선택", ["없음", "A", "B", "C"], index=3)
    
    # 조별 색상 (진한색 / 연한색)
    COLORS = {
        "A": {"bg": "#FFF3E0", "text": "#FB8C00", "hi": "#FB8C00"}, # 주황
        "B": {"bg": "#FFEBEE", "text": "#E53935", "hi": "#E53935"}, # 빨강
        "C": {"bg": "#E3F2FD", "text": "#1E88E5", "hi": "#1E88E5"}  # 파랑
    }
    
    curr = today_kst.replace(day=1)
    for _ in range(3):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        st.write(f"**{y}년 {m}월**")
        html = "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            html += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    html += "<td class='cal-td' style='background:#f9f9f9;'></td>"
                else:
                    d_obj = date(y, m, day)
                    s_lbl = get_shift_label(d_obj)
                    is_hi = (hi == s_lbl)
                    
                    # [핵심] 강조 시: 날짜까지 배경색 채움 / 평상시: 날짜는 흰색, 조 이름만 연한 배경색
                    td_bg = COLORS[s_lbl]["hi"] if is_hi else "white"
                    date_bg = COLORS[s_lbl]["hi"] if is_hi else "white"
                    shift_bg = COLORS[s_lbl]["hi"] if is_hi else COLORS[s_lbl]["bg"]
                    
                    # 글자색 설정
                    date_color = "white" if is_hi else ("#d32f2f" if i==0 else ("#1976d2" if i==6 else "#333"))
                    shift_color = "white" if is_hi else COLORS[s_lbl]["text"]
                    
                    today_cls = "today-border" if d_obj == today_kst else ""
                    
                    html += f"""
                    <td class='cal-td {today_cls}' style='background-color:{td_bg};'>
                        <div class="date-part" style="background-color:{date_bg}; color:{date_color};">{day}</div>
                        <div class="shift-part" style="background-color:{shift_bg}; color:{shift_color};">{s_lbl}</div>
                    </td>"""
            html += "</tr>"
        st.markdown(html + "</table><br>", unsafe_allow_html=True)
        curr = (curr + timedelta(days=32)).replace(day=1)

# (탭 1, 2는 이전 최종 로직 그대로 포함)
