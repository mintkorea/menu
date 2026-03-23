import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- [1] 핵심 설정 ---
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 근무 편성표", layout="wide")

# --- [2] CSS: 타이틀 크기 절반 축소 & 가독성 ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem !important; }
    /* 타이틀 폰트 크기 절반으로 축소 */
    .small-title { font-size: 24px !important; font-weight: bold; margin-bottom: 10px; }
    .stDataFrame div[data-testid="stTable"] { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# 타이틀 폰트 크기 조정 적용
st.markdown('<p class="small-title">📅 C조 근무 편성표</p>', unsafe_allow_html=True)

# --- [3] 사용자 강조 선택 ---
# 임의의 슬라이더 삭제, 기존 '사용자 확인' 기능 복구
user_focus = st.selectbox("👤 강조할 성함 선택", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 근무 데이터 생성 (경과된 근무 포함 고정 범위) ---
today = datetime.now().date()
cal_data = []

# 경과된 근무표 확인을 위해 과거(-15일)부터 미래(+45일)까지 자동 표기
for i in range(-15, 45):
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
    
    # 토요일(파랑), 일요일(빨강) 색상 강조
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

# 표 출력 (요일 셸 없이 날짜에 통합)
st.dataframe(
    df.style.apply(apply_style, axis=1),
    use_container_width=True,
    hide_index=True
)
