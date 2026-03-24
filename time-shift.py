import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (모바일 최적화 및 버튼 축소) ---
st.set_page_config(page_title="C조 통합 포털", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 22px !important; font-weight: 800; text-align: center; margin-bottom: 10px; }
    
    /* 버튼: 작고 덜 튀게 설정 */
    .stButton > button {
        width: auto; padding: 2px 10px; border-radius: 6px; height: 2.2em;
        background-color: #f8f9fa; color: #555; font-weight: normal; font-size: 12px;
        border: 1px solid #ddd; display: block; margin: 0 auto 15px auto;
    }

    /* 통합 테이블: 건물 헤더와 이름 헤더 일체화 */
    .custom-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 11px; }
    .custom-table th, .custom-table td { 
        border: 1px solid #dee2e6; padding: 6px 1px; text-align: center; 
        white-space: nowrap; overflow: hidden;
    }
    .bld-header { background-color: #f1f3f5; font-weight: bold; font-size: 10px; color: #495057; }
    .name-header { background-color: #e9ecef; font-weight: bold; }
    .highlight-row { background-color: #FFE5E5; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 (이름 이니셜 처리 및 날짜 계산) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# 07시 기준 날짜 처리
if now.hour < 7:
    target_date = (now - timedelta(days=1)).date()
else:
    target_date = now.date()
next_date = target_date + timedelta(days=1)

PATTERN_START = datetime(2026, 3, 9).date()

def get_workers(d):
    diff = (d - PATTERN_START).days
    # 기본 근무자 명단 (원본 데이터)
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: names = ["황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")]
        elif ci == 1: names = ["황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")]
        else: names = ["황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")]
    else:
        names = ["황재업", "김태언", "이태원", "이정석"]
    
    # 공간 확보를 위해 '이름'만 추출 (예: 황재업 -> 재업)
    return [n[1:] if len(n)==3 else n for n in names]

# 오늘/내일 근무자 이니셜 명단
w_today = get_workers(target_date)
w_next = get_workers(next_date)

# --- [3] 데이터 정의 및 테이블 렌더링 함수 ---
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

# 테이블 생성 함수 (중요: 여기서 오류 해결)
def render_unified_table(df_input, names, h_idx=None):
    j, s, a, b = names
    html = f"""
    <table class="custom-table">
        <tr class="bld-header">
            <th rowspan="2" style="width:24%;">시간</th>
            <th colspan="2" style="background:#FFF2CC;">성의회관</th>
            <th colspan="2" style="background:#D9EAD3;">의학연구원</th>
        </tr>
        <tr class="name-header">
            <th style="background:#FFF2CC;">{j}</th><th style="background:#FFF2CC;">{s}</th>
            <th style="background:#D9EAD3;">{a}</th><th style="background:#D9EAD3;">{b}</th>
        </tr>
    """
    for i, r in df_input.iterrows():
        cls = "highlight-row" if i == h_idx else ""
        # 주의: 렌더링 시에는 고정된 위치(인덱스)의 데이터를 가져옴
        html += f"<tr class='{cls}'><td>{r[0]}~{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>"
    return html + "</table>"

# 현재 인덱스 계산
def get_curr_idx(h):
    curr = h if h >= 7 else h + 24
    for i, r in enumerate(time_data):
        sh = int(r[0].split(':')[0]); sh = sh if sh >= 7 else sh + 24
        eh = int(r[1].split(':')[0]); eh = eh if eh >= 7 else eh + 24
        if sh <= curr < eh: return i
    return 20
curr_idx = get_curr_idx(now.hour)

# --- [4] 화면 출력 ---
st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; font-size:13px; color:666; margin-bottom:10px;">{target_date.strftime("%m/%d")} ({now.strftime("%H:%M")})</div>', unsafe_allow_html=True)

# 1. 팝업 버튼 (작고 중앙 정렬)
@st.dialog("📅 오늘 전체 시간표")
def show_all():
    df_today = pd.DataFrame(time_data)
    st.markdown(render_unified_table(df_today, w_today, curr_idx), unsafe_allow_html=True)

if st.button("📋 전체 시간표 보기"):
    show_all()

# 2. 메인 화면: 현재 근무
st.markdown("**▼ 현재 근무**")
df_curr = pd.DataFrame([time_data[curr_idx]])
st.markdown(render_unified_table(df_curr, w_today, 0), unsafe_allow_html=True)

st.write("")
st.markdown("---")

# 3. 내일 근무 미리보기
st.markdown(f"**📅 내일 근무 예정 ({next_date.strftime('%m/%d')})**")
df_all = pd.DataFrame(time_data)
st.markdown(render_unified_table(df_all, w_next), unsafe_allow_html=True)
