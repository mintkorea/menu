import streamlit as st
from datetime import datetime, date, timedelta, timezone
import calendar

# 1. KST 시간 및 로직 설정 (선임자 우선 A배정)
def get_kst():
    return datetime.now(timezone(timedelta(hours=9)))

now_kst = get_kst()
today_kst = now_kst.date()

# [로직] C조 6일 주기 (선임 순위: 김태언 > 이태원 > 이정석)
PATTERN = [
    ("황재업", "김태언", "이태원", "이정석"), # 1일차: 태원(선임) A
    ("황재업", "김태언", "이정석", "이태원"), # 2일차: 정석(후임) A
    ("황재업", "이정석", "김태언", "이태원"), # 3일차: 태언(선임) A
    ("황재업", "이정석", "이태원", "김태언"), # 4일차: 태원(후임) A
    ("황재업", "이태원", "김태언", "이정석"), # 5일차: 태언(선임) A
    ("황재업", "이태원", "이정석", "김태언")  # 6일차: 정석(후임) A
]

def get_base_workers(dt):
    start_date = date(2026, 3, 27)
    diff = (dt - start_date).days
    return list(PATTERN[diff % 6])

def apply_vacation(workers, v_name):
    if not v_name or v_name == "없음": return workers
    ldr, sung, ui_a, ui_b = workers
    if v_name == sung: return [ldr, "연차(조장대근)", ui_a, ui_b]
    if v_name == ui_a: return [ldr, ldr, "연차(성의이동)", ui_b]
    if v_name == ui_b: return [ldr, ldr, ui_a, "연차(성의이동)"]
    return workers

# 2. UI 스타일 (스크린샷 기반 복구)
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")
st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 0px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; height: 45px; font-weight: 800; font-size: 14px; }
    /* 현황판 카드 스타일 복구 */
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 12px; text-align: center; background: white; margin-bottom: 10px; }
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ddd; }
    .cal-td { border: 1px solid #eee; height: 65px; vertical-align: top; padding: 0 !important; background-color: white; }
    .hi-text { color: white !important; }
    .sun { color: #d32f2f !important; } .sat { color: #1976d2 !important; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

# --- 탭 1: 근무현황 (스크린샷 16:08 디자인 복구) ---
with tab1:
    st.markdown(f"<h3 style='text-align:center;'>🛡️ 실시간 근무 현황</h3>", unsafe_allow_html=True)
    v_person = st.selectbox("🏥 오늘 연차자 선택", ["없음", "김태언", "이정석", "이태원"])
    
    # 오전 7시 기준 날짜 판정
    w_date = today_kst if now_kst.hour >= 7 else (today_kst - timedelta(days=1))
    base = get_base_workers(w_date)
    final = apply_vacation(base, v_person)
    
    # [복구] 4인 현황판 레이아웃
    st.markdown(f'''
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
        <div class="status-card"><small>조장</small><br><b>{final[0]}</b></div>
        <div class="status-card"><small>성의회관</small><br><b style="color:#d32f2f;">{final[1]}</b></div>
        <div class="status-card"><small>의산A</small><br><b>{final[2]}</b></div>
        <div class="status-card"><small>의산B</small><br><b>{final[3]}</b></div>
    </div>
    ''', unsafe_allow_html=True)

# --- 탭 2: 편성표 (날짜 공란 해결) ---
with tab2:
    st.markdown("<h3 style='text-align:center;'>📅 C조 상세 편성표</h3>", unsafe_allow_html=True)
    s_date = st.date_input("조회 시작일", today_kst)
    t_html = '<table style="width:100%; border-collapse:collapse; text-align:center; font-size:13px;">'
    t_html += '<tr style="background:#f4f4f4; font-weight:bold;"><td>날짜</td><td>조장</td><td>성희</td><td>의산A</td><td>의산B</td></tr>'
    for i in range(21):
        target = s_date + timedelta(days=i)
        ws = get_base_workers(target)
        wd = target.weekday()
        day_str = f"{target.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})"
        style = "color:#d32f2f;" if wd==6 else ("color:#1976d2;" if wd==5 else "")
        t_html += f'<tr><td style="{style}">{day_str}</td><td>{ws[0]}</td><td>{ws[1]}</td><td>{ws[2]}</td><td>{ws[3]}</td></tr>'
    st.markdown(t_html + "</table>", unsafe_allow_html=True)

# --- 탭 3: 근무달력 (흰 배경 + 강조 시 칸 전체 색상) ---
with tab3:
    st.markdown("<h3 style='text-align:center;'>🏥 성의교정 근무달력</h3>", unsafe_allow_html=True)
    hi = st.selectbox("🎯 강조할 조 선택", ["없음", "A", "B", "C"], index=3)
    BG_COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}
    
    def get_shift_label(dt):
        return ["B", "C", "A"][(dt - date(2026, 1, 1)).days % 3]

    curr = today_kst.replace(day=1)
    for _ in range(3):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        st.write(f"**{y}년 {m}월**")
        html = "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            html += "<tr>"
            for i, day in enumerate(week):
                if day == 0: html += "<td class='cal-td' style='background:#f9f9f9;'></td>"
                else:
                    d_obj = date(y, m, day)
                    s_lbl = get_shift_label(d_obj)
                    is_hi = (hi == s_lbl)
                    bg = f"background-color: {BG_COLORS[s_lbl]};" if is_hi else "background-color: white;"
                    text_cls = "hi-text" if is_hi else ""
                    day_cls = ("sun" if i==0 else "sat" if i==6 else "") if not is_hi else "hi-text"
                    html += f"<td class='cal-td' style='{bg}'><div style='height:30%; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:12px;' class='{day_cls}'>{day}</div><div style='height:70%; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:18px;' class='{text_cls}'>{s_lbl}</div></td>"
            html += "</tr>"
        st.markdown(html + "</table><br>", unsafe_allow_html=True)
        curr = (curr + timedelta(days=32)).replace(day=1)
