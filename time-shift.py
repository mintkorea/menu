import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [복구] 실시간 상황 작업 중이던 원본 소스 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표", layout="wide")

# --- [1] CSS: 4칸 박스 및 사용자 정의 스타일 ---
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; }
    .fixed-title { font-size: 28px !important; font-weight: 800 !important; margin-bottom: 15px !important; }
    
    /* 실시간 근무지 카드 스타일 */
    .status-container { display: flex; flex-direction: column; gap: 10px; margin-bottom: 25px; }
    .status-card {
        border: 2px solid #2E4077; border-radius: 12px;
        padding: 15px; text-align: center; background-color: white;
    }
    .name-label { font-size: 20px; font-weight: 800; color: #333; margin-bottom: 8px; border-bottom: 1px dotted #ccc; }
    .loc-label { font-size: 24px; font-weight: 800; color: #C04B41; }
    
    [data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="fixed-title">📅 C조 근무 편성표</div>', unsafe_allow_html=True)

# --- [2] 실시간 근무지 판정 로직 (작업 중이던 부분) ---
today = datetime(2026, 3, 24).date()
days_diff = (today - PATTERN_START).days

# 근무자 계산
sc = days_diff // 3
ci, i2 = (sc // 2) % 3, sc % 2 == 1
if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")

# 4칸 실시간 상황판 출력
st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="name-label">황재업</div><div class="loc-label">안내실</div></div>
        <div class="status-card"><div class="name-label">{h}</div><div class="loc-label">로비</div></div>
        <div class="status-card"><div class="name-label">{a}</div><div class="loc-label">로비</div></div>
        <div class="status-card"><div class="name-label">{b}</div><div class="loc-label">휴게</div></div>
    </div>
""", unsafe_allow_html=True)

# --- [3] 하단 조회 설정 (원본 레이아웃) ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    start_date = st.date_input("📅 조회 시작 날짜", today)
with col2:
    duration = st.slider("📆 조회 일수", 7, 100, 31)
with col3:
    user_focus = st.selectbox("👤 강조할 성함", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 데이터 및 스타일 로직 ---
color_map = {"황재업": "#D1FAE5", "김태언": "#FFF2CC", "이태원": "#FFE5D9", "이정석": "#FDE2E2"}

cal_data = []
for i in range(duration):
    d = start_date + timedelta(days=i)
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        r_sc = diff // 3
        r_ci, r_i2 = (r_sc // 2) % 3, r_sc % 2 == 1
        if r_ci == 0: rh, ra, rb = "김태언", ("이정석" if r_i2 else "이태원"), ("이태원" if r_i2 else "이정석")
        elif r_ci == 1: rh, ra, rb = "이정석", ("이태원" if r_i2 else "김태언"), ("김태언" if r_i2 else "이태원")
        else: rh, ra, rb = "이태원", ("이정석" if r_i2 else "김태언"), ("김태언" if r_i2 else "이정석")
        cal_data.append({"날짜": d.strftime("%m/%d(%a)"), "조장": "황재업", "성희": rh, "의산A": ra, "의산B": rb})

df = pd.DataFrame(cal_data)

def apply_style(row):
    styles = [''] * len(row)
    if 'Sun' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
    elif 'Sat' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
    if user_focus != "안 함":
        bg_color = color_map.get(user_focus, "#FFF2CC")
        for i, val in enumerate(row):
            if val == user_focus: styles[i] = f'background-color: {bg_color}; font-weight: bold;'
    return styles

if not df.empty:
    st.dataframe(df.style.apply(apply_style, axis=1), use_container_width=True, hide_index=True, height=(len(df) + 1) * 38)
