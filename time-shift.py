import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 및 데이터 ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

# --- 2. CSS 스타일 (폰트 확대 및 중앙 정렬) ---
st.markdown("""
    <style>
    /* 전체 폰트 크기 확대 */
    [data-testid="stMetricValue"] { font-size: 24px; }
    .stDataTable td, .stDataTable th { font-size: 16px !important; }
    
    /* 타이틀 디자인 */
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    .period-text { font-size: 18px; color: #555; text-align: center; margin-bottom: 20px; }
    
    /* 사이드바 폰트 확대 */
    [data-testid="stSidebar"] { font-size: 18px !important; }
    [data-testid="stSidebar"] .stSelectbox label { font-size: 18px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴", ["📅 교대 근무표", "📍 실시간 상황판"])
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업"] + WORKERS)
    duration = st.number_input("📅 조회 기간(개월)", min_value=1, max_value=6, value=1)

# --- 4. 근무표 생성 로직 ---
now = datetime.now().date()
end_date = now + timedelta(days=30 * duration)

if menu == "📅 교대 근무표":
    st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='period-text'>({now.strftime('%m월 %d일')} ~ {end_date.strftime('%m월 %d일')})</div>", unsafe_allow_html=True)

    cal_list = []
    curr = now
    while curr <= end_date:
        diff = (curr - START_DATE).days
        if diff % 3 == 0:
            s = (diff // 3) % 3
            wd = curr.weekday()
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "회관": WORKERS[(0+s)%3],
                "의산A": WORKERS[(1+s)%3],
                "의산B": WORKERS[(2+s)%3],
                "조장": "황재업",
                "weekday": wd  # 스타일링용 데이터
            })
        curr += timedelta(days=1)

    df_cal = pd.DataFrame(cal_list)

    # --- 5. 스타일 및 출력 (인덱스/weekday 완전 제거) ---
    def color_row(row):
        # 주말 색상 텍스트 결정
        color = "black"
        if row.weekday == 5: color = "#1E88E5" # 토요일
        elif row.weekday == 6: color = "#E53935" # 일요일
        
        # 전체 행 스타일 (배경색은 본인 이름 강조 시에만 적용)
        bg_color = "white"
        if user_name != "안 함" and user_name in row.values:
            bg_color = WORKER_COLORS.get(user_name, "white")
            
        return [f'background-color: {bg_color}; color: {color if col=="날짜" else "black"}; font-weight: {"bold" if col=="날짜" else "normal"}' for col in row.index]

    # 데이터프레임 스타일 적용 후 weekday 숨기기
    styled_df = df_cal.style.apply(color_row, axis=1).hide(axis="columns", subset=["weekday"])

    # st.table 대신 st.dataframe의 정적 모드를 사용하여 인덱스를 숨김
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,  # 왼쪽 숫자(인덱스) 열을 완전히 삭제
    )

elif menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>C조 실시간 근무 상황판</div>", unsafe_allow_html=True)
    # 기반 상황판 로직 추가 가능
    st.info("실시간 상황판 메뉴입니다. 날짜를 선택하여 상세 일정을 확인하세요.")
