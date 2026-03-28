import streamlit as st
from datetime import datetime, date
import calendar
import pytz

# -------------------------------
# 1. 페이지 및 시간 설정
# -------------------------------
st.set_page_config(page_title="🏥 성의교정 근무 달력", layout="wide")

KST = pytz.timezone("Asia/Seoul")
today_kst = datetime.now(KST).date()

# -------------------------------
# 2. 근무 로직 (3교대 가정)
# -------------------------------
def get_shift_simple(d):
    base = date(2024, 1, 1)  # 기준일
    diff = (d - base).days % 3
    return ["A", "B", "C"][diff]

# -------------------------------
# 3. CSS 스타일 (디자인 개선)
# -------------------------------
st.markdown("""
<style>
    /* 테이블 기본 스타일 */
    .cal-table {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
        margin-bottom: 20px;
        background-color: white;
    }
    .cal-table th {
        padding: 10px;
        background-color: #f8f9fa;
        border-bottom: 2px solid #dee2e6;
        text-align: center;
    }
    .cal-table td {
        height: 90px;
        border: 1px solid #eee;
        vertical-align: top;
        padding: 5px;
    }
    
    /* 날짜 및 근무조 텍스트 */
    .cal-date-part {
        font-size: 13px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
    }
    .cal-shift-part {
        font-size: 22px;
        font-weight: 900;
        text-align: center;
        margin-top: 10px;
    }
    
    /* 요일 색상 */
    .sun { color: #d32f2f !important; }
    .sat { color: #1976d2 !important; }
    
    /* 오늘 표시 */
    .today-border {
        outline: 3px solid #333 !important;
        outline-offset: -3px;
    }
    
    /* 빈 칸 배경 */
    .empty-td { background-color: #fcfcfc; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 4. 상단 UI (필터)
# -------------------------------
st.title("🏥 성의교정 근무 달력")

options = ["선택 없음", "A", "B", "C"]
current_shift = get_shift_simple(today_kst)

col1, _ = st.columns([1, 2])
with col1:
    hi = st.selectbox(
        "🎯 강조할 근무조를 선택하세요",
        options,
        index=options.index(current_shift) if current_shift in options else 0
    )

# 근무조별 색상 정의
B_COLS = {"A":"#FFE0B2", "B":"#FFCDD2", "C":"#BBDEFB"}  # 기본 (연한 색)
S_COLS = {"A":"#FB8C00", "B":"#E53935", "C":"#1E88E5"}  # 강조 (진한 색)

# -------------------------------
# 5. 달력 생성 및 출력
# -------------------------------
calendar.setfirstweekday(calendar.SUNDAY)
cal_obj = calendar.Calendar()

# 향후 12개월 계산
months = []
curr = today_kst.replace(day=1)
for _ in range(12):
    months.append((curr.year, curr.month))
    if curr.month == 12:
        curr = curr.replace(year=curr.year + 1, month=1)
    else:
        curr = curr.replace(month=curr.month + 1)

# 탭으로 분리하여 렌더링 오류 방지 및 가독성 향상
tabs = st.tabs([f"{m}월" for y, m in months])

for idx, (y, m) in enumerate(months):
    with tabs[idx]:
        st.subheader(f"📅 {y}년 {m}월")
        
        weeks = cal_obj.monthdayscalendar(y, m)
        html = "<table class='cal-table'><thead><tr>"
        for i, day_name in enumerate(["일", "월", "화", "수", "목", "금", "토"]):
            cls = "sun" if i == 0 else "sat" if i == 6 else ""
            html += f"<th class='{cls}'>{day_name}</th>"
        html += "</tr></thead><tbody>"

        for week in weeks:
            html += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    html += "<td class='empty-td'></td>"
                else:
                    d_obj = date(y, m, day)
                    shift = get_shift_simple(d_obj)
                    is_hi = (hi == shift)

                    # 스타일 결정
                    bg_color = S_COLS[shift] if is_hi else B_COLS[shift]
                    date_bg = "rgba(255,255,255,0.6)" if is_hi else "#FFFFFF"
                    text_cls = "sun" if i == 0 else "sat" if i == 6 else ""
                    today_cls = "today-border" if d_obj == today_kst else ""

                    html += f"""
                    <td class='{today_cls}' style='background-color:{bg_color};'>
                        <div class='cal-date-part {text_cls}' style='background-color:{date_bg};'>
                            {day}
                        </div>
                        <div class='cal-shift-part'>
                            {shift}
                        </div>
                    </td>
                    """
            html += "</tr>"
        
        html += "</tbody></table>"
        # 핵심: 각 탭 안에서 개별적으로 markdown 실행
        st.markdown(html, unsafe_allow_html=True)

# -------------------------------
# 6. 하단 정보
# -------------------------------
st.caption(f"기준일: 2024-01-01 (A조 시작) | 오늘 날짜: {today_kst}")
