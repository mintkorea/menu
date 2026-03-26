import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 페이지 설정 및 스타일 ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

# CSS를 별도의 변수로 분리하여 관리
common_style = """
<style>
    .block-container { padding-top: 1.5rem !important; max-width: 500px; margin: auto; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 12px; padding: 10px 5px; text-align: center; background: white; }
    .worker-name { font-size: 14px; font-weight: 700; color: #555; }
    .status-val { font-size: 18px; font-weight: 900; color: #C04B41; }
    .table-wrapper { width: 100%; margin-top: 5px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table th, .custom-table td { border: 1px solid #dee2e6; padding: 10px 2px; }
    .header-main { background-color: #f8f9fa; font-weight: 800; }
    .header-sub-seong { background-color: #FFF2CC; font-weight: 700; color: #856404; }
    .header-sub-uisan { background-color: #D9EAD3; font-weight: 700; color: #274e13; }
    .highlight-row { background-color: #FFE5E5 !important; font-weight: bold; color: #C04B41; outline: 2px solid #C04B41; }
    .ready-msg { text-align: center; padding: 10px; background: #EEF2FF; border-radius: 10px; border: 1px solid #2E4077; margin-bottom: 15px; font-weight: 700; color: #2E4077; font-size: 14px; }
</style>
"""
st.markdown(common_style, unsafe_allow_html=True)

# --- [2] 로직 (시간 및 인원) ---
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
    return "정보없음", "정보없음", "정보없음", "정보없음"

today = now.date()
is_prep_time = (5 <= now.hour < 7) or (now.hour == 5 and now.minute >= 30)
work_date = today if (now.hour >= 7 or is_prep_time) else (today - timedelta(days=1))
names = get_workers(work_date)

# --- [3] 데이터 ---
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

# --- [4] 화면 출력 ---
st.markdown(f'<p style="text-align:right; font-size:12px; color:gray;">{now.strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)

# 카드 영역
st.markdown(f'''
<div class="status-container">
    <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">{"교대 대기" if curr_idx == -1 else data[curr_idx][2]}</div></div>
    <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">{"교대 대기" if curr_idx == -1 else data[curr_idx][3]}</div></div>
    <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">{"교대 대기" if curr_idx == -1 else data[curr_idx][4]}</div></div>
    <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">{"교대 대기" if curr_idx == -1 else data[curr_idx][5]}</div></div>
</div>
''', unsafe_allow_html=True)

if curr_idx == -1 and is_prep_time:
    st.markdown('<div class="ready-msg">📢 곧 근무가 시작됩니다. (07:00 투입)</div>', unsafe_allow_html=True)

# 버튼 (체크박스)
show_all = st.checkbox("🔄 전체 시간표 순서대로 보기", value=False)

# 테이블 정렬
display_rows = data.copy()
highlight = curr_idx
if not show_all and curr_idx != -1:
    display_rows = [data[curr_idx]] + [r for i, r in enumerate(data) if i != curr_idx]
    highlight = 0
elif curr_idx == -1:
    highlight = -1

# 테이블 생성
rows_html = ""
for i, r in enumerate(display_rows):
    cls = ' class="highlight-row"' if i == highlight and highlight != -1 else ""
    rows_html += f"<tr{cls}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>"

table_html = f"""
<div class="table-wrapper">
    <table class="custom-table">
        <thead>
            <tr class="header-main"><th colspan="2">구분</th><th colspan="2" style="background:#FFF2CC;">성의회관</th><th colspan="2" style="background:#D9EAD3;">의산연</th></tr>
            <tr style="background:#fff; font-weight:700;"><td>From</td><td>To</td>
                <td class="header-sub-seong">{names[0]}</td><td class="header-sub-seong">{names[1]}</td>
                <td class="header-sub-uisan">{names[2]}</td><td class="header-sub-uisan">{names[3]}</td>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
</div>
"""
st.markdown(table_html, unsafe_allow_html=True)
