import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
<style>
.block-container { padding-top: 3.0rem !important; max-width: 500px; margin: auto; }

/* 달력 기본 */
.calendar-table {
    width:100%;
    border-collapse:collapse;
    text-align:center;
}

.calendar-table td {
    background:#FFFFFF;   /* 👉 기본 흰색 고정 */
    border:1px solid #eee;
    padding:6px;
    font-size:10px;
}

.calendar-table th {
    padding:5px;
    font-size:11px;
}

.today {
    border:2px solid #000 !important;
}

.highlight {
    color:white;
    font-weight:900;
    font-size:11px;
}
</style>
""", unsafe_allow_html=True)

# --- [2] 핵심 로직 ---
kst = pytz.timezone('Asia/Seoul')
today_kst = datetime.now(kst).date()

PATTERN_START = date(2026, 3, 9)

def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    return ["C", "A", "B"][diff % 3]

if 'default_shift' not in st.session_state:
    st.session_state.default_shift = get_shift_simple(today_kst)

# --- [3] UI ---
tab1, tab2, tab3 = st.tabs(["🕒 실시간", "📅 일정", "🏥 달력"])

# -------------------------------
# 탭3 (달력)
# -------------------------------
with tab3:
    st.markdown('<div style="text-align:center;font-size:20px;font-weight:900;">🏥 근무달력</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        offset = st.slider("📅 월 이동", -12, 12, 0)
    with c2:
        hi_shift = st.selectbox(
            "🎯 강조 조",
            ["선택 안 함", "A", "B", "C"],
            index=["선택 안 함", "A", "B", "C"].index(st.session_state.default_shift)
        )

    def generate_cal_html(start_dt, highlight):

        # 👉 강조 색상
        COLORS = {
            "A": "#FB8C00",
            "B": "#E53935",
            "C": "#1E88E5"
        }

        html = "<div style='display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:15px;'>"
        curr = start_dt

        for _ in range(3):
            y, m = curr.year, curr.month
            cal = calendar.monthcalendar(y, m)

            html += f"<div style='border:1px solid #eee; padding:10px;'>"
            html += f"<h4 style='text-align:center'>{y}년 {m}월</h4>"
            html += "<table class='calendar-table'>"

            html += """
            <tr>
                <th style='color:red'>일</th>
                <th>월</th><th>화</th><th>수</th>
                <th>목</th><th>금</th>
                <th style='color:blue'>토</th>
            </tr>
            """

            for week in cal:
                html += "<tr>"
                for i, day in enumerate(week):

                    if day == 0:
                        html += "<td></td>"
                        continue

                    d_obj = date(y, m, day)
                    shift = get_shift_simple(d_obj)

                    # 👉 기본은 무조건 흰색
                    style = ""

                    # 👉 강조 조건일 때만 색 적용
                    if highlight != "선택 안 함" and shift == highlight:
                        style += f"background:{COLORS[shift]};"
                        text_class = "highlight"
                    else:
                        text_class = ""

                    # 👉 오늘 테두리
                    if d_obj == today_kst:
                        style += "border:2px solid #000;"

                    html += f"""
                    <td style="{style}">
                        <div class="{text_class}">{day}</div>
                        <div class="{text_class}">{shift}</div>
                    </td>
                    """

                html += "</tr>"

            html += "</table></div>"

            curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)

        return html + "</div>"

    cal_start = (today_kst.replace(day=1) + timedelta(days=31 * offset)).replace(day=1)

    st.markdown(generate_cal_html(cal_start, hi_shift), unsafe_allow_html=True)