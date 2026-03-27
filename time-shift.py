import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 (지시사항 100% 반영) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 40px !important; max-width: 500px; margin: auto; }
    
    /* 탭 스타일 고정 */
    .stTabs [data-baseweb="tab-list"] { gap: 0px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] {
        flex: 1; text-align: center; height: 45px; 
        background-color: #f0f2f6; padding: 0px !important; 
        font-weight: 800; font-size: 15px !important; 
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    
    /* 타이틀 및 날짜 (크게 노출) */
    .main-title { text-align: center; font-size: 24px; font-weight: 900; color: #2E4077; margin-top: 10px; }
    .date-box { text-align: center; font-size: 18px; font-weight: 800; color: #d32f2f; margin-bottom: 20px; border: 1px solid #ddd; padding: 5px; border-radius: 5px; }

    /* 현황판 카드 (4개 명확히 노출) */
    .status-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 12px 5px; text-align: center; background: #fff; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .w-name { font-size: 14px; font-weight: 800; color: #444; margin-bottom: 4px; }
    .w-pos { font-size: 18px; font-weight: 900; color: #C04B41; }

    /* 테이블 및 요일 색상 */
    .table-container { width: 100%; overflow-x: auto; }
    .c-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .c-table td, .c-table th { border: 1px solid #dee2e6; padding: 10px 2px; }
    .sun { color: #d32f2f !important; font-weight: bold; }
    .sat { color: #1976d2 !important; font-weight: bold; }

    /* 플로팅 탑 버튼 위치 */
    #topBtn {
        position: fixed; bottom: 90px; right: 20px; z-index: 999;
        width: 50px; height: 50px; background: #2E4077; color: white;
        border: none; border-radius: 50%; font-size: 20px; cursor: pointer;
    }
    </style>
    <button onclick="window.scrollTo({top: 0, behavior: 'smooth'})" id="topBtn">▲</button>
    """, unsafe_allow_html=True)

# --- [2] 로직 (엑셀 원본 데이터 무조건 유지) ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()

# 엑셀 첫 줄 기준: 2026-02-01(일) / 조장-성의-의산A-의산B 순서
BASE_DATE = date(2026, 2, 1)
WORKERS_ORDER = [
    ("황재업", "김태언", "이태원", "이정석"), # 2/1
    ("황재업", "김태언", "이정석", "이태원"), # 2/4
    ("황재업", "이정석", "김태언", "이태원"), # 2/7
    ("황재업", "이정석", "이태원", "김태언"), # 2/10
    ("황재업", "이태원", "김태언", "이정석"), # 2/13
    ("황재업", "이태원", "이정석", "김태언")  # 2/16
]

def get_actual_workers(target_date):
    diff = (target_date - BASE_DATE).days
    day_idx = diff % 3
    # 3일마다 다음 순번으로 (6개 세트 순환)
    cycle_idx = (diff // 3) % 6
    names = WORKERS_ORDER[cycle_idx]
    return names, ["C", "A", "B"][day_idx]

# 시간표 데이터 (고정)
SHIFT_DATA = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"],
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"],
    ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"],
    ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"],
    ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"],
    ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"],
    ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"],
    ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"],
    ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"]
]

def find_curr_idx(dt):
    m = dt.hour * 60 + dt.minute
    if dt.hour < 7: m += 1440
    for i, r in enumerate(SHIFT_DATA):
        sh, sm = map(int, r[0].split(':')); eh, em = map(int, r[1].split(':'))
        s = (sh+24 if sh<7 else sh)*60+sm
        e = (eh+24 if (eh<7 or (eh==7 and em==0)) and sh!=7 else eh)*60+em
        if s <= m < e: return i
    return -1

# --- [3] 화면 구성 ---
t1, t2, t3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with t1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-box">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    is_prep = (5 <= now_kst.hour < 7) or (now_kst.hour == 5 and now_kst.minute >= 30)
    w_date = today_kst if (now_kst.hour >= 7 or is_prep) else (today_kst - timedelta(days=1))
    names, _ = get_actual_workers(w_date)
    idx = find_curr_idx(now_kst)
    
    st.markdown(f'''<div class="status-grid">
        <div class="status-card"><div class="w-name">{names[0]} (조장)</div><div class="w-pos">{SHIFT_DATA[idx][2] if idx!=-1 else "-"}</div></div>
        <div class="status-card"><div class="w-name">{names[1]} (성희)</div><div class="w-pos">{SHIFT_DATA[idx][3] if idx!=-1 else "-"}</div></div>
        <div class="status-card"><div class="w-name">{names[2]} (의산A)</div><div class="w-pos">{SHIFT_DATA[idx][4] if idx!=-1 else "-"}</div></div>
        <div class="status-card"><div class="w-name">{names[3]} (의산B)</div><div class="w-pos">{SHIFT_DATA[idx][5] if idx!=-1 else "-"}</div></div>
    </div>''', unsafe_allow_html=True)

    rows = "".join([f"<tr{' style=\"background:#FFE5E5;\"' if i==0 else ''}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(SHIFT_DATA[idx:] if idx!=-1 else [])])
    st.markdown(f'''<div class="table-container"><table class="c-table">
        <tr style="background:#f4f4f4; font-weight:bold;"><td colspan="2">시간</td><td colspan="2" style="background:#FFF2CC">성의회관</td><td colspan="2" style="background:#D9EAD3">의산연</td></tr>
        <tr style="background:#fff; font-weight:bold;"><td>From</td><td>To</td><td>{names[0]}</td><td>{names[1]}</td><td>{names[2]}</td><td>{names[3]}</td></tr>
        {rows}</table></div>''', unsafe_allow_html=True)

with t2:
    st.markdown('<div class="main-title">📅 근무 일정 조회</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: start_d = st.date_input("시작일", today_kst)
    with c2: highlight = st.selectbox("강조", ["없음", "황재업", "김태언", "이태원", "이정석"])
    
    html = '<div class="table-container"><table class="c-table"><tr style="background:#f8f9fa; font-weight:800;"><td>날짜</td><td>조장</td><td>성희</td><td>의산A</td><td>의산B</td></tr>'
    for i in range(45):
        d = start_d + timedelta(days=i)
        ws, _ = get_actual_workers(d)
        wd = d.weekday()
        lbl = f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})"
        cls = "sun" if wd == 6 else ("sat" if wd == 5 else "")
        html += f'<tr><td class="{cls}">{lbl}</td>'
        for w in ws:
            bg = "#D9EAD3" if w == highlight else ""
            html += f'<td style="background:{bg};">{w}</td>'
        html += '</tr>'
    st.markdown(html + '</table></div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="main-title">🏥 12개월 근무달력</div>', unsafe_allow_html=True)
    B_COLS = {"A":"#FFE0B2", "B":"#FFCDD2", "C":"#BBDEFB"}
    curr = today_kst.replace(day=1)
    for _ in range(12):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        st.markdown(f"<div style='text-align:center; font-weight:900; margin-top:10px;'>{y}년 {m}월</div>", unsafe_allow_html=True)
        ch = "<table class='c-table' style='margin-bottom:20px;'><tr style='background:#f4f4f4;'><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            ch += "<tr>"
            for i, day in enumerate(week):
                if day == 0: ch += "<td></td>"
                else:
                    d_obj = date(y, m, day)
                    _, sl = get_actual_workers(d_obj)
                    cls = "sun" if i==0 else ("sat" if i==6 else "")
                    ch += f"<td style='background:{B_COLS[sl]}; height:45px;'><div class='{cls}'>{day}</div><b>{sl}</b></td>"
            ch += "</tr>"
        st.markdown(ch + "</table>", unsafe_allow_html=True)
        curr = (curr + timedelta(days=32)).replace(day=1)
