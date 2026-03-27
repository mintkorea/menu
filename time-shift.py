import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta, timezone
import calendar

# --- [1] 한국 표준시(KST) 및 기본 로직 (원본 소스 복구) ---
def get_kst():
    utc_now = datetime.now(timezone.utc)
    return utc_now + timedelta(hours=9)

now_kst = get_kst()
today_kst = now_kst.date()

# 근무 조 계산 (기준일: 2026-01-01 B조 시작)
ORDER = ["B", "C", "A"]
def get_shift(dt):
    base_date = date(2026, 1, 1)
    diff = (dt - base_date).days
    return ORDER[diff % 3]

# C조 상세 작업자 로직 (2/1 황재업-김태언-이태원-이정석 패턴 유지)
C_BASE = date(2026, 2, 1)
C_WORKERS_ORDER = [
    ("황재업", "김태언", "이태원", "이정석"), ("황재업", "김태언", "이정석", "이태원"),
    ("황재업", "이정석", "김태언", "이태원"), ("황재업", "이정석", "이태원", "김태언"),
    ("황재업", "이태원", "김태언", "이정석"), ("황재업", "이태원", "이정석", "김태언")
]

def get_c_details(dt):
    diff = (dt - C_BASE).days
    cycle_idx = (diff // 3) % 6
    return C_WORKERS_ORDER[cycle_idx]

# 시간대별 상세 업무
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

def find_idx(dt):
    m = dt.hour * 60 + dt.minute
    if dt.hour < 7: m += 1440
    for i, r in enumerate(SHIFT_DATA):
        sh, sm = map(int, r[0].split(':')); eh, em = map(int, r[1].split(':'))
        s = (sh+24 if sh<7 else sh)*60+sm
        e = (eh+24 if (eh<7 or (eh==7 and em==0)) and sh!=7 else eh)*60+em
        if s <= m < e: return i
    return -1

# --- [2] 페이지 설정 및 스타일 (상단 여백 및 버튼 복구) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 50px !important; max-width: 500px; margin: auto; }
    .main-title { text-align: center; font-size: 24px; font-weight: 900; color: #2E4077; margin-bottom: 5px; }
    .date-display { text-align: center; font-size: 18px; font-weight: 800; color: #d32f2f; margin-bottom: 20px; }
    
    /* 탭 디자인 */
    .stTabs [data-baseweb="tab-list"] { gap: 0px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; height: 45px; font-weight: 800; }
    
    /* 카드 디자인 (4명 노출용) */
    .status-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 12px 2px; text-align: center; background: white; }
    .w-name { font-size: 13px; color: #666; font-weight: 800; }
    .w-pos { font-size: 18px; color: #C04B41; font-weight: 900; }

    /* 테이블 */
    .c-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; }
    .c-table td, .c-table th { border: 1px solid #dee2e6; padding: 8px 1px; }
    .sun { color: #d32f2f !important; font-weight: bold; }
    .sat { color: #1976d2 !important; font-weight: bold; }

    /* 플로팅 버튼 */
    .top-btn {
        position: fixed; bottom: 80px; right: 20px; background-color: #2E4077; color: white;
        width: 50px; height: 50px; border-radius: 50%; display: flex;
        align-items: center; justify-content: center; font-size: 20px;
        text-decoration: none; z-index: 9999; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    </style>
    <a href="#" class="top-btn" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">▲</a>
    """, unsafe_allow_html=True)

# --- [3] 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    is_prep = (5 <= now_kst.hour < 7) or (now_kst.hour == 5 and now_kst.minute >= 30)
    w_date = today_kst if (now_kst.hour >= 7 or is_prep) else (today_kst - timedelta(days=1))
    
    # [복구] C조 상세 작업자 및 카드 4개 노출
    names = get_c_details(w_date)
    idx = find_idx(now_kst)
    
    st.markdown(f'''<div class="status-container">
        <div class="status-card"><div class="w-name">{names[0]} (조장)</div><div class="w-pos">{SHIFT_DATA[idx][2] if idx!=-1 else "대기"}</div></div>
        <div class="status-card"><div class="w-name">{names[1]} (성희)</div><div class="w-pos">{SHIFT_DATA[idx][3] if idx!=-1 else "대기"}</div></div>
        <div class="status-card"><div class="w-name">{names[2]} (의산A)</div><div class="w-pos">{SHIFT_DATA[idx][4] if idx!=-1 else "대기"}</div></div>
        <div class="status-card"><div class="w-name">{names[3]} (의산B)</div><div class="w-pos">{SHIFT_DATA[idx][5] if idx!=-1 else "대기"}</div></div>
    </div>''', unsafe_allow_html=True)

    # 전체 시간표 보기
    rows = "".join([f"<tr{' style=\"background:#FFE5E5;\"' if i==0 else ''}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(SHIFT_DATA[idx:] if idx!=-1 else [])])
    st.markdown(f'''<div class="table-container"><table class="c-table">
        <tr style="background:#f4f4f4; font-weight:bold;"><td colspan="2">시간</td><td colspan="2" style="background:#FFF2CC">성의회관</td><td colspan="2" style="background:#D9EAD3">의산연</td></tr>
        <tr style="background:#fff; font-weight:bold;"><td>From</td><td>To</td><td>{names[0]}</td><td>{names[1]}</td><td>{names[2]}</td><td>{names[3]}</td></tr>
        {rows}</table></div>''', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="main-title">📅 근무 일정 조회</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: start_d = st.date_input("시작일", today_kst)
    with c2: focus = st.selectbox("본인 강조", ["없음", "황재업", "김태언", "이태원", "이정석"])
    
    # [복구] 모든 날짜 출력 및 요일 색상
    html = '<div class="table-container"><table class="c-table"><tr style="background:#f8f9fa; font-weight:800;"><td>날짜</td><td>조장</td><td>성희</td><td>의산A</td><td>의산B</td></tr>'
    for i in range(35):
        d = start_d + timedelta(days=i)
        ws = get_c_details(d)
        wd = d.weekday()
        lbl = f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})"
        cls = "sun" if wd == 6 else ("sat" if wd == 5 else "")
        html += f'<tr><td class="{cls}">{lbl}</td>'
        for w in ws:
            bg = "#D9EAD3" if w == focus else ""
            html += f'<td style="background:{bg};">{w}</td>'
        html += '</tr>'
    st.markdown(html + '</table></div>', unsafe_allow_html=True)

with tab3:
    # --- [복구] 달력 생성 HTML (보내주신 소스 로직 100%) ---
    st.markdown('<div class="main-title">🏥 성의교정 근무달력</div>', unsafe_allow_html=True)
    
    def generate_calendar_html(start_dt):
        BASE_COLORS = {"A": "#FFE0B2", "B": "#FFCDD2", "C": "#BBDEFB"}
        STRONG_COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}
        html = "<style>.cal-table { width: 100%; border-collapse: collapse; text-align: center; table-layout: fixed; margin-bottom: 20px; } .cal-table td { border: 1px solid #eee; height: 50px; vertical-align: middle; } .sun { color: #d32f2f; } .sat { color: #1976d2; } </style>"
        
        curr = start_dt
        for _ in range(12):
            y, m = curr.year, curr.month
            cal = calendar.monthcalendar(y, m)
            html += f"<div style='text-align:center; font-weight:900; margin-top:15px;'>{y}년 {m}월</div><table class='cal-table'>"
            html += "<tr style='background:#f4f4f4;'><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
            for week in cal:
                html += "<tr>"
                for i, day in enumerate(week):
                    if day == 0: html += "<td></td>"
                    else:
                        d_obj = date(y, m, day)
                        s = get_shift(d_obj)
                        cls = "sun" if i == 0 else ("sat" if i == 6 else "")
                        html += f"<td style='background:{BASE_COLORS[s]};'><div class='{cls}'>{day}</div><div style='font-weight:bold;'>{s}</div></td>"
                html += "</tr>"
            html += "</table>"
            curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
        return html

    components.html(generate_calendar_html(today_kst.replace(day=1)), height=1500, scrolling=True)
