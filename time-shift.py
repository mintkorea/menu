import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

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
    
    /* 개인별 고유 색상 (이미지 기반) */
    .color-hwang { background-color: #D9EAD3 !important; font-weight: bold; } 
    .color-kim { background-color: #FFF2CC !important; font-weight: bold; }   
    .color-won { background-color: #EAD1DC !important; font-weight: bold; }   
    .color-lee { background-color: #C9DAF8 !important; font-weight: bold; }   
    
    .highlight-row { background-color: #FFE5E5 !important; font-weight: bold; color: #C04B41; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

today = now.date()
is_prep = (5 <= now.hour < 7) or (now.hour == 5 and now.minute >= 30)
work_date = today if (now.hour >= 7 or is_prep) else (today - timedelta(days=1))
names = get_workers(work_date) or ("황재업", "김태언", "이태원", "이정석")

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
curr_idx = find_idx(now)

# --- [3] UI 출력 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    st.markdown(f'''<div class="status-container">
        <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">{"대기" if curr_idx == -1 else data_list[curr_idx][2]}</div></div>
        <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">{"대기" if curr_idx == -1 else data_list[curr_idx][3]}</div></div>
        <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">{"대기" if curr_idx == -1 else data_list[curr_idx][4]}</div></div>
        <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">{"대기" if curr_idx == -1 else data_list[curr_idx][5]}</div></div>
    </div>''', unsafe_allow_html=True)
    
    show_all = st.checkbox("🔄 전체 시간표 보기", value=False)
    
    # 🕒 로직 수정: 현재 시간 이전은 숨기고 이후 시간만 표시
    if show_all:
        d_rows = data_list.copy()
        hl = curr_idx
    else:
        # 현재 시간 인덱스부터 끝까지의 데이터만 슬라이싱
        if curr_idx != -1:
            d_rows = data_list[curr_idx:]
            hl = 0 # 슬라이싱된 리스트에서 현재 시간은 항상 0번 인덱스
        else:
            d_rows = [] # 근무 시간 외
            hl = -1

    rows_html = "".join([f"<tr{' class=\"highlight-row\"' if i == hl and hl != -1 else ''}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(d_rows)])
    
    if d_rows:
        st.markdown(f"""<div class="table-container"><table class="custom-table">
            <thead><tr class="header-main"><th colspan="2">시간</th><th colspan="2" style="background:#FFF2CC">성의회관</th><th colspan="2" style="background:#D9EAD3">의산연</th></tr>
            <tr style="background:#fff; font-weight:700;"><td>From</td><td>To</td><td>{names[0]}</td><td>{names[1]}</td><td>{names[2]}</td><td>{names[3]}</td></tr></thead>
            <tbody>{rows_html}</tbody></table></div>""", unsafe_allow_html=True)
    else:
        st.info("현재는 근무 시간이 아닙니다.")

with tab2:
    st.markdown('<div class="main-title">📅 근무 일정 조회</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: s_date = st.date_input("시작 날짜", today)
    with col2: focus_name = st.selectbox("본인 강조", ["없음", "황재업", "김태언", "이태원", "이정석"])
    view_days = st.slider("조회 기간 (일)", 7, 60, 31)

    def get_color_class(name):
        if name == "황재업": return "color-hwang"
        if name == "김태언": return "color-kim"
        if name == "이태원": return "color-won"
        if name == "이정석": return "color-lee"
        return ""

    table_html = """<div class="table-container"><table class="custom-table">
                    <thead><tr class="header-main"><th>날짜(요일)</th><th>조장</th><th>성희</th><th>의산A</th><th>의산B</th></tr></thead><tbody>"""
    
    for i in range(view_days):
        d = s_date + timedelta(days=i)
        workers = get_workers(d)
        if workers[0]:
            wd_idx = d.weekday()
            wd_str = ['월','화','수','목','금','토','일'][wd_idx]
            date_label = f"{d.strftime('%m/%d')}({wd_str})"
            date_cls = "sun" if wd_idx == 6 else ("sat" if wd_idx == 5 else "")
            
            table_html += f"<tr><td class='{date_cls}'>{date_label}</td>"
            for w in workers:
                f_cls = get_color_class(w) if w == focus_name else ""
                table_html += f"<td class='{f_cls}'>{w}</td>"
            table_html += "</tr>"
            
    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)
