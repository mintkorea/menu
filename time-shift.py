import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 페이지 설정 및 CSS (가독성 최적화) ---
st.set_page_config(page_title="C조 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; max-width: 500px; margin: auto; }
    .title { font-size: 22px !important; font-weight: 800; text-align: center; margin-bottom: 2px; }
    .sub-title { font-size: 12px; text-align: center; color: #666; margin-bottom: 15px; }
    
    /* 요약 카드 스타일 */
    .card-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
    .card { border: 1px solid #2E4077; border-radius: 8px; padding: 10px; text-align: center; background: white; shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .card-name { font-size: 13px; color: #555; font-weight: bold; }
    .card-loc { font-size: 18px; color: #C04B41; font-weight: 900; margin-top: 2px; }

    /* 통합 테이블 스타일 */
    .unified-table { width: 100%; border-collapse: collapse; font-size: 11px; text-align: center; table-layout: fixed; }
    .unified-table th, .unified-table td { border: 1px solid #ddd; padding: 6px 1px; white-space: nowrap; }
    .bld-header { background-color: #f1f3f5; font-weight: bold; font-size: 10px; color: #495057; }
    .name-header { background-color: #e9ecef; font-weight: bold; }
    .curr-row { background-color: #FFE5E5; font-weight: bold; }
    
    /* 탭 메뉴 스타일 조정 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { height: 40px; border-radius: 4px 4px 0 0; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 (날짜, 패턴, 이름 추출) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# 07시 기준 근무일 설정
target_date = (now - timedelta(days=1)).date() if now.hour < 7 else now.date()
next_date = target_date + timedelta(days=1)
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers(d):
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: res = ["황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")]
        elif ci == 1: res = ["황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")]
        else: res = ["황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")]
    else: res = ["황재업", "김태언", "이태원", "이정석"]
    # 이름 두 글자 이니셜화 (황재업 -> 재업)
    return [n[1:] if len(n)==3 else n for n in res]

w_today = get_workers(target_date)
w_next = get_workers(next_date)

# --- [3] 데이터 및 테이블 생성 함수 ---
time_slots = [
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
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"]
]

def render_table(data_list, names, h_idx=None):
    j, s, a, b = names
    html = f"""<table class="unified-table">
        <tr class="bld-header">
            <th rowspan="2" style="width:24%">시간</th>
            <th colspan="2" style="background:#FFF2CC">성의회관</th>
            <th colspan="2" style="background:#D9EAD3">의학연구원</th>
        </tr>
        <tr class="name-header">
            <th style="background:#FFF2CC">{j}</th><th style="background:#FFF2CC">{s}</th>
            <th style="background:#D9EAD3">{a}</th><th style="background:#D9EAD3">{b}</th>
        </tr>"""
    for i, r in enumerate(data_list):
        cls = "class='curr-row'" if i == h_idx else ""
        html += f"<tr {cls}><td>{r[0]}~{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>"
    return html + "</table>"

def get_curr_idx():
    h = now.hour; val = h if h >= 7 else h + 24
    for i, r in enumerate(time_slots):
        sh = int(r[0].split(':')[0]); sh = sh if sh >= 7 else sh + 24
        eh = int(r[1].split(':')[0]); eh = eh if eh >= 7 else eh + 24
        if sh <= val < eh: return i
    return 20

curr_idx = get_curr_idx()

# --- [4] 메인 화면 구성 ---
st.markdown('<div class="title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">{target_date.strftime("%Y-%m-%d")} ({now.strftime("%H:%M:%S")})</div>', unsafe_allow_html=True)

# 탭 메뉴 복구
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    # 1. 요약 카드 섹션 복구
    c = time_slots[curr_idx]
    st.markdown(f"""
    <div class="card-container">
        <div class="card"><div class="card-name">{w_today[0]} (조장)</div><div class="card-loc">{c[2]}</div></div>
        <div class="card"><div class="card-name">{w_today[1]} (성의)</div><div class="card-loc">{c[3]}</div></div>
        <div class="card"><div class="card-name">{w_today[2]} (의산A)</div><div class="card-loc">{c[4]}</div></div>
        <div class="card"><div class="card-name">{w_today[3]} (의산B)</div><div class="card-loc">{c[5]}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 현재 근무 상세 (통합 헤더 적용)
    st.markdown("**▼ 현재 근무 상세**")
    st.markdown(render_table([time_slots[curr_idx]], w_today, 0), unsafe_allow_html=True)
    
    # 3. 내일 근무 미리보기 추가
    st.write("")
    st.markdown(f"**📅 내일 근무 예정 ({next_date.strftime('%m/%d')})**")
    with st.expander("내일 전체 시간표 확인하기"):
        st.markdown(render_table(time_slots, w_next), unsafe_allow_html=True)

with tab2:
    # 당일 전체 시간표 복구
    st.markdown(f"**📋 {target_date.strftime('%m/%d')} 당일 전체 편성표**")
    st.markdown(render_table(time_slots, w_today, curr_idx), unsafe_allow_html=True)

