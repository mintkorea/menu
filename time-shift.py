import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta, timezone
import calendar

# 1. 한국 표준시(KST) 설정
KST = timezone(timedelta(hours=9))
now_kst = datetime.now(KST)
today_kst = now_kst.date()

# 2. 페이지 설정
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# 3. 근무 로직 및 자동 조 계산
ORDER = ["B", "C", "A"]
BASE_COLORS = {"A": "#FFE0B2", "B": "#FFCDD2", "C": "#BBDEFB"}
STRONG_COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}

def get_shift(dt):
    # 기준일 2026-01-01 (B조 시작)
    base = date(2026, 1, 1)
    return ORDER[(dt - base).days % 3]

# 오늘 날짜의 근무조를 기본값으로 설정
default_shift = get_shift(today_kst)

def is_holiday(dt):
    hols = [date(dt.year, 1, 1), date(dt.year, 3, 1), date(dt.year, 5, 5), date(dt.year, 6, 6),
            date(dt.year, 8, 15), date(dt.year, 10, 3), date(dt.year, 10, 9), date(dt.year, 12, 25)]
    return dt in hols

# 4. CSS: 여백 및 플로팅 버튼
st.markdown("""
    <style>
    .block-container { 
        padding-top: 65px !important; 
        padding-left: 25px !important; 
        padding-right: 25px !important; 
        max-width: 100% !important; 
    }
    .stSlider, .stSelectbox { margin-bottom: 20px !important; }
    .top-btn {
        position: fixed; bottom: 30px; right: 25px; background-color: #333; color: white;
        width: 50px; height: 50px; border-radius: 25px; display: flex;
        align-items: center; justify-content: center; font-size: 24px;
        text-decoration: none; z-index: 9999; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 2px solid white;
    }
    iframe { width: 100% !important; border: none !important; }
    </style>
    <div id="top"></div>
    <a href="#top" class="top-btn">▲</a>
    """, unsafe_allow_html=True)

# 5. 상단 컨트롤러
st.subheader(f"🏥 성의교정 근무스케줄 (오늘: {today_kst} / {default_shift}조)")
c1, c2 = st.columns([1, 1])
with c1:
    offset = st.slider("📅 조회 시작 달 설정 (현재 기준)", -12, 12, 0)
with c2:
    # 접속 시 오늘 근무조(default_shift)가 자동으로 선택되어 있음
    hi_shift = st.selectbox("🎯 강조할 근무 조 선택", ["선택 안 함", "A", "B", "C"], 
                            index=["선택 안 함", "A", "B", "C"].index(default_shift))

# 기준 날짜 계산
base_start_date = (today_kst.replace(day=1) + timedelta(days=31 * offset)).replace(day=1)

# 6. HTML 생성 함수
def get_final_html(start_dt, highlight):
    html_content = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body { font-family: 'Noto Sans KR', sans-serif; background-color: white; margin: 0; padding: 0; overflow: hidden; }
        .grid-container { display: grid; grid-template-columns: 1fr; gap: 10px; padding: 0 5px; box-sizing: border-box; width: 100%; }
        @media (min-width: 800px) { .grid-container { grid-template-columns: repeat(3, 1fr); gap: 25px; padding: 20px; } }
        .cal-box { border: none; background: white; width: 100%; margin-bottom: 25px; }
        .month-title { text-align: center; font-weight: 900; font-size: 1.6rem; margin: 15px 0; color: #222; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th { border-bottom: 2px solid #eee; padding-bottom: 10px; font-size: 14px; }
        td { border: 1px solid #f2f2f2; height: 62px; vertical-align: top; padding: 0; }
        .sun { color: #d32f2f; } .sat { color: #1976d2; }
        .cell-content { display: flex; flex-direction: column; height: 100%; }
        /* 오늘 날짜 표시용 스타일 */
        .today-mark { border: 2.5px solid #333 !important; }
        .date-num { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; background-color: #FFFFFF; }
        .date-num.hi { color: white !important; }
        .shift-name { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 20px; }
    </style>
    <div class="grid-container">
    """
    curr = start_dt
    for _ in range(12):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        html_content += f"<div class='cal-box'><div class='month-title'>{y}년 {m}월</div><table>"
        html_content += "<tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            html_content += "<tr>"
            for i, day in enumerate(week):
                if day == 0: html_content += "<td></td>"
                else:
                    curr_d = date(y, m, day)
                    s = get_shift(curr_d)
                    is_hi = (highlight == s)
                    is_today = (curr_d == today_kst)
                    
                    day_clr = "sun" if (i == 0 or is_holiday(curr_d)) else ("sat" if i == 6 else "")
                    d_bg = STRONG_COLORS[s] if is_hi else "#FFFFFF"
                    d_txt = "white" if is_hi else ""
                    s_bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                    s_txt = "white" if is_hi else "#333"

                    html_content += f"""
                    <td style="background-color: {s_bg}; {'border: 2px solid #333;' if is_today else ''}">
                        <div class="cell-content">
                            <div class="date-num {day_clr if not is_hi else 'hi'}" style="background-color: {d_bg}; color: {d_txt};">
                                {day}
                            </div>
                            <div class="shift-name" style="color: {s_txt};">{s}</div>
                        </div>
                    </td>"""
            html_content += "</tr>"
        html_content += "</table></div>"
        curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
    return html_content + "</div>"

# 7. 렌더링
components.html(get_final_html(base_start_date, hi_shift), height=7600, scrolling=False)
