import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 페이지 설정 및 스타일 (UI 가림 방지) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; max-width: 500px; margin: auto; }
    
    /* 탭 디자인 */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; margin-bottom: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 40px; background-color: #f0f2f6; border-radius: 8px 8px 0 0;
        padding: 0 15px; font-weight: 700; font-size: 14px;
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }

    /* 상태 카드 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 12px; padding: 10px 5px; text-align: center; background: white; }
    .worker-name { font-size: 13px; font-weight: 700; color: #555; }
    .status-val { font-size: 17px; font-weight: 900; color: #C04B41; }
    
    /* 실시간 테이블 스크롤 및 높이 */
    .table-scroll-container { 
        width: 100%; 
        max-height: 420px; 
        overflow-y: auto; 
        border: 1px solid #dee2e6;
        border-radius: 5px;
    }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table th, .custom-table td { border: 1px solid #dee2e6; padding: 10px 1px; }
    
    .custom-table thead { position: sticky; top: 0; z-index: 10; background: white; }
    .header-main { background-color: #f8f9fa !important; font-weight: 800; }
    .header-sub-seong { background-color: #FFF2CC !important; font-weight: 700; color: #856404; }
    .header-sub-uisan { background-color: #D9EAD3 !important; font-weight: 700; color: #274e13; }
    
    .highlight-row { background-color: #FFE5E5 !important; font-weight: bold; color: #C04B41; }
    .ready-msg { text-align: center; padding: 8px; background: #EEF2FF; border-radius: 8px; border: 1px solid #2E4077; margin-bottom: 10px; font-weight: 700; color: #2E4077; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜 및 패턴 로직 ---
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
names = get_workers(work_date)
if names[0] is None: names = ("황재업", "김태언", "이태원", "이정석")

# --- [3] 실시간 데이터 ---
data = [
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
    for i, r in enumerate(data):
        sh, sm = map(int, r[0].split(':'))
        eh, em = map(int, r[1].split(':'))
        s = (sh + 24 if sh < 7 else sh) * 60 + sm
        e = (eh + 24 if (eh < 7 or (eh == 7 and em == 0)) and sh != 7 else eh) * 60 + em
        if s <= m < e: return i
    return -1

curr_idx = find_idx(now)

# --- [4] UI 출력 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown(f'<p style="text-align:right; font-size:11px; color:gray; margin-bottom:5px;">{now.strftime("%m/%d %H:%M")}</p>', unsafe_allow_html=True)
    st.markdown(f'''
    <div class="status-container">
        <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">{"대기" if curr_idx == -1 else data[curr_idx][2]}</div></div>
        <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">{"대기" if curr_idx == -1 else data[curr_idx][3]}</div></div>
        <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">{"대기" if curr_idx == -1 else data[curr_idx][4]}</div></div>
        <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">{"대기" if curr_idx == -1 else data[curr_idx][5]}</div></div>
    </div>
    ''', unsafe_allow_html=True)

    if curr_idx == -1 and is_prep:
        st.markdown('<div class="ready-msg">☕ 07:00 근무 시작 (교대 준비 중)</div>', unsafe_allow_html=True)

    show_all = st.checkbox("🔄 전체 시간표 보기", value=False)

    display_rows = data.copy()
    hl = curr_idx
    if not show_all and curr_idx != -1:
        display_rows = [data[curr_idx]] + [r for i, r in enumerate(data) if i != curr_idx]
        hl = 0
    elif curr_idx == -1: hl = -1

    rows_html = "".join([f"<tr{' class=\"highlight-row\"' if i == hl and hl != -1 else ''}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(display_rows)])

    st.markdown(f"""
    <div class="table-scroll-container">
        <table class="custom-table">
            <thead>
                <tr class="header-main">
                    <th colspan="2">시간</th>
                    <th colspan="2" class="header-sub-seong">성의회관</th>
                    <th colspan="2" class="header-sub-uisan">의산연</th>
                </tr>
                <tr style="background:#fff; font-weight:700;">
                    <td style="width:18%;">From</td><td style="width:18%;">To</td>
                    <td class="header-sub-seong">{names[0]}</td><td class="header-sub-seong">{names[1]}</td>
                    <td class="header-sub-uisan">{names[2]}</td><td class="header-sub-uisan">{names[3]}</td>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📅 향후 31일 근무 일정")
    cal_list = []
    for i in range(31):
        d = today + timedelta(days=i)
        w1, w2, w3, w4 = get_workers(d)
        if w1:
            wd = ['월','화','수','목','금','토','일'][d.weekday()]
            cal_list.append({"날짜": d.strftime('%m/%d'), "요일": wd, "조장": w1, "성희": w2, "의산A": w3, "의산B": w4})
    
    if cal_list:
        df = pd.DataFrame(cal_list)
        # 요일별 색상 적용을 위한 스타일링
        def color_day(val):
            if val == '일': return 'color: red; font-weight: bold'
            if val == '토': return 'color: blue; font-weight: bold'
            return ''
        
        st.dataframe(df.style.applymap(color_day, subset=['요일']), use_container_width=True, hide_index=True)
    else:
        st.warning("편성표 데이터를 불러올 수 없습니다.")
