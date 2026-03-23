import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 데이터 설정 ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

# [이미지 기반] 시간대별 근무 패턴
BASE_PATTERN = [
    {"시간": 7, "표시": "07:00", "조": "안내실", "회": "로비", "A": "휴게", "B": "로비"},
    {"시간": 8, "표시": "08:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴게"},
    {"시간": 9, "표시": "09:00", "조": "안내실", "회": "순찰", "A": "로비", "B": "휴게"},
    {"시간": 10, "표시": "10:00", "조": "휴게", "회": "안내실", "A": "순찰/휴", "B": "로비"},
    {"시간": 11, "표시": "11:00", "조": "안내실", "회": "중식", "A": "중식", "B": "로비"},
    {"시간": 12, "표시": "12:00", "조": "중식", "회": "안내실", "A": "로비", "B": "중식"},
    {"시간": 13, "표시": "13:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴/순"},
    {"시간": 14, "표시": "14:00", "조": "순찰", "회": "안내실", "A": "휴게", "B": "로비"},
    {"시간": 15, "표시": "15:00", "조": "안내실", "회": "휴게", "A": "휴게", "B": "로비"},
    {"시간": 16, "표시": "16:00", "조": "휴게", "회": "안내실", "A": "로비", "B": "휴게"},
    {"시간": 17, "표시": "17:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴게"},
    {"시간": 18, "표시": "18:00", "조": "안내실", "회": "휴게", "A": "휴게", "B": "로비"},
    {"시간": 19, "표시": "19:00", "조": "안내실", "회": "석식", "A": "로비", "B": "석식"},
    {"시간": 20, "표시": "20:00", "조": "안내실", "회": "안내실", "A": "석식", "B": "로비"},
    {"시간": 21, "표시": "21:00", "조": "석식", "회": "안내실", "A": "로비", "B": "휴게"},
    {"시간": 22, "표시": "22:00", "조": "안내실", "회": "순찰", "A": "로비", "B": "휴게"},
    {"시간": 23, "표시": "23:00", "조": "순찰", "회": "취침", "A": "순찰", "B": "로비"},
    {"시간": 0, "표시": "00:00", "조": "안내실", "회": "취침", "A": "취침", "B": "로비"},
    {"시간": 1, "표시": "01:00", "조": "안내실", "회": "취침", "A": "취침", "B": "로비"},
    {"시간": 2, "표시": "02:00", "조": "안내실", "회": "취침", "A": "취침", "B": "로비"},
    {"시간": 3, "표시": "03:00", "조": "취침", "회": "회관근무", "A": "로비", "B": "취침"},
    {"시간": 4, "표시": "04:00", "조": "취침", "회": "회관근무", "A": "로비", "B": "취침"},
    {"시간": 5, "표시": "05:00", "조": "취침", "회": "회관근무", "A": "로비", "B": "취침"},
    {"시간": 6, "표시": "06:00", "조": "안내실", "회": "회관근무", "A": "로비", "B": "순찰"},
]

# --- 2. CSS 스타일 설정 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    .period-text { font-size: 18px; color: #555; text-align: center; margin-bottom: 20px; }
    /* 사이드바 폰트 확대 */
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

# --- 4. 메인 로직 ---
now = datetime.now()

if menu == "📅 교대 근무표":
    # 1. 기간 및 타이틀
    start_v = now.date()
    end_v = start_v + timedelta(days=30 * duration)
    st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='period-text'>({start_v.strftime('%m월 %d일')} ~ {end_v.strftime('%m월 %d일')})</div>", unsafe_allow_html=True)

    # 2. 데이터 생성 (조장을 날짜 바로 뒤로 배치)
    cal_list = []
    curr = start_v
    while curr <= end_v:
        diff = (curr - START_DATE).days
        if diff % 3 == 0:
            s = (diff // 3) % 3
            wd = curr.weekday()
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": "황재업", # 조장을 앞으로 배치
                "회관": WORKERS[(0+s)%3],
                "의산A": WORKERS[(1+s)%3],
                "의산B": WORKERS[(2+s)%3],
                "weekday": wd
            })
        curr += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)

    # 3. 스타일 및 출력 (인덱스/weekday 완전 삭제)
    def style_cal(row):
        date_color = "#E53935" if row.weekday == 6 else ("#1E88E5" if row.weekday == 5 else "black")
        bg_color = WORKER_COLORS.get(user_name, "white") if user_name != "안 함" and user_name in row.values else "white"
        return [f'background-color: {bg_color}; color: {date_color if col=="날짜" else "black"}; font-weight: {"bold" if col=="날짜" else "normal"}' for col in row.index]

    st.dataframe(
        df_cal.style.apply(style_cal, axis=1).hide(axis="columns", subset=["weekday"]),
        use_container_width=True,
        hide_index=True # 왼쪽 숫자(인덱스) 열 삭제
    )

elif menu == "📍 근무 상황판":
    st.markdown("<div class='main-title'>C조 근무 상황판</div>", unsafe_allow_html=True)
    
    # 1. 날짜 선택 달력 추가
    selected_date = st.date_input("📅 조회 날짜를 선택하세요", now.date())
    
    days_diff = (selected_date - START_DATE).days
    if days_diff % 3 == 0:
        shift = (days_diff // 3) % 3
        w_h, w_a, w_b = WORKERS[(0+shift)%3], WORKERS[(1+shift)%3], WORKERS[(2+shift)%3]
        
        # 2. 시간표 생성
        st.markdown(f"**현재 시간 현황 ({now.strftime('%H:%M')})**")
        df_board = pd.DataFrame([
            {"시간": r["표시"], "황재업(조)": r["조"], f"{w_h}(회)": r["회"], f"{w_a}(A)": r["A"], f"{w_b}(B)": r["B"]} 
            for r in BASE_PATTERN
        ])

        def style_board(row):
            is_now = (int(row['시간'].split(':')[0]) == now.hour) and (selected_date == now.date())
            styles = []
            for col in df_board.columns:
                bg = "#FFF9C4" if is_now else "white"
                if user_name != "안 함" and user_name in col: bg = WORKER_COLORS.get(user_name, bg)
                styles.append(f'background-color: {bg}; border: {"1.5px solid red" if is_now else "1px solid #ddd"}')
            return styles

        st.dataframe(
            df_board.style.apply(style_board, axis=1),
            use_container_width=True,
            hide_index=True # 인덱스 삭제
        )
    else:
        st.warning("선택하신 날짜는 C조 휴무일(비번)입니다.")
