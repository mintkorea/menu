import streamlit as st
from datetime import datetime, date
import calendar
import pytz


# -------------------------------
# 1. 기본 설정
# -------------------------------
st.set_page_config(page_title="근무 달력", layout="wide")

KST = pytz.timezone("Asia/Seoul")
today_kst = datetime.now(KST).date()

# -------------------------------
# 2. 샘플 근무 로직 (수정 가능)
# -------------------------------
def get_shift_simple(d):
    base = date(2024, 1, 1)
    diff = (d - base).days % 3
    return ["A", "B", "C"][diff]

# -------------------------------
# 3. 스타일
# -------------------------------
st.markdown("""
<style>
.cal-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

.cal-table th {
    padding: 6px;
    font-size: 13px;
    font-weight: 700;
}

.cal-table td {
    height: 70px;
    border: 1px solid #ddd;
    vertical-align: top;
    padding: 3px;
}

.cal-td {
    position: relative;
}

.empty-td {
    background: #f9f9f9;
}

.cal-date-part {
    font-size: 12px;
    font-weight: 700;
    border-radius: 6px;
    padding: 2px 4px;
    display: inline-block;
}

.cal-shift-part {
    font-size: 16px;
    font-weight: 900;
    text-align: center;
    margin-top: 5px;
}

.sun { color: #d32f2f; }
.sat { color: #1976d2; }

.today-border {
    border: 2px solid #000 !important;
}

.main-title {
    text-align:center;
    font-size:22px;
    font-weight:900;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 4. UI
# -------------------------------
st.markdown('<div class="main-title">🏥 성의교정 근무 달력</div>', unsafe_allow_html=True)

options = ["선택 없음", "A", "B", "C"]
current_shift = get_shift_simple(today_kst)

hi = st.selectbox(
    "🎯 강조 조 선택",
    options,
    index=options.index(current_shift) if current_shift in options else 0
)

# 색상
B_COLS = {"A":"#FFE0B2", "B":"#FFCDD2", "C":"#BBDEFB"}  # 기본
S_COLS = {"A":"#FB8C00", "B":"#E53935", "C":"#1E88E5"}  # 강조

# -------------------------------
# 5. 달력 생성
# -------------------------------
calendar.setfirstweekday(calendar.SUNDAY)
cal_obj = calendar.Calendar()

cal_html = ""
curr_cal_date = today_kst.replace(day=1)

for _ in range(12):
    y, m = curr_cal_date.year, curr_cal_date.month
    weeks = cal_obj.monthdayscalendar(y, m)

    cal_html += f"""
    <div style='text-align:center; font-weight:900; font-size:18px; margin-top:30px; margin-bottom:10px; color:#2E4077;'>
        {y}년 {m}월
    </div>
    """

    cal_html += """
    <table class='cal-table'>
        <thead>
            <tr>
                <th class='sun'>일</th>
                <th>월</th>
                <th>화</th>
                <th>수</th>
                <th>목</th>
                <th>금</th>
                <th class='sat'>토</th>
            </tr>
        </thead>
        <tbody>
    """

    for week in weeks:
        cal_html += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                cal_html += "<td class='cal-td empty-td'></td>"
            else:
                d_obj = date(y, m, day)
                s = get_shift_simple(d_obj)

                # 안전 처리
                if s not in B_COLS:
                    s = "A"

                is_hi = (hi == s)

                bg_color = S_COLS[s] if is_hi else B_COLS[s]
                date_bg = S_COLS[s] if is_hi else "#FFFFFF"

                text_color_class = (
                    "sun" if i == 0 else "sat" if i == 6 else ""
                )

                today_class = "today-border" if d_obj == today_kst else ""

                cal_html += f"""
                <td class='cal-td {today_class}' style='background:{bg_color};'>
                    <div class='cal-date-part {text_color_class}' style='background:{date_bg};'>
                        {day}
                    </div>
                    <div class='cal-shift-part'>
                        {s}
                    </div>
                </td>
                """

        cal_html += "</tr>"

    cal_html += "</tbody></table>"

    # 다음 달
    if m == 12:
        curr_cal_date = curr_cal_date.replace(year=y+1, month=1)
    else:
        curr_cal_date = curr_cal_date.replace(month=m+1)

# 출력
st.markdown(cal_html, unsafe_allow_html=True)
