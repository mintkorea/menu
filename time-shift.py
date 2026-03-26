import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        height: 40px; background-color: #f0f2f6; border-radius: 8px 8px 0 0;
        padding: 0 20px; font-weight: 700; color: #333 !important;
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 14px !important; text-align: center; margin-bottom: 15px; color: #666; }
    
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }
    .status-card { border: 2px solid #2E4077; border-radius: 12px; padding: 12px 5px; text-align: center; background: white; }
    .worker-name { font-size: 14px !important; font-weight: 700; color: #555; }
    .status-val { font-size: 19px !important; font-weight: 900; color: #C04B41; }
    
    .table-wrapper { width: 100%; margin-top: 5px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: center; }
    .custom-table th, .custom-table td { border: 1px solid #dee2e6; padding: 8px 2px; }
    .highlight-row { background-color: #FFE5E5 !important; font-weight: bold; color: #C04B41; outline: 2px solid #C04B41; }
    
    .ready-msg { text-align: center; padding: 10px; background: #EEF2FF; border-radius: 10px; border: 1px solid #2E4077; margin-bottom: 15px; font-weight: 700; color: #2E4077; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜 및 패턴 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

today = now.date()
# 05:30분부터는 오늘 주간 근무자 미리 계산
is_early_morning = (5 <= now.hour < 7) or (now.hour == 5 and now.minute >= 30)
work_date = today if (now.hour >= 7 or is_early_morning) else (today - timedelta(days=1))

jojang, seonghui, uisanA, uisanB = get_workers_by_date(work_date)
# 비번일 경우 예외처리
if jojang is None:
    jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

# --- [3] 시간표 데이터 ---
combined_data = [
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

def get_current_idx(dt):
    curr_m = dt.hour * 60 + dt.minute
    if dt.hour < 7: curr_m += 1440
    for i, row in enumerate(combined_data):
        sh, sm = map(int, row[0].split(':'))
        eh, em = map(int, row[1].split(':'))
        s_m = (sh + 24 if sh < 7 else sh) * 60 + sm
        e_m = (eh + 24 if (eh < 7 or (eh == 7 and em == 0)) and sh != 7 else eh) * 60 + em
        if s_m <= curr_m < e_m: return i
    return -1

curr_idx = get_current_idx(now)

# --- [4] UI 출력 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    # 상단 실시간 카드
    if get_workers_by_date(work_date)[0] is not None:
        def get_status(idx, col):
            return combined_data[idx][col] if idx != -1 else "교대 대기"

        st.markdown(f'''
            <div class="status-container">
                <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{get_status(curr_idx, 2)}</div></div>
                <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{get_status(curr_idx, 3)}</div></div>
                <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{get_status(curr_idx, 4)}</div></div>
                <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{get_status(curr_idx, 5)}</div></div>
            </div>
        ''', unsafe_allow_html=True)
        
        if curr_idx == -1 and is_early_morning:
            st.markdown('<div class="ready-msg">☕ 교대 준비 중입니다. (07:00 근무 시작)</div>', unsafe_allow_html=True)

    # --- 체크박스 ---
    show_all = st.checkbox("🔄 전체 시간표 순서대로 보기", value=False)

    # 테이블 정렬 및 하이라이트 설정
    display_data = combined_data.copy()
    high_idx = curr_idx

    if not show_all and curr_idx != -1:
        display_data = [combined_data[curr_idx]] + [r for i, r in enumerate(combined_data) if i != curr_idx]
        high_idx = 0
    
    # --- 수정된 2단 헤더 테이블 ---
    html_table = f"""
    <div class="table-wrapper">
    <table class="custom-table">
        <thead>
            <tr style="background:#f8f9fa; font-weight:bold;">
                <th colspan="2" style="background:#f1f3f5;">구분 (시간)</th>
                <th colspan="2" style="background:#FFF2CC;">성의회관</th>
                <th colspan="2" style="background:#D9EAD3;">의산연</th>
            </tr>
            <tr style="background:#fdfdfe; font-size:11.5px; font-weight:700; color:#444;">
                <td style="width:18%;">From</td>
                <td style="width:18%;">To</td>
                <td style="background:#FFF9E6; width:16%; color:#B08D2E;">{jojang}</td>
                <td style="background:#FFF9E6; width:16%; color:#B08D2E;">{seonghui}</td>
                <td style="background:#EBF5E9; width:16%; color:#3E7E44;">{uisanA}</td>
                <td style="background:#EBF5E9; width:16%; color:#3E7E44;">{uisanB}</td>
            </tr>
        </thead>
        <tbody>
    """
    for i, r in enumerate(display_data):
        row_cls = "highlight-row" if i == high_idx and high_idx != -1 else ""
        html_table += f'''
            <tr class="{row_cls}">
                <td>{r[0]}</td><td>{r[1]}</td>
                <td>{r[2]}</td><td>{r[3]}</td>
                <td>{r[4]}</td><td>{r[5]}</td>
            </tr>'''
    
    st.markdown(html_table + "</tbody></table></div>", unsafe_allow_html=True)

with tab2:
    # 편성표 탭 (동일 유지)
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_date = st.date_input("📅 시작일", today, key="cal_final")
    with c2: focus_u = st.selectbox("👤 강조 대상", ["안 함", "황재업", "김태언", "이태원", "이정석"])
    view_days = st.slider("📅 조회 기간 (일)", 7, 60, 31)
    # ... (이하 동일)
