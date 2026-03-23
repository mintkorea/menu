import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [1] 기본 설정 및 패턴 엔진 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표", layout="wide")

# --- [2] CSS: 가독성 및 스크롤 최적화 ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    /* 표 내부 텍스트 크기 및 요일 색상 강조를 위한 스타일 */
    .stDataFrame div[data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [3] 타이틀 (Streamlit 기본 타이틀 사용으로 가려짐 방지) ---
# 기존 마크다운 방식이 아닌 기본 title 함수를 사용하여 확실히 표시
st.title("📅 C조 근무 편성표") 

# --- [4] 조회 기간 설정 및 강조 ---
with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        # 달력 시작일 선택
        start_date = st.date_input("📅 조회 시작 날짜", datetime(2026, 3, 16).date())
    with col2:
        # 조회 일수 슬라이더
        duration = st.slider("📆 조회 일수(범위)", 7, 100, 31)
    
    # 강조할 성함 선택
    user_focus = st.selectbox("👤 강조할 성함 선택", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [5] 근무 데이터 생성 (요일 셸 없이 날짜에 통합) ---
cal_data = []
for i in range(duration):
    d = start_date + timedelta(days=i)
    diff = (d - PATTERN_START).days
    
    # 3일 주기 로직 적용
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

# --- [6] 스타일 적용 (요일 색상 + 사용자 강조) ---
def apply_style(row):
    styles = [''] * len(row)
    # 날짜 셀 요일 색상 강조 (빨강/파랑)
    if '(Sun)' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
    elif '(Sat)' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
    
    # 사용자 노란색 강조
    if user_focus != "안 함":
        for i, val in enumerate(row):
            if val == user_focus:
                styles[i] = 'background-color: #FFF2CC; font-weight: bold; color: black;'
    return styles

# --- [7] 표 출력 (스크롤 없이 전체 노출 설정) ---
if not df.empty:
    st.dataframe(
        df.style.apply(apply_style, axis=1),
        use_container_width=True,
        hide_index=True,
        height=(len(df) + 1) * 38 # 스크롤 따로 생기지 않게 높이 자동 조절
    )
