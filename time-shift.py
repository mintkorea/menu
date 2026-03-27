import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 (UI 디테일 수정) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    /* [수정] 탭 상단 잘림 방지: 여백을 20px -> 40px로 확대 */
    .block-container { padding-top: 40px !important; max-width: 500px; margin: auto; }
    
    /* 탭 메뉴 스타일 */
    .stTabs [data-baseweb="tab-list"] { gap: 0px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] {
        flex: 1; text-align: center; height: 40px; 
        background-color: #f0f2f6; padding: 0px !important; 
        font-weight: 800; font-size: 12px !important; 
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    
    /* 현황판 카드 스타일 (일부 미노출 방지: 여백 및 높이 조정) */
    .status-card {
        border: 2px solid #2E4077; border-radius: 10px; padding: 8px 2px; 
        text-align: center; background: white; min-height: 60px;
    }

    /* 테이블 스타일 */
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 5px; overflow-x: auto; margin-bottom: 20px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 11px; text-align: center; table-layout: fixed; }
    .custom-table td, .custom-table th { border: 1px solid #dee2e6; padding: 8px 1px; }

    /* [수정] 플로팅 탑 버튼 위치 위로 조정 (bottom: 20px -> 70px) */
    #scrollToTopBtn {
        position: fixed; bottom: 70px; right: 20px; z-index: 99;
        width: 45px; height: 45px; background-color: #2E4077; color: white;
        border: none; border-radius: 50%; cursor: pointer; font-weight: bold; font-size: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    </style>
    
    <button onclick="window.scrollTo({top: 0, behavior: 'smooth'})" id="scrollToTopBtn">▲</button>
    """, unsafe_allow_html=True)

# --- [2] 로직 정의 (KeyError 방지) ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
PATTERN_START = date(2026, 3, 9)

DATA_LIST = [
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
    for i, r in enumerate(DATA_LIST):
        sh, sm = map(int, r[0].split(':')); eh, em = map(int, r[1].split(':'))
        s = (sh+24 if sh<7 else sh)*60+sm
        e = (eh+24 if (eh<7 or (eh==7 and em==0)) and sh!=7 else eh)*60+em
        if s <= m < e: return i
    return -1

def get_workers(target_date):
    # 패턴 주기 계산 (3일 주기)
    diff = (target_date - PATTERN_START).days
    day_idx = diff % 3
    if day_idx == 0: # C조 근무일
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return ("황재업", "김태언", "이정석", "이태원") if i2 else ("황재업", "김태언", "이태원", "이정석")
        elif ci == 1: return ("황재업", "이정석", "이태원", "김태언") if i2 else ("황재업", "이정석", "김태언", "이태원")
        else: return ("황재업", "이태원", "이정석", "김태언") if i2 else ("황재업", "이태원", "김태언", "이정석")
    return ("-", "-", "-", "-") # 근무일이 아닐 경우 예외 처리

def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    return ["C", "A", "B"][diff % 3]

# --- [3] 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown(f'<div style="text-align:center; font-size:14px; color:#666; margin-bottom:10px;">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    is_prep = (5 <= now_kst.hour < 7) or (now_kst.hour == 5 and now_kst.minute >= 30)
    work_date = today_kst if (now_kst.hour >= 7 or is_prep) else (today_kst - timedelta(days=1))
    names = get_workers(work_date)
    
    idx = find_idx(now_kst)
    
    # [수정] 카드 일부 미노출 방지를 위한 그리드 레이아웃
    st.markdown(f'''<div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; margin-bottom:15px;">
        <div class="status-card">
            <div style="font-size:12px; font-weight:800; color:#333;">{names[0]}</div>
            <div style="font-size:16px; font-weight:900; color:#C04B41;">{DATA_LIST[idx][2] if idx != -1 else "대기"}</div>
        </div>
        <div class="status-card">
            <div style="font-size:12px; font-weight:800; color:#333;">{names[1]}</div>
            <div style="font-size:16px; font-weight:900; color:#C04B41;">{DATA_LIST[idx][3] if idx != -1 else "대기"}</div>
        </div>
    </div>''', unsafe_allow_html=True)

    if st.checkbox("🔄 전체 시간표 보기", value=False):
        d_rows, hl = DATA_LIST, idx
    else:
        d_rows, hl = (DATA_LIST[idx:], 0) if idx != -1 else ([], -1)

    if d_rows:
        rows = "".join([f"<tr{' style=\"background:#FFE5E5;font-weight:bold;\"' if i==hl else ''}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(d_rows)])
        st.markdown(f'''<div class="table-container"><table class="custom-table">
            <tr style="background:#f4f4f4; font-weight:bold;"><td colspan="2">시간</td><td colspan="2" style="background:#FFF2CC">성의회관</td><td colspan="2" style="background:#D9EAD3">의산연</td></tr>
            <tr style="background:#fff; font-weight:bold;"><td>From</td><td>To</td><td>{names[0]}</td><td>{names[1]}</td><td>{names[2]}</td><td>{names[3]}</td></tr>
            {rows}</table></div>''', unsafe_allow_html=True)

with tab2:
    st.markdown('<div style="text-align:center; font-size:18px; font-weight:900; color:#2E4077; margin-bottom:10px;">📅 근무 일정 조회</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_date = st.date_input("시작 날짜", today_kst, key="s_date")
    with c2: focus = st.selectbox("본인 강조", ["없음", "황재업", "김태언", "이태원", "이정석"])
    
    range_val = st.slider("조회 기간 (일)", 7, 60, 21)
    
    t_html = '<div class="table-container"><table class="custom-table"><tr style="background:#f8f9fa; font-weight:800;"><td>날짜</td><td>조장</td><td>성희</td><td>의산A</td><td>의산B</td></tr>'
    for i in range(range_val):
        d = s_date + timedelta(days=i)
        ws = get_workers(d)
        wd = d.weekday()
        lbl = f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})"
        cls = "sun" if wd == 6 else ("sat" if wd == 5 else "")
        t_html += f'<tr><td class="{cls}">{lbl}</td>'
        for w in ws:
            bg = {"황재업":"#D9EAD3","김태언":"#FFF2CC","이태원":"#EAD1DC","이정석":"#C9DAF8"}.get(w,"") if w == focus else ""
            t_html += f'<td style="background:{bg};">{w}</td>'
        t_html += '</tr>'
    st.markdown(t_html + '</table></div>', unsafe_allow_html=True)

with tab3:
    # --- 달력 (12개월 로직) ---
    st.markdown('<div style="text-align:center; font-size:18px; font-weight:900; color:#2E4077; margin-bottom:10px;">🏥 성의교정 근무달력</div>', unsafe_allow_html=True)
    # (이하 12개월 달력 코드 동일...)
    # ...
