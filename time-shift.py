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
    /* 표 내부 텍스트 정렬 및 크기 */
    .stDataFrame div[data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [3] 상단 메뉴 (조회 및 강조) ---
st.title("📅 C조 근무 편성표")

with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        # 강조할 사용자 선택 (기능 복구)
        user_focus = st.selectbox("👤 강조할 성함 선택", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 근무 데이터 생성 로직 ---
today = datetime.now().date()
cal_data = []

# 오늘 기준 전후 30일치 편성
for i in range(-5, 30):
    d = today + timedelta(days=i)
    diff = (d - PATTERN_START).days
    
    # 3일 로테이션 (C조 근무일만 계산)
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        
        # 원본 엔진 순번
        if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
        
        cal_data.append({
            "날짜": d.strftime("%m/%d(%a)"),
            "요일": d.strftime("%a"),
            "조장": "황재업",
            "성희": h,
            "의산A": a,
            "의산B": b
        })

df = pd.DataFrame(cal_data)

# --- [5] 스타일 적용 (요일 색상 + 사용자 강조) ---
def apply_style(row):
    styles = [''] * len(row)
    
    # 1. 요일 색상 (날짜 컬럼 기준)
    if 'Sun' in row['날짜']:
        styles[0] = 'color: red; font-weight: bold'
    elif 'Sat' in row['날짜']:
        styles[0] = 'color: blue; font-weight: bold'
    
    # 2. 사용자 강조 (노란색 배경)
    if user_focus != "안 함":
        for i, val in enumerate(row):
            if val == user_focus:
                styles[i] = 'background-color: #FFF2CC; font-weight: bold; color: black;'
                
    return styles

# 표 출력 (불필요한 인덱스 제거)
st.dataframe(
    df.style.apply(apply_style, axis=1),
    use_container_width=True,
    hide_index=True
)
