import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta, timezone
import calendar

# 1. 한국 표준시(KST) 계산 함수
def get_kst():
    # 서버가 어느 나라에 있든 한국 시간으로 보정
    utc_now = datetime.now(timezone.utc)
    return utc_now + timedelta(hours=9)

now_kst = get_kst()
today_kst = now_kst.date()

# 2. 근무 조 계산 로직 (기준일: 2026-01-01 B조)
ORDER = ["B", "C", "A"]
def get_shift(dt):
    base_date = date(2026, 1, 1)
    diff = (dt - base_date).days
    return ORDER[diff % 3]

# 3. 세션 상태 초기화 (오늘의 조를 디폴트로 딱 한 번만 설정)
if 'default_shift' not in st.session_state:
    st.session_state.default_shift = get_shift(today_kst)

# 4. 페이지 설정 및 디자인
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 60px !important; padding-left: 20px !important; padding-right: 20px !important; }
    .top-btn {
        position: fixed; bottom: 30px; right: 20px; background-color: #333; color: white;
        width: 45px; height: 45px; border-radius: 50%; display: flex;
        align-items: center; justify-content: center; font-size: 20px;
        text-decoration: none; z-index: 9999; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 2px solid white;
    }
    iframe { width: 100% !important; border: none !important; }
    </style>
    <div id="top"></div>
    <a href="#top" class="top-btn">▲</a>
    """, unsafe_allow_html=True)

# 5. 상단 컨트롤 박스
st.subheader(f"🏥 성의교정 근무표 (오늘: {today_kst} {st.session_state.default_shift}조)")

col1, col2 = st.columns(2)
with col1:
    offset = st.slider("📅 조회 기준월 변경", -12, 12, 0)
with col2:
    shift_options = ["선택 안 함", "A", "B", "C"]
    # 세션에 저장된 오늘 조의 인덱스를 찾아 기본값으로 넣음
    idx = shift_options.index(st.session_state.default_shift)
    hi_shift = st.selectbox("🎯 강조할 근무 조 선택", shift_options, index=idx)

# 6. 달력 생성 HTML
def generate_html(start_dt, highlight):
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
        td { border: 1px solid #f2f2f2; height: 60px; vertical-align: top; padding: 0; position: relative; }
        .date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; background: white; }
        .shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 19px; }
        .sun { color: #d32f2f; } .sat { color: #1976d2; }
        .hi-text { color: white !important; }
    </style>
    <div class="container">
    """

    curr = start_dt
    for _ in range(12):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        html += f"<div class='month-box'><div class='title'>{y}년 {m}월</div><table>"
        html += "<tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        
        for week in cal:
            html += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    html += "<td></td>"
                else:
                    d_obj = date(y, m, day)
                    s = get_shift(d_obj)
                    is_hi = (highlight == s)
                    is_today = (d_obj == today_kst)
                    
                    day_class = "sun" if (i == 0) else ("sat" if i == 6 else "")
                    s_bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                    d_bg = STRONG_COLORS[s] if is_hi else "white"
                    
                    td_style = f"background-color: {s_bg};"
                    if is_today: td_style += " border: 3.5px solid #333;"

                    html += f"""
                    <td style="{td_style}">
                        <div class="date-part {day_class if not is_hi else 'hi-text'}" style="background-color: {d_bg};">
                            {day}
                        </div>
                        <div class="shift-part {'hi-text' if is_hi else ''}">
                            {s}
                        </div>
                    </td>
                    """
            html += "</tr>"
        html += "</table></div>"
        curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
    
    html += "</div>"
    return html

# 7. 출력
start_date = (today_kst.replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
# key 파라미터를 추가하여 상태 변화 시 강제 리프레시 유도
components.html(generate_html(start_date, hi_shift), height=7500, scrolling=False)
