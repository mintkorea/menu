import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [1] 핵심 설정 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표", layout="wide")

# --- [2] CSS: 가독성 설정 ---
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    .stDataFrame div[data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📅 C조 근무 편성표")

# --- [3] 상단 메뉴: 조회 기간 선택 및 사용자 강조 ---
with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        # 조회 기간 선택 (슬라이더)
        days_range = st.slider("📅 조회 기간 설정 (오늘 기준)", -10, 60, (0, 30))
    with col2:
        # 강조할 사용자 선택
        user_focus = st.selectbox("👤 강조할 성함 선택", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 근무 데이터 생성 로직 (요일 컬럼 제외) ---
today = datetime.now().date()
cal_data = []

# 설정한 슬라이더 범위에 따라 데이터 생성
for i in range(days_range[0], days_range[1] + 1):
    d = today + timedelta(days=i)
    diff = (d - PATTERN_START).days
    
    # 3일 로테이션 (C조 근무일만 계산)
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
    
    # 1. 날짜별 요일 색상 강조 (토요일: 파랑, 일요일: 빨강)
    if '(Sun)' in row['날짜']:
        styles[0] = 'color: red; font-weight: bold'
    elif '(Sat)' in row['날짜']:
        styles[0] = 'color: blue; font-weight: bold'
    
    # 2. 사용자 강조 (선택한 이름이 있으면 노란색 배경)
    if user_focus != "안 함":
        for i, val in enumerate(row):
            if val == user_focus:
                styles[i] = 'background-color: #FFF2CC; font-weight: bold; color: black;'
                
    return styles

# 최종 표 출력 (hide_index로 깔끔하게 표시)
if not df.empty:
    st.dataframe(
        df.style.apply(apply_style, axis=1),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("선택하신 기간에는 근무가 없습니다.")
