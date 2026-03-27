import streamlit as st
from datetime import datetime, date, timedelta, timezone
import calendar

# 1. 로직 및 시간 설정 (건드리지 않음)
def get_kst():
    return datetime.now(timezone(timedelta(hours=9)))

now_kst = get_kst()
today_kst = now_kst.date()

def get_shift_label(dt):
    return ["B", "C", "A"][(dt - date(2026, 1, 1)).days % 3]

PATTERN = [
    ("황재업", "김태언", "이태원", "이정석"), ("황재업", "김태언", "이정석", "이태원"),
    ("황재업", "이정석", "김태언", "이태원"), ("황재업", "이정석", "이태원", "김태언"),
    ("황재업", "이태원", "김태언", "이정석"), ("황재업", "이태원", "이정석", "김태언")
]

def get_base_workers(dt):
    diff = (dt - date(2026, 3, 27)).days
    return list(PATTERN[diff % 6])

def apply_vacation(workers, v_name):
    if not v_name or v_name == "없음": return workers
    ldr, sung, ui_a, ui_b = workers
    if v_name == sung: return [ldr, "연차(조장대근)", ui_a, ui_b]
    if v_name == ui_a: return [ldr, ldr, "연차(성의이동)", ui_b]
    if v_name == ui_b: return [ldr, ldr, ui_a, "연차(성의이동)"]
    return workers

# 2. 스타일 설정 (큼직한 글씨 + 셸 전체 배색)
st.set_page_config(page_title="C조 근무 시스템", layout="wide")
st.markdown("""
    <style>
    .block-container { padding: 10px !important; max-width: 450px; margin: auto; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 10px; text-align: center; background: white; margin-bottom: 10px; }
    
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ddd; }
    .cal-td { border: 1px solid #fff; height: 65px; vertical-align: middle; padding: 0 !important; text-align: center; }
    
    .date-num { font-size: 11px; font-weight: 700; display: block; }
    .shift-name { font-size: 24px; font-weight: 900; display: block; } /* 글자 크기 시원하게 확대 */
    
    .sun { color: #d32f2f; } .sat { color: #1976d2; }
    .today-border { border: 3px solid #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. 화면 출력 (탭 없이 순서대로 나열)
st.markdown("<h3 style='text-align:center;'>🛡️ 실시간 근무 현황</h3>", unsafe_allow_html=True)
v_person = st.selectbox("🏥 연차자 선택", ["없음", "김태언", "이정석", "이태원"])
w_date = today_kst if now_kst.hour >= 7 else (today_kst - timedelta(days=1))
final = apply_vacation(get_base_workers(w_date), v_person)

st.markdown(f'''
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
    <div class="status-card"><small>조장</small><br><b>{final[0]}</b></div>
    <div class="status-card"><small>성의회관</small><br><b style="color:red;">{final[1]}</b></div>
    <div class="status-card"><small>의산A</small><br><b>{final[2]}</b></div>
    <div class="status-card"><small>의산B</small><br><b>{final[3]}</b></div>
</div>
''', unsafe_allow_html=True)

st.write("---")

st.markdown("<h3 style='text-align:center;'>🏥 성의교정 근무달력</h3>", unsafe_allow_html=True)
hi = st.selectbox("🎯 강조할 조 선택", ["없음", "A", "B", "C"], index=3)

COLOR_MAP = {
    "A": {"bg": "#FFF4E5", "hi": "#FB8C00", "txt": "#FB8C00"},
    "B": {"bg": "#FFEBEE", "hi": "#E53935", "txt": "#E53935"},
    "C": {"bg": "#E3F2FD", "hi": "#1E88E5", "txt": "#1E88E5"}
}

curr = today_kst.replace(day=1)
for _ in range(2):
    y, m = curr.year, curr.month
    cal = calendar.monthcalendar(y, m)
    st.markdown(f"<div style='text-align:center; font-weight:bold; margin-top:10px;'>{y}년 {m}월</div>", unsafe_allow_html=True)
    html = "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
    for week in cal:
        html += "<tr>"
        for i, day in enumerate(week):
            if day == 0: html += "<td style='background:#f4f4f4;'></td>"
            else:
                d_obj = date(y, m, day)
                s_lbl = get_shift_label(d_obj)
                is_hi = (hi == s_lbl)
                
                # 셸 전체 배경색 (강조 시 진하게, 평소엔 연하게)
                bg = COLOR_MAP[s_lbl]["hi"] if is_hi else COLOR_MAP[s_lbl]["bg"]
                t_color = "#fff" if is_hi else COLOR_MAP[s_lbl]["txt"]
                d_color = "#fff" if is_hi else ("#d32f2f" if i==0 else ("#1976d2" if i==6 else "#333"))
                
                today_cls = "today-border" if d_obj == today_kst else ""
                html += f"""
                <td class='cal-td {today_cls}' style='background-color:{bg};'>
                    <span class='date-num' style='color:{d_color};'>{day}</span>
                    <span class='shift-name' style='color:{t_color};'>{s_lbl}</span>
                </td>"""
        html += "</tr>"
    st.markdown(html + "</table>", unsafe_allow_html=True)
    curr = (curr + timedelta(days=32)).replace(day=1)
