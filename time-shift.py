import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [1] 기본 설정 및 패턴 엔진 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="성의교정 C조 근무편성표", layout="wide")

# --- [2] CSS: 타이틀 크기 축소 및 가독성 최적화 ---
st.markdown("""
    <style>
    .block-container { padding: 0.7rem !important; }
    /* 타이틀 폰트 크기 절반(24px)으로 상단에 확실히 고정 */
    .main-title { 
        font-size: 24px !important; 
        font-weight: bold; 
        margin-bottom: 15px; 
        color: #1E3A8A; 
        border-bottom: 2px solid #eee;
        padding-bottom: 5px;
    }
    /* 표 내부 텍스트 크기 및 스크롤 제거 */
    .stDataFrame div[data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# [타이틀] 지시하신 대로 상단에 삽입
st.markdown('<div class="main-title">📅 성의교정 C조 근무편성표</div>', unsafe_allow_html=True)

# --- [3] 조회 기간 설정 (달력 + 슬라이드) ---
with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        # 달력으로 시작일 선택 (과거 근무 확인용)
        start_date = st.date_input("📅 조회 시작 날짜", datetime.now().date() - timedelta(days=7))
    with col2:
        # 슬라이드로 조회할 총 일수 결정
        duration = st.slider("📆 조회 일수(범위)", 7, 100, 31)
    
    # 강조할 성함 선택
    user_focus = st.selectbox("👤 강조할 성함 선택", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 근무 데이터 생성 (요일 셸 통합) ---
cal_data = []
for i in range(duration):
    d = start_date + timedelta(days=i)
    diff = (d - PATTERN_START).days
    
    # 3일 주기 로직 (사용자 원본 엔진)
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
    if '(Sun)' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
    elif '(Sat)' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
    
    if user_focus != "안 함":
        for i, val in enumerate(row):
            if val == user_focus:
                styles[i] = 'background-color: #FFF2CC; font-weight: bold; color: black;'
    return styles

# --- [6] 표 출력 (스크롤 없이 전체 노출) ---
if not df.empty:
    st.dataframe(
        df.style.apply(apply_style, axis=1),
        use_container_width=True,
        hide_index=True,
        height=(len(df) + 1) * 38  # 행 개수에 맞춰 높이 자동 조절
    )
