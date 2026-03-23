import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [1] 기본 설정 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표", layout="wide")

# --- [2] CSS: 타이틀 가시성 및 표 스타일 ---
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; }
    
    .fixed-title { 
        font-size: 24px !important; 
        font-weight: 800 !important;
        margin-bottom: 20px !important;
        color: #1E1E1E !important;
        padding-bottom: 10px;
        border-bottom: 2px solid #f0f2f6;
    }
    
    [data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="fixed-title">📅 C조 근무 편성표</div>', unsafe_allow_html=True)

# --- [3] 조회 설정 ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    # 이미지의 날짜 선택 방식 반영
    start_date = st.date_input("📅 조회 시작 날짜", datetime(2026, 3, 16).date())
with col2:
    # 이미지의 슬라이더 범위 반영
    duration = st.slider("📆 조회 일수", 7, 100, 31)
with col3:
    user_focus = st.selectbox("👤 강조할 성함", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 이미지에서 추출한 개인별 고유 색상 적용 ---
# 이미지 분석 결과: 김태언(노랑), 이태원(살구/베이지), 이정석(분홍)
color_map = {
    "황재업": "#D1FAE5", # 연한 초록 (임의 유지)
    "김태언": "#FFF2CC", # 이미지 확인 색상
    "이태원": "#FFE5D9", # 이미지 확인 색상 (살구색 계열)
    "이정석": "#FDE2E2"  # 이미지 확인 색상 (연분홍 계열)
}

# --- [5] 데이터 생성 및 로직 ---
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

def apply_style(row):
    styles = [''] * len(row)
    # 이미지의 토요일(파랑), 일요일(빨강) 강조 반영
    if 'Sun' in row['날짜']: styles[0] = 'color: red; font-weight: bold'
    elif 'Sat' in row['날짜']: styles[0] = 'color: blue; font-weight: bold'
    
    if user_focus != "안 함":
        bg_color = color_map.get(user_focus, "#FFF2CC")
        for i, val in enumerate(row):
            if val == user_focus:
                styles[i] = f'background-color: {bg_color}; font-weight: bold; color: black;'
    return styles

# --- [6] 표 출력 (스크롤 없이 전체 노출) ---
if not df.empty:
    st.dataframe(
        df.style.apply(apply_style, axis=1),
        use_container_width=True,
        hide_index=True,
        height=(len(df) + 1) * 38 # 스크롤 제거를 위해 높이 자동 조절
    )
