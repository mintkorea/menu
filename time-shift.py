import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 (탭 잘림 방지 및 여백 최적화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    /* 상단 여백 5mm 수준(20px) */
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    
    /* 탭 메뉴 잘림 방지: 너비 균등 배분 */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 2px; 
        margin-bottom: 15px; 
        display: flex; 
        justify-content: space-between;
    }
    .stTabs [data-baseweb="tab"] {
        flex-grow: 1;
        text-align: center;
        height: 42px; 
        background-color: #f0f2f6; 
        border-radius: 8px 8px 0 0;
        padding: 0 5px; 
        font-weight: 700; 
        font-size: 13px; /* 탭 글씨 크기 약간 줄임 */
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    
    .main-title { text-align: center; font-size: 19px; font-weight: 900; color: #2E4077; margin-bottom: 5px; }
    .date-display { text-align: center; font-size: 15px; color: #444; margin-bottom: 10px; font-weight: 800; }

    /* 실시간 카드 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-bottom: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 6px 2px; text-align: center; background: white; }
    .worker-name { font-size: 14px; font-weight: 800; }
    .status-val { font-size: 16px; font-weight: 900; color: #C04B41; }
    
    /* 공통 테이블 */
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 5px; margin-bottom: 20px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table td { border: 1px solid #dee2e6; padding: 8px 2px; }
    
    /* 달력 전용 스타일 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; margin-bottom: 40px; }
    .cal-td { border: 1px solid #eee; height: 55px; vertical-align: top; padding: 0 !important; }
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 14px; background: white; }
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; }
    .sun { color: #d32f2f !important; }
    .sat { color: #1976d2 !important; }
    .hi-text { color: white !important; }
    .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 정의 ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
PATTERN_START = date(2026, 3, 9)

def get_workers(target_date):
    if isinstance(target_date, datetime): target_date = target_date.date()
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    return ["C", "A", "B"][diff % 3]

if 'default_hi_shift' not in st.session_state:
    st.session_state.default_hi_shift = get_shift_simple(today_kst)

# --- [3] 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    is_prep = (5 <= now_kst.hour < 7) or (now_kst.hour == 5 and now_kst.minute >= 30)
    work_date = today_kst if (now_kst.hour >= 7 or is_prep) else (today_kst - timedelta(days=1))
    names = get_workers(work_date) or ("황재업", "김태언", "이태원", "이정석")
    
    # 시간표 데이터 (중략 - 기존과 동일)
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
    
    idx = find_idx(now_kst)
    st.markdown(f'''<div class="status-container">
        <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">{"대기" if idx == -1 else data_list[idx][2]}</div></div>
        <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">{"대기" if idx == -1 else data_list[idx][3]}</div></div>
        <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">{"대기" if idx == -1 else data_list[idx][4]}</div></div>
        <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">{"대기" if idx == -1 else data_list[idx][5]}</div></div>
    </div>''', unsafe_allow_html=True)
    
    if st.checkbox("🔄 전체 시간표", value=False):
        d_rows, hl = data_list, idx
    else:
        d_rows, hl = (data_list[idx:], 0) if idx != -1 else ([], -1)

    if d_rows:
        rows = "".join([f"<tr{' style=\"background:#FFE5E5;font-weight:bold;\"' if i==hl else ''}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(d_rows)])
        st.markdown(f'<div class="table-container"><table class="custom-table"><tr style="background:#f8f9fa;font-weight:800;"><td colspan="2">시간</td><td colspan="2">성의</td><td colspan="2">의산</td></tr>{rows}</table></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="main-title">📅 근무 편성표</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_date = st.date_input("시작", today_kst)
    with c2: focus = st.selectbox("강조", ["없음", "황재업", "김태언", "이태원", "이정석"])
    
    t_html = '<div class="table-container"><table class="custom-table"><tr style="background:#f8f9fa;font-weight:800;"><td>날짜</td><td>조장</td><td>성희</td><td>의산A</td><td>의산B</td></tr>'
    for i in range(21):
        d = s_date + timedelta(days=i)
        ws = get_workers(d)
        if ws[0]:
            wd = d.weekday()
            lbl = f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})"
            cls = "sun" if wd==6 else ("sat" if wd==5 else "")
            t_html += f'<tr><td class="{cls}">{lbl}</td>'
            for w in ws:
                bg = {"황재업":"#D9EAD3","김태언":"#FFF2CC","이태원":"#EAD1DC","이정석":"#C9DAF8"}.get(w,"") if w==focus else ""
                t_html += f'<td style="background:{bg};">{w}</td>'
            t_html += '</tr>'
    st.markdown(t_html + '</table></div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="main-title">🏥 근무달력 (12개월)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: offset = st.slider("📅 월 이동", -6, 6, 0)
    with c2: 
        opts = ["선택 안 함", "A", "B", "C"]
        hi = st.selectbox("🎯 강조", opts, index=opts.index(st.session_state.default_hi_shift))

    B_COLS = {"A":"#FFE0B2","B":"#FFCDD2","C":"#BBDEFB"}
    S_COLS = {"A":"#FB8C00","B":"#E53935","C":"#1E88E5"}
    
    cal_html = ""
    curr = (today_kst.replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
    
    for _ in range(12): # 12개월 조회
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        cal_html += f"<div style='text-align:center; font-weight:900; margin-bottom:10px;'>{y}년 {m}월</div>"
        cal_html += "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            cal_html += "<tr>"
            for i, day in enumerate(week):
                if day == 0: cal_html += "<td class='cal-td'></td>"
                else:
                    d_obj = date(y, m, day)
                    s = get_shift_simple(d_obj)
                    is_hi = (hi == s)
                    s_bg, d_bg = (S_COLS[s], S_COLS[s]) if is_hi else (B_COLS[s], "white")
                    td_cls = "today-border" if d_obj == today_kst else ""
                    cal_html += f"<td class='cal-td {td_cls}' style='background:{s_bg};'><div class='cal-date-part {('sun' if i==0 else 'sat' if i==6 else '') if not is_hi else 'hi-text'}' style='background:{d_bg};'>{day}</div><div class='cal-shift-part {'hi-text' if is_hi else ''}'>{s}</div></td>"
            cal_html += "</tr>"
        cal_html += "</table>"
        curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
    st.markdown(cal_html, unsafe_allow_html=True)
