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

.stTabs [data-baseweb="tab-list"] { gap: 8px; margin-bottom: 15px; }
.stTabs [data-baseweb="tab"] {
    height: 42px; background-color: #f0f2f6;
    border-radius: 8px 8px 0 0;
    padding: 0 15px; font-weight: 700; font-size: 14px;
}
.stTabs [aria-selected="true"] {
    background-color: #2E4077 !important;
    color: white !important;
}

.main-title {
    text-align: center;
    font-size: 20px;
    font-weight: 900;
    color: #2E4077;
    margin-top: 5px;
}

.date-display {
    text-align: center;
    font-size: 16px;
    color: #444;
    margin-bottom: 15px;
    font-weight: 800;
}

.status-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-bottom: 10px;
}

.status-card {
    border: 2px solid #2E4077;
    border-radius: 12px;
    padding: 8px 5px;
    text-align: center;
    background: white;
}

.worker-name { font-size: 15px; font-weight: 800; }
.status-val { font-size: 17px; font-weight: 900; color: #C04B41; }

.table-container {
    width: 100%;
    border: 1px solid #dee2e6;
    border-radius: 5px;
    margin-bottom: 20px;
}

.custom-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    text-align: center;
    table-layout: fixed;
    background: white;
}

.custom-table th, .custom-table td {
    border: 1px solid #dee2e6;
    padding: 10px 2px;
}

.header-main {
    background-color: #f8f9fa !important;
    font-weight: 800;
}

.sat { color: blue !important; font-weight: bold; }
.sun { color: red !important; font-weight: bold; }

/* 개인 색상 */
.color-hwang { background-color: #D9EAD3 !important; }
.color-kim { background-color: #FFF2CC !important; }
.color-won { background-color: #EAD1DC !important; }
.color-lee { background-color: #C9DAF8 !important; }

.highlight-row {
    background-color: #FFE5E5 !important;
    font-weight: bold;
    color: #C04B41;
}
</style>
""", unsafe_allow_html=True)

# --- [2] 핵심 로직 ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()

PATTERN_START = date(2026, 3, 9)

def get_workers(target_date):
    if isinstance(target_date, datetime):
        target_date = target_date.date()
    diff = (target_date - PATTERN_START).days

    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1

        if ci == 0:
            return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1:
            return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else:
            return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")

    return None, None, None, None


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
    st.markdown('<div class="main-title">🏥 근무달력</div>', unsafe_allow_html=True)

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
        STRONGS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}

        html = "<div style='display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:15px;'>"
        curr = start_dt

        for _ in range(3):
            y, m = curr.year, curr.month
            cal = calendar.monthcalendar(y, m)

            html += f"<div style='border:1px solid #eee; padding:10px;'>"
            html += f"<h4>{y}년 {m}월</h4>"
            html += "<table style='width:100%; border-collapse:collapse; text-align:center;'>"

            html += "<tr><th style='color:red'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th style='color:blue'>토</th></tr>"

            for week in cal:
                html += "<tr>"
                for i, day in enumerate(week):
                    if day == 0:
                        html += "<td></td>"
                    else:
                        d_obj = date(y, m, day)
                        s = get_shift_simple(d_obj)

                        is_hi = (highlight == s)
                        bg = STRONGS[s] if is_hi else "#FFFFFF"

                        # 오늘 강조
                        if d_obj == today_kst:
                            border = "3px solid #000"
                        else:
                            border = "1px solid #eee"

                        day_style = "font-size:11px; font-weight:900;" if is_hi else "font-size:10px;"
                        shift_style = "font-weight:900;" if is_hi else ""

                        html += f"""
                        <td style='background:{bg}; border:{border}; padding:6px;'>
                            <div style='{day_style}'>{day}</div>
                            <div style='{shift_style}'>{s}</div>
                        </td>
                        """

                html += "</tr>"

            html += "</table></div>"

            curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)

        return html + "</div>"

    cal_start = (today_kst.replace(day=1) + timedelta(days=31 * offset)).replace(day=1)

    st.markdown(generate_cal_html(cal_start, hi_shift), unsafe_allow_html=True)