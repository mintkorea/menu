import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [1] 핵심 설정 (변동 없음) ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표", layout="wide")

# --- [2] CSS: 타이틀 크기 절반 축소 & 가독성 ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem !important; }
    /* 타이틀 폰트 크기 절반(24px)으로 축소 */
    .small-title { font-size: 24px !important; font-weight: bold; margin-bottom: 15px; color: #31333F; }
    .stDataFrame div[data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# [타이틀] 절반 크기로 적용
st.markdown('<p class="small-title">📅 C조 근무 편성표</p>', unsafe_allow_html=True)

# --- [3] 조회 및 강조 설정 ---
with st.container():
    # [조회달력 슬라이드] - 사용자님이 말씀하신 슬라이더 방식 복구
    lookback, lookforward = st.slider("📅 조회 기간 설정 (오늘 기준)", -30, 90, (-10, 60))
    
    # 강조할 성함 선택
    user_focus = st.selectbox("👤 강조할 성함 선택", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 근무 데이터 생성 (요일 셸 없이 통합) ---
today = datetime.now().date()
cal_data = []

# 슬라이더에서 선택한 범위만큼 데이터 생성
for i in range(lookback, lookforward + 1):
    d = today + timedelta(days=i)
    diff = (d - PATTERN_START).days
    
    # 3일 로테이션 (C조 근무일)
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        
        if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
        
        cal_data.append({
            "날짜": d.strftime("%m/%d(%a)"),
            "조장": "황재업",
            "성희": h,
            "의산A": a,
            "의산B": b
        })

df = pd.DataFrame(cal_data)

# --- [5] 스타일 적용 (요일 색상 + 사용자 강조) ---
def apply_style(row):
    styles = [''] * len(row)
    
    # 요일 색상 (Sun: 빨강, Sat: 파랑)
    if '(Sun)' in row['날짜']:
        styles[0] = 'color: red; font-weight: bold'
    elif '(Sat)' in row['날짜']:
        styles[0] = 'color: blue; font-weight: bold'
    
    # 사용자 강조 (노란색 배경)
    if user_focus != "안 함":
        for i, val in enumerate(row):
            if val == user_focus:
                styles[i] = 'background-color: #FFF2CC; font-weight: bold; color: black;'
                
    return styles

# 표 출력 (요일 셸 삭제 반영)
st.dataframe(
    df.style.apply(apply_style, axis=1),
    use_container_width=True,
    hide_index=True
)
