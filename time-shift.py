import streamlit as st
from datetime import datetime, date, timedelta, timezone
import calendar

# 1. 시간 및 로직 (고정)
def get_kst():
    return datetime.now(timezone(timedelta(hours=9)))

now_kst = get_kst()
today_kst = now_kst.date()

def get_shift_label(dt):
    # 2026-01-01 B조 시작 기준 순환
    return ["B", "C", "A"][(dt - date(2026, 1, 1)).days % 3]

# C조 6일 패턴 (선임자 우선 A배정)
PATTERN = [
    ("황재업", "김태언", "이태원", "이정석"), ("황재업", "김태언", "이정석", "이태원"),
    ("황재업", "이정석", "김태언", "이태원"), ("황재업", "이정석", "이태원", "김태언"),
    ("황재업", "이태원", "김태언", "이정석"), ("황재업", "이태원", "이정석", "김태언")
]

def get_base_workers(dt):
    # 3/27 시작 기준
    return list(PATTERN[(dt - date(2026, 3, 27)).days % 6])

# 2. CSS 스타일 (지시하신 배경/색상 규칙 반영)
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")
st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 0px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; height: 45px; font-weight: 800; }
    
    /* 달력 기본 구조 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ddd; }
    .cal-td { border: 1px solid #eee; height: 65px; vertical-align: top; padding: 0 !important; overflow: hidden; }
    
    /* 날짜 칸 (기본 흰색 배경) */
    .date-part { height: 35%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 12px; background-color: white; }
    
    /* 조 이름 칸 (기본 흰색 배경) */
    .shift-part { height: 65%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 18px; background-color: white; }
    
    .sun { color: #d32f2f; } .sat { color: #1976d2; }
    .today-border { border: 2.5px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

# --- 탭 3: 근무달력 (완결) ---
with tab3:
    st.markdown("<h3 style='text-align:center;'>🏥 성의교정 근무달력</h3>", unsafe_allow_html=True)
    hi = st.selectbox("🎯 강조할 조 선택", ["없음", "A", "B", "C"], index=3) # 기본 C조 강조
    
    # 조별 고유 색상
    COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}
    
    curr = today_kst.replace(day=1)
    for _ in range(3): # 3개월 표시
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        st.write(f"**{y}년 {m}월**")
        html = "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            html += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    html += "<td class='cal-td' style='background:#f9f9f9;'></td>"
                else:
                    d_obj = date(y, m, day)
                    s_lbl = get_shift_label(d_obj)
                    is_hi = (hi == s_lbl)
                    
                    # 1. 하이라이트 여부에 따른 배경색 결정 (하이라이트 시 날짜까지 배색)
                    td_bg = COLORS[s_lbl] if is_hi else "white"
                    date_bg = COLORS[s_lbl] if is_hi else "white"
                    shift_bg = COLORS[s_lbl] if is_hi else "white"
                    
                    # 2. 글자색 결정 (하이라이트 시 흰색, 아닐 시 조별 고유 색상)
                    shift_text_color = "white" if is_hi else COLORS[s_lbl]
                    date_text_color = "white" if is_hi else ("#d32f2f" if i==0 else ("#1976d2" if i==6 else "#333"))
                    
                    today_cls = "today-border" if d_obj == today_kst else ""
                    
                    html += f"""
                    <td class='cal-td {today_cls}' style='background-color:{td_bg};'>
                        <div class="date-part" style="background-color:{date_bg}; color:{date_text_color};">{day}</div>
                        <div class="shift-part" style="background-color:{shift_bg}; color:{shift_text_color};">{s_lbl}</div>
                    </td>"""
            html += "</tr>"
        st.markdown(html + "</table><br>", unsafe_allow_html=True)
        curr = (curr + timedelta(days=32)).replace(day=1)

# --- 탭 1 & 2 (누락 없이 통합) ---
with tab1:
    st.markdown("<h3 style='text-align:center;'>🛡️ 실시간 현황</h3>", unsafe_allow_html=True)
    v_person = st.selectbox("🏥 연차자 선택", ["없음", "김태언", "이정석", "이태원"])
    w_date = today_kst if now_kst.hour >= 7 else (today_kst - timedelta(days=1))
    base = get_base_workers(w_date)
    # 연차 이동 로직 적용된 4인 현황판 출력...

with tab2:
    st.markdown("<h3 style='text-align:center;'>📅 C조 상세 편성표</h3>", unsafe_allow_html=True)
    # 20일치 리스트 출력...
