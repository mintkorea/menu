import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta, timezone
import calendar

# 1. 한국 표준시(KST) 강제 설정 (서버 시간 무관하게 한국 시간 계산)
def get_now_kst():
    # UTC 기준에 9시간을 더해 한국 시간을 만듭니다.
    return datetime.now(timezone.utc) + timedelta(hours=9)

now_kst = get_now_kst()
today_kst = now_kst.date()

# 2. 근무 조 계산 로직 (기준일: 2026-01-01 B조)
ORDER = ["B", "C", "A"]
def get_shift(dt):
    base_date = date(2026, 1, 1)
    diff = (dt - base_date).days
    return ORDER[diff % 3]

# 오늘 날짜의 조를 미리 계산해둡니다.
today_shift = get_shift(today_kst)

# 3. 페이지 레이아웃 설정
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# CSS: 상단 여백 및 베젤 보호
st.markdown("""
    <style>
    .block-container { 
        padding-top: 60px !important; 
        padding-left: 20px !important; 
        padding-right: 20px !important; 
    }
    .top-btn {
        position: fixed; bottom: 30px; right: 20px; background-color: #333; color: white;
        width: 45px; height: 45px; border-radius: 50%; display: flex;
        align-items: center; justify-content: center; font-size: 20px;
        text-decoration: none; z-index: 9999; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 2px solid white;
    }
    iframe { width: 100% !important; border: none !important; }
    </style>
    <div id="top-anchor"></div>
    <a href="#top-anchor" class="top-btn">▲</a>
    """, unsafe_allow_html=True)

# 4. 상단 컨트롤 박스
st.subheader(f"🏥 성의교정 근무표 (오늘: {today_kst} {today_shift}조)")

col1, col2 = st.columns(2)
with col1:
    offset = st.slider("📅 조회 기준월 변경 (현재 달 대비)", -12, 12, 0)
with col2:
    # 접속 시 오늘 조가 자동으로 선택되도록 index 설정
    shift_options = ["선택 안 함", "A", "B", "C"]
    try:
        default_idx = shift_options.index(today_shift)
    except:
        default_idx = 0
    hi_shift = st.selectbox("🎯 강조할 근무 조 선택", shift_options, index=default_idx)

# 5. 달력 생성 HTML (날짜 배경 흰색 고정 + 하이라이트 로직)
def generate_calendar_html(start_dt, highlight):
    # 색상 정의
    BASE_COLORS = {"A": "#FFE0B2", "B": "#FFCDD2", "C": "#BBDEFB"}
    STRONG_COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}
    
    html = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body { font-family: 'Noto Sans KR', sans-serif; background: white; margin: 0; padding: 0; }
        .container { display: grid; grid-template-columns: 1fr; gap: 20px; padding: 10px; }
        @media (min-width: 800px) { .container { grid-template-columns: repeat(3, 1fr); } }
        .month-box { margin-bottom: 30px; }
        .title { text-align: center; font-weight: 900; font-size: 1.5rem; margin-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th { border-bottom: 2px solid #eee; padding: 8px 0; font-size: 14px; }
        td { border: 1px solid #f2f2f2; height: 60px; vertical-align: top; padding: 0; }
        .date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; background: white; }
        .shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 19px; }
        .sun { color: #d32f2f; } .sat { color: #1976d2; }
        .hi-text { color: white !important; }
    </style>
    <div class="container">
    """

    curr = start_dt
    for _ in range(12):
        year, month = curr.year, curr.month
        cal = calendar.monthcalendar(year, month)
        html += f"<div class='month-box'><div class='title'>{year}년 {month}월</div><table>"
        html += "<tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        
        for week in cal:
            html += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    html += "<td></td>"
                else:
                    d_obj = date(year, month, day)
                    s = get_shift(d_obj)
                    is_hi = (highlight == s)
                    is_today = (d_obj == today_kst)
                    
                    # 색상 결정
                    day_class = "sun" if (i == 0) else ("sat" if i == 6 else "")
                    s_bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                    d_bg = STRONG_COLORS[s] if is_hi else "white"
                    txt_color = "hi-text" if is_hi else ""
                    
                    # 오늘 날짜 테두리
                    td_style = f"background-color: {s_bg};"
                    if is_today:
                        td_style += " border: 3px solid #333;"

                    html += f"""
                    <td style="{td_style}">
                        <div class="date-part {day_class if not is_hi else 'hi-text'}" style="background-color: {d_bg};">
                            {day}
                        </div>
                        <div class="shift-part {txt_color}">
                            {s}
                        </div>
                    </td>
                    """
            html += "</tr>"
        html += "</table></div>"
        # 다음 달 계산
        curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
    
    html += "</div>"
    return html

# 6. 달력 표시
# 슬라이더로 계산된 시작 월
display_start_date = (today_kst.replace(day=1) + timedelta(days=31 * offset)).replace(day=1)

components.html(generate_calendar_html(display_start_date, hi_shift), height=7000, scrolling=False)
