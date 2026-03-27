import streamlit as st
from datetime import datetime, date, timedelta, timezone
import calendar

# --- [1] KST 및 로직 (동일 유지) ---
def get_kst():
    return datetime.now(timezone(timedelta(hours=9)))

now_kst = get_kst()
today_kst = now_kst.date()

def get_shift_label(dt):
    # 2026-01-01 B조 시작 기준 순환 로직
    diff = (dt - date(2026, 1, 1)).days
    return ["B", "C", "A"][diff % 3]

# --- [2] UI 스타일 (달력 배경 흰색 고정 및 강조 로직) ---
st.markdown("""
    <style>
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ddd; }
    .cal-td { border: 1px solid #eee; height: 65px; vertical-align: top; padding: 0 !important; background-color: white; } /* 기본 배경 흰색 */
    .cal-date-part { height: 35%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px; }
    .cal-shift-part { height: 65%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 18px; }
    
    /* 요일 색상 */
    .sun { color: #d32f2f !important; }
    .sat { color: #1976d2 !important; }
    .today-border { border: 2.5px solid #333 !important; }
    
    /* 강조 시 텍스트 흰색 처리 */
    .hi-text { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [3] 달력 출력 부분 ---
with st.expander("🏥 근무달력 (A,B,C) 상세보기", expanded=True):
    col1, col2 = st.columns([1, 1])
    with col1:
        # 기본 강조를 오늘 조로 설정
        default_hi = get_shift_label(today_kst)
        hi = st.selectbox("🎯 강조할 조 선택", ["없음", "A", "B", "C"], index=["없음", "A", "B", "C"].index(default_hi))
    
    # 강조 색상 정의
    BG_COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"} # 강조 시 진한 색상
    
    curr = today_kst.replace(day=1)
    for _ in range(3):  # 향후 3개월 표시
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        st.write(f"#### {y}년 {m}월")
        
        html = "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            html += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    html += "<td class='cal-td' style='background:#f9f9f9;'></td>"
                else:
                    d_obj = date(y, m, day)
                    s_label = get_shift_label(d_obj)
                    is_hi = (hi == s_label)
                    
                    # 강조될 때만 배경색 변경, 평소엔 흰색
                    bg_style = f"background-color: {BG_COLORS[s_label]};" if is_hi else "background-color: white;"
                    text_cls = "hi-text" if is_hi else ""
                    today_cls = "today-border" if d_obj == today_kst else ""
                    
                    # 요일 색상 결정
                    day_color_cls = "sun" if i == 0 else ("sat" if i == 6 else "")
                    if is_hi: day_color_cls = "hi-text" # 강조 시 요일 색상도 흰색으로
                    
                    html += f"""
                    <td class='cal-td {today_cls}' style='{bg_style}'>
                        <div class='cal-date-part {day_color_cls}'>{day}</div>
                        <div class='cal-shift-part {text_cls}'>{s_label}</div>
                    </td>
                    """
            html += "</tr>"
        st.markdown(html + "</table><br>", unsafe_allow_html=True)
        curr = (curr + timedelta(days=32)).replace(day=1)
