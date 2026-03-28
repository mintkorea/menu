import streamlit as st
from datetime import datetime, date
import calendar
import pytz

# 1. 설정
st.set_page_config(page_title="🏥 성의교정 근무 달력", layout="wide")
KST = pytz.timezone("Asia/Seoul")
today_kst = datetime.now(KST).date()

# 2. 근무 로직
def get_shift_simple(d):
    base = date(2024, 1, 1)
    diff = (d - base).days % 3
    return ["A", "B", "C"][diff]

# 3. 스타일 (먼저 한 번만 선언)
st.markdown("""
<style>
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; margin-bottom: 5px; }
    .cal-table th { background: #f8f9fa; padding: 8px; border-bottom: 2px solid #eee; font-size: 14px; }
    .cal-table td { height: 80px; border: 1px solid #f0f0f0; vertical-align: top; padding: 4px; }
    .cal-date { font-size: 12px; font-weight: bold; padding: 2px 5px; border-radius: 4px; display: inline-block; background: white; }
    .cal-shift { font-size: 20px; font-weight: 900; text-align: center; margin-top: 10px; color: #333; }
    .sun { color: #d32f2f; }
    .sat { color: #1976d2; }
    .today-box { outline: 3px solid #000 !important; outline-offset: -3px; }
</style>
""", unsafe_allow_html=True)

st.title("🏥 성의교정 근무 달력")

# 4. 필터
options = ["선택 없음", "A", "B", "C"]
current_shift = get_shift_simple(today_kst)
hi = st.selectbox("🎯 강조 조 선택", options, index=options.index(current_shift))

B_COLS = {"A":"#FFE0B2", "B":"#FFCDD2", "C":"#BBDEFB"}
S_COLS = {"A":"#FB8C00", "B":"#E53935", "C":"#1E88E5"}

# 5. 달력 렌더링 (월별 탭 활용)
calendar.setfirstweekday(calendar.SUNDAY)
curr = today_kst.replace(day=1)

tabs = st.tabs([f"{ (curr.month + i - 1) % 12 + 1 }월" for i in range(12)])

for i in range(12):
    y, m = curr.year, curr.month
    with tabs[i]:
        # 월 헤더 출력
        st.markdown(f"### 📅 {y}년 {m}월")
        
        # 테이블 시작
        html = "<table class='cal-table'><thead><tr>"
        for j, name in enumerate(["일", "월", "화", "수", "목", "금", "토"]):
            cls = "sun" if j == 0 else "sat" if j == 6 else ""
            html += f"<th class='{cls}'>{name}</th>"
        html += "</tr></thead><tbody>"

        weeks = calendar.Calendar(calendar.SUNDAY).monthdayscalendar(y, m)
        for week in weeks:
            html += "<tr>"
            for idx, day in enumerate(week):
                if day == 0:
                    html += "<td style='background:#fafafa;'></td>"
                else:
                    d_obj = date(y, m, day)
                    s = get_shift_simple(d_obj)
                    is_hi = (hi == s)
                    bg = S_COLS[s] if is_hi else B_COLS[s]
                    t_cls = "sun" if idx == 0 else "sat" if idx == 6 else ""
                    td_cls = "today-box" if d_obj == today_kst else ""
                    
                    html += f"""
                    <td class='{td_cls}' style='background:{bg};'>
                        <div class='cal-date {t_cls}'>{day}</div>
                        <div class='cal-shift'>{s}</div>
                    </td>
                    """
            html += "</tr>"
        html += "</tbody></table>"
        
        # 각 월별로 개별 마크다운 실행
        st.markdown(html, unsafe_allow_html=True)

    # 다음 달 계산
    if m == 12: curr = curr.replace(year=y+1, month=1)
    else: curr = curr.replace(month=m+1)
