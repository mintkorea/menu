import streamlit as st
from datetime import datetime, date
import calendar
import pytz

# 1. 페이지 설정
st.set_page_config(page_title="근무 달력", layout="wide")
KST = pytz.timezone("Asia/Seoul")
today_kst = datetime.now(KST).date()

# 2. 근무 로직
def get_shift_simple(d):
    base = date(2024, 1, 1)
    diff = (d - base).days % 3
    return ["A", "B", "C"][diff]

# 3. CSS 스타일 (마크다운 충돌 방지를 위해 별도 변수 선언)
style_html = """
<style>
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; margin-bottom: 20px; }
    .cal-table th { background: #f8f9fa; padding: 10px; border-bottom: 2px solid #ddd; font-size: 14px; }
    .cal-table td { height: 80px; border: 1px solid #eee; vertical-align: top; padding: 5px; }
    .cal-date { font-size: 12px; font-weight: bold; padding: 2px 5px; border-radius: 4px; display: inline-block; background: white; }
    .cal-shift { font-size: 22px; font-weight: 900; text-align: center; margin-top: 10px; }
    .sun { color: red !important; }
    .sat { color: blue !important; }
    .today-box { outline: 3px solid black !important; outline-offset: -3px; }
</style>
"""
st.markdown(style_html, unsafe_allow_html=True)

st.title("🏥 성의교정 근무 달력")

# 4. 필터
options = ["선택 없음", "A", "B", "C"]
current_shift = get_shift_simple(today_kst)
hi = st.selectbox("🎯 강조 조 선택", options, index=options.index(current_shift))

B_COLS = {"A":"#FFE0B2", "B":"#FFCDD2", "C":"#BBDEFB"}
S_COLS = {"A":"#FB8C00", "B":"#E53935", "C":"#1E88E5"}

# 5. 달력 루프
curr = today_kst.replace(day=1)
tabs = st.tabs([f"{ (curr.month + i - 1) % 12 + 1 }월" for i in range(12)])

for i in range(12):
    y, m = curr.year, curr.month
    with tabs[i]:
        st.write(f"### 📅 {y}년 {m}월")
        
        # 테이블 헤더 구성
        html_str = "<table class='cal-table'><thead><tr>"
        for j, name in enumerate(["일", "월", "화", "수", "목", "금", "토"]):
            c = "sun" if j == 0 else "sat" if j == 6 else ""
            html_str += f"<th class='{c}'>{name}</th>"
        html_str += "</tr></thead><tbody>"

        weeks = calendar.Calendar(calendar.SUNDAY).monthdayscalendar(y, m)
        for week in weeks:
            html_str += "<tr>"
            for idx, day in enumerate(week):
                if day == 0:
                    html_str += "<td style='background:#f9f9f9;'></td>"
                else:
                    d_obj = date(y, m, day)
                    s = get_shift_simple(d_obj)
                    is_hi = (hi == s)
                    bg = S_COLS[s] if is_hi else B_COLS[s]
                    
                    t_cls = "sun" if idx == 0 else "sat" if idx == 6 else ""
                    td_cls = "today-box" if d_obj == today_kst else ""
                    
                    # f-string 내부에 따옴표가 겹치지 않게 조심해서 조립
                    cell = f"<td class='{td_cls}' style='background:{bg};'>"
                    cell += f"<div class='cal-date {t_cls}'>{day}</div>"
                    cell += f"<div class='cal-shift'>{s}</div>"
                    cell += "</td>"
                    html_str += cell
            html_str += "</tr>"
        
        html_str += "</tbody></table>"
        
        # 핵심: 월별로 독립된 마크다운 렌더링
        st.markdown(html_str, unsafe_allow_html=True)

    # 다음 달 계산
    if m == 12: curr = curr.replace(year=y+1, month=1)
    else: curr = curr.replace(month=m+1)
