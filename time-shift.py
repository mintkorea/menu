import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (표 통합 및 모바일 최적화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 22px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 14px !important; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 요약 카드 스타일 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 8px 0; text-align: center; background: #F8F9FA; }
    .worker-name { font-size: 14px; font-weight: 700; color: #444; }
    .status-val { font-size: 17px; font-weight: 900; color: #C04B41; }

    /* 통합 테이블: 줄바꿈 방지 및 헤더 고정 */
    .custom-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 11px; }
    .custom-table th, .custom-table td { 
        border: 1px solid #dee2e6; padding: 6px 2px; text-align: center; 
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .header-row { background-color: #f8f9fa; font-weight: bold; }
    .highlight-row { background-color: #FFE5E5; font-weight: bold; }
    
    /* 버튼 스타일 */
    .stButton > button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #1E3A5F; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 (날짜 및 인원 배정) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# 자정~07시 로직 적용
if now.hour < 7:
    target_date = (now - timedelta(days=1)).date()
    display_msg = f"{target_date.strftime('%m/%d')} 야간 근무 (07시 종료)"
else:
    target_date = now.date()
    display_msg = f"{target_date.strftime('%m/%d')} 근무 현황"

PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(d):
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이정석")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return "황재업", "김태언", "이태원", "이정석"

jojang, seonghui, uisanA, uisanB = get_workers_by_date(target_date)

# --- [3] 데이터 및 테이블 함수 ---
time_data = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "순찰", "안내실", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "순찰"],
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"],
    ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"],
    ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"],
    ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"],
    ["23:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"],
    ["02:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"],
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"],
]
df_rt = pd.DataFrame(time_data, columns=["From", "To", jojang, seonghui, uisanA, uisanB])

def render_table(df, h_idx=None):
    html = f"""<table class="custom-table">
        <tr class="header-row">
            <th style="width:24%">시간</th><th style="background:#FFF2CC">{jojang[:2]}</th><th style="background:#FFF2CC">{seonghui[:2]}</th>
            <th style="background:#D9EAD3">{uisanA[:2]}</th><th style="background:#D9EAD3">{uisanB[:2]}</th>
        </tr>"""
    for i, r in df.iterrows():
        cls = "highlight-row" if i == h_idx else ""
        html += f"<tr class='{cls}'><td>{r['From']}~{r['To']}</td><td>{r[jojang]}</td><td>{r[seonghui]}</td><td>{r[uisanA]}</td><td>{r[uisanB]}</td></tr>"
    return html + "</table>"

# 현재 인덱스 찾기
def get_idx(h, m):
    curr = h if h >= 7 else h + 24
    for i, r in df_rt.iterrows():
        sh = int(r['From'].split(':')[0]); sh = sh if sh >= 7 else sh + 24
        eh = int(r['To'].split(':')[0]); eh = eh if eh >= 7 else eh + 24
        if sh <= curr < eh: return i
    return 20
curr_idx = get_idx(now.hour, now.minute)

# --- [4] 화면 출력 ---
st.markdown(f'<div class="unified-title">C조 실시간 현황</div>', unsafe_allow_html=True)
st.markdown(f'<div class="title-sub">{display_msg} ({now.strftime("%H:%M")})</div>', unsafe_allow_html=True)

# 요약 카드
c = df_rt.iloc[curr_idx]
st.markdown(f"""<div class="status-container">
    <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{c[jojang]}</div></div>
    <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{c[seonghui]}</div></div>
    <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{c[uisanA]}</div></div>
    <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status
