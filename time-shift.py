import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [1] 기본 설정 및 패턴 엔진 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표", layout="wide")

# --- [2] CSS: 타이틀 크기(절반) 및 여백 최적화 ---
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; }
    
    /* 타이틀 폰트 크기를 절반 정도로 줄여 상단에 확실히 표시 */
    .fixed-title { 
        font-size: 24px !important; 
        font-weight: 800 !important;
        margin-bottom: 15px !important;
        color: #31333F !important;
        padding-bottom: 5px;
        border-bottom: 2px solid #f0f2f6;
    }
    
    /* 표 텍스트 크기 및 스크롤 방지 */
    [data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# [타이틀] 절반 크기로 최상단 배치
st.markdown('<div class="fixed-title">📅 C조 근무 편성표</div>', unsafe_allow_html=True)

# --- [3] 조회 설정 (달력 + 슬라이드) ---
# 최신 캡처의 위아래 배치 구조 반영
with st.container():
    # 1. 달력 시작일 선택
    start_date = st.date_input("📅 조회 시작 날짜", datetime(2026, 3, 16).date())
    
    # 2. 조회 일수 슬라이더
    duration = st.slider("📆 조회 일수", 7, 100, 31)
    
    # 3. 강조할 성함 선택
    user_focus = st.selectbox("👤 강조할 성함 선택", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 이미지에서 추출한 개인별 고유 색상 ---
color_map = {
    "황재업": "#D1FAE5", # 연한 초록
    "김태언": "#FFF2CC", # 이미지 확인 (노랑)
    "이태원": "#FFE5D9", # 이미지 확인 (살구/주황)
    "이정석": "#FDE2E2"  # 이미지 확인 (연분홍)
}

# --- [5] 근무 데이터 생성 (요일 셸 없이 통합) ---
cal_data = []
for i in range(duration):
    d = start_date + timedelta(days=i)
    diff = (d - PATTERN_START).days
    
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
        
        cal_data.append({
            "날짜": d.strftime("%m/%d(%a)"),
            "조장": "황재업", "성희": h, "의산A": a, "의산B": b
        })

df = pd.DataFrame(cal_data)

# --- [6] 스타일 적용 (요일 색상 + 개인 색상) ---
def apply_style(row):
    styles = [''] * len(row)
    # 토요일(파랑), 일요일(빨강) 색상 강조
    if 'Sun' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
    elif 'Sat' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
    
    # 사람별 고유 색상 강조
    if user_focus != "안 함":
        bg_color = color_map.get(user_focus, "#FFF2CC")
        for i, val in enumerate(row):
            if val == user_focus:
                styles[i] = f'background-color: {bg_color}; font-weight: bold; color: black;'
    return styles

# --- [7] 표 출력 (스크롤 없이 전체 노출) ---
if not df.empty:
    st.dataframe(
        df.style.apply(apply_style, axis=1),
        use_container_width=True,
        hide_index=True,
        height=(len(df) + 1) * 38 # 내부 스크롤 제거
    )
