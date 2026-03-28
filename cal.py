import streamlit as st
from datetime import datetime, date, timedelta
import calendar
import pytz

# -------------------------------
# 1. 기본 설정
# -------------------------------
st.set_page_config(page_title="근무 달력", layout="wide")

KST = pytz.timezone("Asia/Seoul")
today_kst = datetime.now(KST).date()

# -------------------------------
# 2. 근무 로직 (유지)
# -------------------------------
def get_shift_simple(d):
    base = date(2024, 1, 1)
    diff = (d - base).days % 3
    return ["A", "B", "C"][diff]

# -------------------------------
# 3. 스타일 (강조 레이아웃 보정)
# -------------------------------
st.markdown("""
<style>
    .cal-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; table-layout: fixed; }
    .cal-table th { padding: 8px; font-size: 14px; background-color: #f8f9fa; }
    .cal-table td { height: 80px; border: 1px solid #eee; vertical-align: top; padding: 5px; }
    .empty-td { background: #fdfdfd; }
    .cal-date-part { font-size: 12px; font-weight: 700; padding: 2px 6px; border-radius: 4px; display: inline-block; }
    .cal-shift-part { font-size: 18px; font-weight: 900; text-align: center; margin-top: 10px; }
    .sun { color: #d32f2f; }
    .sat { color: #1976d2; }
    .today-border { border: 3px solid #333 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center;">🏥 성의교정 근무 달력</h1>', unsafe_allow_html=True)

# -------------------------------
# 4. 필터링 UI
# -------------------------------
options = ["선택 없음", "A", "B", "C"]
current_shift = get_shift_simple(today_kst)

col1, col2 = st.columns([1, 3])
with col1:
    hi = st.selectbox("🎯 강조 조 선택", options, index=options.index(current_shift) if current_shift in options else 0)

# 색상 설정
B_COLS = {"A":"#FFE0B2", "B":"#FFCDD2", "C":"#BBDEFB"}  
S_COLS = {"A":"#FB8C00", "B":"#E53935", "C":"#1E88E5"}  

# -------------------------------
# 5. 달력 생성 (Tabs 활용으로 성능 및 가독성 향상)
# -------------------------------
calendar.setfirstweekday(calendar.SUNDAY)
cal_obj = calendar.Calendar()

# 향후 12개월의 월 리스트 생성
months_to_show = []
temp_date = today_kst.replace(day=1)
for _ in range(12):
    months_to_show.append((temp_date.year, temp_date.month))
    # 다음 달 1일로 안전하게 이동
    if temp_date.month == 12:
        temp_date = temp_date.replace(year=temp_date.year + 1, month=1)
    else:
        temp_date = temp_date.replace(month=temp_date.month + 1)

tabs = st.tabs([f"{m}월" for y, m in months_to_show])

for idx, (y, m) in enumerate(months_to_show):
    with tabs[idx]:
        st.subheader(f"📅 {y}년 {m}월")
        weeks = cal_obj.monthdayscalendar(y, m)
        
        cal_html = "<table class='cal-table'><thead><tr>"
        for day_name, cls in zip(["일", "월", "화", "수", "목", "금", "토"], ["sun","","","","","","sat"]):
            cal_html += f"<th class='{cls}'>{day_name}</th>"
        cal_html += "</tr></thead><tbody>"

        for week in weeks:
            cal_html += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    cal_html += "<td class='empty-td'></td>"
                else:
                    d_obj = date(y, m, day)
                    s = get_shift_simple(d_obj)
                    is_hi = (hi == s)
                    
                    bg_color = S_COLS.get(s, "#fff") if is_hi else B_COLS.get(s, "#fff")
                    date_bg = "#FFFFFF" if not is_hi else "rgba(255,255,255,0.5)"
                    text_cls = "sun" if i == 0 else "sat" if i == 6 else ""
                    today_cls = "today-border" if d_obj == today_kst else ""

                    cal_html += f"""
                    <td class='{today_cls}' style='background:{bg_color};'>
                        <div class='cal-date-part {text_cls}' style='background:{date_bg};'>{day}</div>
                        <div class='cal-shift-part'>{s}</div>
                    </td>
                    """
            cal_html += "</tr>"
        cal_html += "</tbody></table>"
        st.markdown(cal_html, unsafe_allow_html=True)
