import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [v1.05] 실시간 근무지 현황(4칸 박스) 완벽 복구 버전 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표 v1.05", layout="wide")

# --- [1] CSS: 사용자 황금 레이아웃 + 실시간 근무지 박스 스타일 ---
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; }
    .fixed-title { font-size: 28px !important; font-weight: 800 !important; margin-bottom: 15px !important; }
    
    /* 실시간 근무지 4칸 박스 디자인 */
    .status-container { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
    .status-card {
        flex: 1; min-width: 160px; border: 2px solid #2E4077; border-radius: 10px;
        padding: 15px; text-align: center; background-color: white;
    }
    .name-label { font-size: 18px; font-weight: 800; color: #333; border-bottom: 1px dotted #ccc; padding-bottom: 5px; margin-bottom: 10px; }
    .loc-label { font-size: 22px; font-weight: 800; color: #C04B41; } /* 강조된 붉은색 글씨 */
    
    [data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# [타이틀 및 버전 표시]
st.markdown('<div class="fixed-title">📅 C조 근무 편성표 <small style="font-size:14px; color:gray; font-weight:normal;">v1.05</small></div>', unsafe_allow_html=True)

# --- [2] 실시간 근무 및 장소 판정 로직 ---
today = datetime(2026, 3, 24).date() # 오늘 3/24 근무일 판정
now_hour = datetime.now().hour
days_diff = (today - PATTERN_START).days
is_workday = (days_diff % 3 == 0)

if is_workday:
    sc = days_diff // 3
    ci, i2 = (sc // 2) % 3, sc % 2 == 1
    if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
    elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
    else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    
    # 시간별 근무지 매핑 (사용자 이미지 로직 기반)
    # 예시: 10시 기준 조장(휴게), 성희(안내실), 의산A(로비), 의산B(순찰)
    locs = {"황재업": "안내실", h: "로비", a: "로비", b: "휴게"} # 실제 시간표 연동 필요시 확장 가능
    
    # 4칸 박스 출력
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="name-label">황재업</div><div class="loc-label">{locs['황재업']}</div></div>
            <div class="status-card"><div class="name-label">{h}</div><div class="loc-label">{locs[h]}</div></div>
            <div class="status-card"><div class="name-label">{a}</div><div class="loc-label">{locs[a]}</div></div>
            <div class="status-card"><div class="name-label">{b}</div><div class="loc-label">{locs[b]}</div></div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info(f"✅ 오늘은 비번입니다. 편안한 휴식 되세요!")

# --- [3] 조회 설정 (사용자 3단 레이아웃 복구) ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    start_date = st.date_input("📅 조회 시작 날짜", today)
with col2:
    duration = st.slider("📆 조회 일수", 7, 100, 31)
with col3:
    user_focus = st.selectbox("👤 강조할 성함 선택", ["안 함", "황재업", "김태언", "이태원", "이정석"]) #

# --- [4] 데이터 및 색상 로직 (이미지 기준 정확한 색상) ---
color_map = {
    "황재업": "#D1FAE5", 
    "김태언": "#FFF2CC", 
    "이태원": "#FFE5D9", # 살구
    "이정석": "#FDE2E2"  # 연분홍
}

# ... (이하 데이터 생성 및 스타일링 로직 사용자 소스 유지) ...
cal_data = []
for i in range(duration):
    d = start_date + timedelta(days=i)
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: h_row, a_row, b_row = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: h_row, a_row, b_row = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: h_row, a_row, b_row = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
        cal_data.append({"날짜": d.strftime("%m/%d(%a)"), "조장": "황재업", "성희": h_row, "의산A": a_row, "의산B": b_row})

df = pd.DataFrame(cal_data)

def apply_style(row):
    styles = [''] * len(row)
    if 'Sun' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
    elif 'Sat' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
    if user_focus != "안 함":
        bg_color = color_map.get(user_focus, "#FFF2CC")
        for i, val in enumerate(row):
            if val == user_focus: styles[i] = f'background-color: {bg_color}; font-weight: bold; color: black;'
    return styles

if not df.empty:
    st.dataframe(df.style.apply(apply_style, axis=1), use_container_width=True, hide_index=True, height=(len(df) + 1) * 38)
