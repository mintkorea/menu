import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date, timezone
import pytz
import calendar

# --- [1] 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.0rem !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; margin-bottom: 15px; }
    .stTabs [data-baseweb="tab"] {
        height: 42px; background-color: #f0f2f6; border-radius: 8px 8px 0 0;
        padding: 0 15px; font-weight: 700; font-size: 14px;
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    .main-title { text-align: center; font-size: 20px; font-weight: 900; color: #2E4077; margin-top: 5px; }
    
    /* 🕒 실시간 현황 날짜/시간 폰트 16px */
    .date-display { text-align: center; font-size: 16px; color: #444; margin-bottom: 15px; font-weight: 800; }

    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 12px; padding: 8px 5px; text-align: center; background: white; }
    .worker-name { font-size: 15px; font-weight: 800; color: #333; }
    .status-val { font-size: 17px; font-weight: 900; color: #C04B41; }
    
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 5px; margin-bottom: 20px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; background: white; }
    .custom-table th, .custom-table td { border: 1px solid #dee2e6; padding: 10px 2px; }
    .header-main { background-color: #f8f9fa !important; font-weight: 800; }
    
    .sat { color: blue !important; font-weight: bold; }
    .sun { color: red !important; font-weight: bold; }
    
    /* 개인별 고유 색상 */
    .color-hwang { background-color: #D9EAD3 !important; font-weight: bold; } 
    .color-kim { background-color: #FFF2CC !important; font-weight: bold; }   
    .color-won { background-color: #EAD1DC !important; font-weight: bold; }   
    .color-lee { background-color: #C9DAF8 !important; font-weight: bold; }   
    
    .highlight-row { background-color: #FFE5E5 !important; font-weight: bold; color: #C04B41; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 (시간 및 근무조) ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()

# 근무 패턴 기준일 (이미지 기반: 2026-03-09 황재업 조장 시작일)
PATTERN_START = date(2026, 3, 9)

def get_workers(target_date):
    if isinstance(target_date, datetime):
        target_date = target_date.date()
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

# 달력용 간단 조 판별 (C조 기준)
def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    return "C" if diff % 3 == 0 else ("A" if diff % 3 == 1 else "B")

# 세션 상태 초기화
if 'default_shift' not in st.session_state:
    st.session_state.default_shift = get_shift_simple(today_kst)

# --- [3] UI 출력 ---
tab1, tab2, tab3 = st.tabs(["🕒 실시간 현황", "📅 근무 일정 조회", "🏥 근무달력"])

# [탭 1: 실시간 현황]
with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    is_prep = (5 <= now_kst.hour < 7) or (now_kst.hour == 5 and now_kst.minute >= 30)
    work_date = today_kst if (now_kst.hour >= 7 or is_prep) else (today_kst - timedelta(days=1))
    names = get_workers(work_date) or ("황재업", "김태언", "이태원", "이정석")
    
    # 시간표 데이터 생략 (동일)
    data_list = [["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"], ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"], ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"], ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"], ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"], ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"], ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"], ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"], ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"], ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"], ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"], ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"]]
    
    def find_idx(dt):
        m = dt.hour * 60 + dt.minute
        if dt.hour < 7: m += 1440
        for i, r in enumerate(data_list):
            sh, sm = map(int, r[0].split(':'))
            eh, em = map(int, r[1].split(':'))
            s, e = (sh+24 if sh<7 else sh)*60+sm, (eh+24 if (eh<7 or (eh==7 and em==0)) and sh!=7 else eh)*60+em
            if s <= m < e: return i
        return -1
    curr_idx = find_idx(now_kst)

    st.markdown(f'''<div class="status-container">
        <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">{"대기" if curr_idx == -1 else data_list[curr_idx][2]}</div></div>
        <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">{"대기" if curr_idx == -1 else data_list[curr_idx][3]}</div></div>
        <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">{"대기" if curr_idx == -1 else data_list[curr_idx][4]}</div></div>
        <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">{"대기" if curr_idx == -1 else data_list[curr_idx][5]}</div></div>
    </div>''', unsafe_allow_html=True)
    
    show_all = st.checkbox("🔄 전체 시간표 보기", value=False)
    if show_all:
        d_rows, hl = data_list.copy(), curr_idx
    else:
        d_rows, hl = (data_list[curr_idx:], 0) if curr_idx != -1 else ([], -1)

    rows_html = "".join([f"<tr{' class=\"highlight-row\"' if i == hl and hl != -1 else ''}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(d_rows)])
    if d_rows:
        st.markdown(f"""<div class="table-container"><table class="custom-table">
            <thead><tr class="header-main"><th colspan="2">시간</th><th colspan="2" style="background:#FFF2CC">성의회관</th><th colspan="2" style="background:#D9EAD3">의산연</th></tr>
            <tr style="background:#fff; font-weight:700;"><td>From</td><td>To</td><td>{names[0]}</td><td>{names[1]}</td><td>{names[2]}</td><td>{names[3]}</td></tr></thead>
            <tbody>{rows_html}</tbody></table></div>""", unsafe_allow_html=True)

# [탭 2: 근무 일정 조회]
with tab2:
    st.markdown('<div class="main-title">📅 근무 일정 조회</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: s_date = st.date_input("시작 날짜", today_kst)
    with col2: focus_name = st.selectbox("본인 강조", ["없음", "황재업", "김태언", "이태원", "이정석"])
    view_days = st.slider("조회 기간 (일)", 7, 60, 31)

    def get_color_class(name):
        return {"황재업": "color-hwang", "김태언": "color-kim", "이태원": "color-won", "이정석": "color-lee"}.get(name, "")

    table_html = """<div class="table-container"><table class="custom-table">
                    <thead><tr class="header-main"><th>날짜(요일)</th><th>조장</th><th>성희</th><th>의산A</th><th>의산B</th></tr></thead><tbody>"""
    for i in range(view_days):
        d = s_date + timedelta(days=i)
        workers = get_workers(d)
        if workers[0]:
            wd_idx = d.weekday()
            date_label = f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd_idx]})"
            date_cls = "sun" if wd_idx == 6 else ("sat" if wd_idx == 5 else "")
            table_html += f"<tr><td class='{date_cls}'>{date_label}</td>"
            for w in workers:
                f_cls = get_color_class(w) if w == focus_name else ""
                table_html += f"<td class='{f_cls}'>{w}</td>"
            table_html += "</tr>"
    st.markdown(table_html + "</tbody></table></div>", unsafe_allow_html=True)

# [탭 3: 근무달력]
with tab3:
    st.markdown('<div class="main-title">🏥 성의교정 근무달력</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: offset = st.slider("📅 기준월 변경", -12, 12, 0)
    with c2: hi_shift = st.selectbox("🎯 강조 조", ["선택 안 함", "A", "B", "C"], index=["선택 안 함", "A", "B", "C"].index(st.session_state.default_shift))

    def generate_cal_html(start_dt, highlight):
        COLORS = {"A": "#FFE0B2", "B": "#FFCDD2", "C": "#BBDEFB"}
        STRONGS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}
        html = "<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; font-family: sans-serif;'>"
        curr = start_dt
        for _ in range(3): # 3개월씩 표시
            y, m = curr.year, curr.month
            cal = calendar.monthcalendar(y, m)
            html += f"<div style='border:1px solid #eee; padding:10px;'><h4>{y}년 {m}월</h4><table style='width:100%; border-collapse:collapse; text-align:center;'>"
            html += "<tr><th style='color:red'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th style='color:blue'>토</th></tr>"
            for week in cal:
                html += "<tr>"
                for i, day in enumerate(week):
                    if day == 0: html += "<td></td>"
                    else:
                        d_obj = date(y, m, day)
                        s = get_shift_simple(d_obj)
                        is_hi = (highlight == s)
                        bg = STRONGS[s] if is_hi else COLORS[s]
                        border = "3px solid #333" if d_obj == today_kst else "1px solid #f2f2f2"
                        html += f"<td style='background:{bg}; border:{border}; padding:5px;'><div style='font-size:10px;'>{day}</div><div style='font-weight:900;'>{s}</div></td>"
                html += "</tr>"
            html += "</table></div>"
            curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
        return html + "</div>"

    cal_start = (today_kst.replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
    st.markdown(generate_cal_html(cal_start, hi_shift), unsafe_allow_html=True)
