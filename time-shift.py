import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 데이터 설정 ---
# START_DATE 기준으로 3일 로테이션 계산
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

# 시간대별 근무 패턴 (이미지 기반 고정 데이터)
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

# --- 2. CSS 스타일 (표 중앙 정렬 및 폰트 확대) ---
st.set_page_config(page_title="성의교정 C조", layout="centered")
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    .period-text { font-size: 18px; color: #555; text-align: center; margin-bottom: 20px; }
    
    /* 사이드바 스타일 확대 */
    [data-testid="stSidebar"] { font-size: 18px !important; }
    [data-testid="stSidebar"] .stRadio > label, [data-testid="stSidebar"] .stSelectbox label { 
        font-size: 18px !important; font-weight: bold !important; 
    }
    
    /* 표 데이터 중앙 정렬 및 폰트 크기 */
    [data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th {
        text-align: center !important;
        font-size: 16px !important;
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
            # [수정] weekday 열은 아예 만들지 않고, 조장 열을 앞으로 배치
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": "황재업",
                "회관": WORKERS[(0+s)%3],
                "의산A": WORKERS[(1+s)%3],
                "의산B": WORKERS[(2+s)%3]
            })
        curr += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)

    # 행별 스타일 적용 (주말 색상 및 이름 강조)
    def style_cal(row):
        bg_color = WORKER_COLORS.get(user_name, "white") if user_name != "안 함" and user_name in row.values else "white"
        date_text = str(row["날짜"])
        font_color = "black"
        if "(토)" in date_text: font_color = "#1E88E5"
        elif "(일)" in date_text: font_color = "#E53935"
        
        return [f'background-color: {bg_color}; color: {font_color if col=="날짜" else "black"}; font-weight: {"bold" if col=="날짜" else "normal"}' for col in row.index]

    # [수정] 중앙 정렬 레이아웃 적용
    _, mid, _ = st.columns([0.5, 9, 0.5])
    with mid:
        st.dataframe(
            df_cal.style.apply(style_cal, axis=1),
            use_container_width=True,
            hide_index=True 
        )

elif menu == "📍 근무 상황판":
    st.markdown("<div class='main-title'>C조 근무 상황판 (전체 시간표)</div>", unsafe_allow_html=True)
    
    # [수정] 달력 추가
    selected_date = st.date_input("📅 조회 날짜 선택", now.date())
    
    days_diff = (selected_date - START_DATE).days
    if days_diff % 3 == 0:
        shift = (days_diff // 3) % 3
        w_h, w_a, w_b = WORKERS[(0+shift)%3], WORKERS[(1+shift)%3], WORKERS[(2+shift)%3]
        
        # 시간표 데이터 구성
        df_board = pd.DataFrame([
            {"시간": r["표시"], "황재업(조)": r["조"], f"{w_h}(회)": r["회"], f"{w_a}(A)": r["A"], f"{w_b}(B)": r["B"]} 
            for r in BASE_PATTERN
        ])

        def style_board(row):
            # 현재 시간 표시 (선택 날짜가 오늘일 때만)
            is_now = (int(row['시간'].split(':')[0]) == now.hour) and (selected_date == now.date())
            styles = []
            for col in df_board.columns:
                bg = "#FFF9C4" if is_now else "white"
                if user_name != "안 함" and user_name in col: bg = WORKER_COLORS.get(user_name, bg)
                styles.append(f'background-color: {bg}; border: {"1.5px solid red" if is_now else "1px solid #ddd"}')
            return styles

        _, mid, _ = st.columns([0.2, 9.6, 0.2])
        with mid:
            st.dataframe(
                df_board.style.apply(style_board, axis=1),
                use_container_width=True,
                hide_index=True
            )
    else:
        st.warning(f"⚠️ {selected_date.strftime('%m월 %d일')}은 C조 휴무일(비번)입니다.")
