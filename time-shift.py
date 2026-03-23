import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 데이터 설정 ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

# --- 2. CSS 스타일 설정 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    .period-text { font-size: 18px; color: #555; text-align: center; margin-bottom: 20px; }
    [data-testid="stSidebar"] { font-size: 18px !important; }
    [data-testid="stSidebar"] .stRadio > label, [data-testid="stSidebar"] .stSelectbox label { 
        font-size: 18px !important; font-weight: bold !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴", ["📅 교대 근무표", "📍 근무 상황판"])
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업"] + WORKERS)
    if menu == "📅 교대 근무표":
        duration = st.number_input("📅 조회 기간(개월)", min_value=1, max_value=6, value=1)

# --- 4. 근무표 로직 ---
now = datetime.now()

if menu == "📅 교대 근무표":
    start_v = now.date()
    end_v = start_v + timedelta(days=30 * duration)
    st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='period-text'>({start_v.strftime('%m월 %d일')} ~ {end_v.strftime('%m월 %d일')})</div>", unsafe_allow_html=True)

    cal_list = []
    curr = start_v
    while curr <= end_v:
        diff = (curr - START_DATE).days
        if diff % 3 == 0:
            s = (diff // 3) % 3
            wd = curr.weekday()
            # 데이터 생성 시 'weekday'를 별도 열로 만들지 않고 로직에서만 사용
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": "황재업",
                "회관": WORKERS[(0+s)%3],
                "의산A": WORKERS[(1+s)%3],
                "의산B": WORKERS[(2+s)%3]
            })
        curr += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)

    # 주말 색상을 입히기 위해 '날짜' 열의 텍스트를 기준으로 스타일 적용
    def style_row(row):
        bg_color = WORKER_COLORS.get(user_name, "white") if user_name != "안 함" and user_name in row.values else "white"
        
        # 날짜 텍스트에서 요일 추출하여 색상 결정
        date_text = str(row["날짜"])
        font_color = "black"
        if "(토)" in date_text: font_color = "#1E88E5"
        elif "(일)" in date_text: font_color = "#E53935"
        
        return [f'background-color: {bg_color}; color: {font_color if col=="날짜" else "black"}; font-weight: {"bold" if col=="날짜" else "normal"}' for col in row.index]

    # hide_index=True를 통해 왼쪽 인덱스 숫자도 삭제
    st.dataframe(
        df_cal.style.apply(style_row, axis=1),
        use_container_width=True,
        hide_index=True 
    )

elif menu == "📍 근무 상황판":
    # 상황판 로직 (이전과 동일하게 유지하되 인덱스 삭제 적용)
    st.markdown("<div class='main-title'>C조 근무 상황판</div>", unsafe_allow_html=True)
    selected_date = st.date_input("📅 날짜 선택", now.date())
    # ... (상황판 세부 코드 생략, 출력 시 hide_index=True 적용)
