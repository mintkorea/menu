import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta, timezone
import pytz
import calendar

# --- [1] 시간 및 로직 설정 ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()

# 근무 패턴 기준 (2026-03-09 C조/황재업 조장 시작일 기준)
PATTERN_START = date(2026, 3, 9)

def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    # 0:C, 1:A, 2:B 순환
    return ["C", "A", "B"][diff % 3]

# 세션 상태 초기화 (오늘의 조를 기본값으로)
if 'default_hi_shift' not in st.session_state:
    st.session_state.default_hi_shift = get_shift_simple(today_kst)

# --- [2] 페이지 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    /* 상단 여백 5mm 추가 (약 20px 추가하여 총 70px) */
    .block-container { padding-top: 70px !important; max-width: 600px; margin: auto; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; margin-bottom: 15px; }
    .stTabs [data-baseweb="tab"] {
        height: 42px; background-color: #f0f2f6; border-radius: 8px 8px 0 0;
        padding: 0 15px; font-weight: 700; font-size: 14px;
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    
    .main-title { text-align: center; font-size: 20px; font-weight: 900; color: #2E4077; margin-bottom: 10px; }
    .date-display { text-align: center; font-size: 16px; color: #444; margin-bottom: 15px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- [3] 달력 HTML 생성 함수 ---
def generate_calendar_html(start_dt, highlight):
    # 조별 배경색 및 강조색
    BASE_COLORS = {"A": "#FFE0B2", "B": "#FFCDD2", "C": "#BBDEFB"}
    STRONG_COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}
    
    html = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body { font-family: 'Noto Sans KR', sans-serif; background: white; margin: 0; padding: 0; }
        .container { display: flex; flex-direction: column; gap: 30px; padding: 5px; }
        .month-box { width: 100%; }
        .title { text-align: center; font-weight: 900; font-size: 1.3rem; margin-bottom: 10px; color: #333; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; }
        th { border: 1px solid #eee; background: #f8f9fa; padding: 8px 0; font-size: 13px; }
        td { border: 1px solid #eee; height: 65px; vertical-align: top; padding: 0; position: relative; }
        
        /* 날짜 부분: 기본 흰색 */
        .date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 15px; background: white; }
        /* 조 표시 부분: 기본 배경색 */
        .shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 18px; }
        
        .sun { color: #d32f2f; } .sat { color: #1976d2; }
        .hi-text { color: white !important; }
        .today-border { border: 3px solid #333 !important; }
    </style>
    <div class="container">
    """

    curr = start_dt
    for _ in range(12): # 12개월 표시
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
                    s = get_shift_simple(d_obj)
                    is_hi = (highlight == s)
                    is_today = (d_obj == today_kst)
                    
                    day_class = "sun" if (i == 0) else ("sat" if i == 6 else "")
                    
                    # 강조 시: 날짜와 조 칸 모두 STRONG_COLOR / 미강조 시: 날짜는 흰색, 조 칸은 BASE_COLOR
                    s_bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                    d_bg = STRONG_COLORS[s] if is_hi else "white"
                    
                    td_class = "today-border" if is_today else ""

                    html += f"""
                    <td class="{td_class}" style="background-color: {s_bg};">
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
        # 다음 달 계산
        curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
    
    html += "</div>"
    return html

# --- [4] 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 실시간 현황", "📅 일정 조회", "🏥 근무달력"])

# (탭 1, 탭 2 로직은 이전과 동일하므로 생략하거나 기존 코드를 그대로 유지하시면 됩니다)
with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    # ... (실시간 현황 코드)

with tab2:
    st.markdown('<div class="main-title">📅 근무 일정 조회</div>', unsafe_allow_html=True)
    # ... (일정 조회 코드)

with tab3:
    st.markdown('<div class="main-title">🏥 성의교정 근무달력</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        offset = st.slider("📅 조회 기준월 변경", -12, 12, 0)
    with c2:
        shift_options = ["선택 안 함", "A", "B", "C"]
        # 접속일 근무조를 기본값으로 설정
        default_idx = shift_options.index(st.session_state.default_hi_shift)
        hi_shift = st.selectbox("🎯 강조할 근무 조 선택", shift_options, index=default_idx)

    # 달력 시작일 설정
    start_date = (today_kst.replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
    
    # 달력 HTML 출력
    components.html(generate_calendar_html(start_date, hi_shift), height=1000, scrolling=True)
