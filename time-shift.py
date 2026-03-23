import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 데이터 설정 ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {
    "황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"
}

# --- 2. 페이지 및 스타일 설정 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")
st.markdown("""
    <style>
    /* 전체 폰트 크기 확대 */
    html, body, [data-testid="stTable"] { font-size: 14px !important; text-align: center !important; }
    
    /* 표 레이아웃: 인덱스 열 강제 숨기기 */
    thead tr th:first-child, tbody tr td:first-child { display: none !important; }
    
    table { margin-left: auto; margin-right: auto; width: 100% !important; table-layout: fixed !important; border-collapse: collapse; }
    th, td { text-align: center !important; padding: 10px 5px !important; border: 1px solid #ddd !important; }
    th { background-color: #f8f9fa; font-weight: bold; }

    /* 타이틀 스타일 */
    .main-title { font-size: 24px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 10px; }
    .period-text { font-size: 16px; color: #444; text-align: center; margin-bottom: 25px; font-weight: 500; }
    
    /* 사이드바 스타일 확대 */
    [data-testid="stSidebar"] { font-size: 18px !important; min-width: 300px; }
    [data-testid="stSidebar"] .stRadio > label, [data-testid="stSidebar"] .stSelectbox label { 
        font-size: 18px !important; font-weight: bold !important; color: #1E3A8A; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 컨트롤 ---
with st.sidebar:
    st.header("📋 근무 설정")
    menu = st.radio("메뉴 선택", ["📅 교대 근무표", "📍 실시간 상황판"])
    st.divider()
    user_name = st.selectbox("본인 성함 강조", ["안 함", "황재업"] + WORKERS)
    if menu == "📅 교대 근무표":
        duration = st.number_input("조회 기간(개월)", min_value=1, max_value=12, value=1)

# --- 4. 근무표 로직 ---
now = datetime.now()

if menu == "📅 교대 근무표":
    # 기간 설정
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
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "회관": WORKERS[(0+s)%3],
                "의산A": WORKERS[(1+s)%3],
                "의산B": WORKERS[(2+s)%3],
                "조장": "황재업",
                "weekday": wd  # 스타일 처리용 (표시 안됨)
            })
        curr += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)
    
    # 스타일 적용 함수
    def apply_cal_style(row):
        styles = []
        f_color = "black"
        if row['weekday'] == 5: f_color = "#1E88E5" # 토요일 파랑
        elif row['weekday'] == 6: f_color = "#E53935" # 일요일 빨강
        
        for col in df_cal.columns:
            if col == "weekday": styles.append(""); continue # weekday 데이터는 스타일 미적용
            bg = "white"
            val = str(row[col])
            # 이름 강조
            if user_name != "안 함" and user_name == val:
                bg = WORKER_COLORS.get(user_name, "white")
            
            s = f'background-color: {bg};'
            if col == "날짜": s += f' color: {f_color}; font-weight: bold;'
            styles.append(s)
        return styles

    # weekday 열을 숨기고 출력
    st.table(df_cal.style.apply(apply_cal_style, axis=1).hide(axis="columns", subset=["weekday"]))

elif menu == "📍 실시간 상황판":
    # (상황판 코드는 이전과 동일하되, 스타일이 자동 적용됩니다)
    st.markdown("<div class='main-title'>성의교정 C조 실시간 상황판</div>", unsafe_allow_html=True)
    st.info("실시간 상황판은 선택한 날짜의 시간대별 위치를 보여줍니다.")
    # ... (상황판 세부 로직 생략 가능 - 필요시 이전 코드 유지)
