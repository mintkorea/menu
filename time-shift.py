import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 데이터 설정 (3/24 패턴 마지막 날 반영) ---
# 3/24 근무: 이태원(회), 이정석(A), 김태언(B) -> 이 패턴이 '마지막'이므로
# 3/27 근무는 로테이션상 다음 순번이 시작되어야 함.
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "이정석", "김태언"] 
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "이정석": "#FFFDE7", "김태언": "#E8F5E9"}

# 시간표 패턴 (이미지 image_499070.png 기반)
BASE_PATTERN = [
    {"시간": "07:00", "조": "안내실", "회": "로비", "A": "휴게", "B": "로비"},
    {"시간": "08:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴게"},
    {"시간": "09:00", "조": "안내실", "회": "순찰", "A": "로비", "B": "휴게"},
    {"시간": "10:00", "조": "휴게", "회": "안내실", "A": "순찰/휴", "B": "로비"},
    {"시간": "11:00", "조": "안내실", "회": "중식", "A": "중식", "B": "로비"},
    {"시간": "12:00", "조": "중식", "회": "안내실", "A": "로비", "B": "중식"},
    {"시간": "13:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴/순"},
    {"시간": "14:00", "조": "순찰", "회": "안내실", "A": "휴게", "B": "로비"},
    {"시간": "15:00", "조": "안내실", "회": "휴게", "A": "휴게", "B": "로비"},
    {"시간": "16:00", "조": "휴게", "회": "안내실", "A": "로비", "B": "휴게"},
    {"시간": "17:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴게"},
    {"시간": "18:00", "조": "안내실", "회": "휴게", "A": "휴게", "B": "로비"},
    {"시간": "19:00", "조": "안내실", "회": "석식", "A": "로비", "B": "석식"},
    {"시간": "20:00", "조": "안내실", "회": "안내실", "A": "석식", "B": "로비"},
    {"시간": "21:00", "조": "석식", "회": "안내실", "A": "로비", "B": "휴게"},
    {"시간": "22:00", "조": "안내실", "회": "순찰", "A": "로비", "B": "휴게"},
    {"시간": "23:00", "조": "순찰", "회": "취침", "A": "순찰", "B": "로비"},
    {"시간": "00:00", "조": "안내실", "회": "취침", "A": "취침", "B": "로비"},
    {"시간": "01:00", "조": "안내실", "회": "취침", "A": "취침", "B": "로비"},
    {"시간": "02:00", "조": "안내실", "회": "취침", "A": "취침", "B": "로비"},
    {"시간": "03:00", "조": "취침", "회": "회관근무", "A": "로비", "B": "취침"},
    {"시간": "04:00", "조": "취침", "회": "회관근무", "A": "로비", "B": "취침"},
    {"시간": "05:00", "조": "취침", "회": "회관근무", "A": "로비", "B": "취침"},
    {"시간": "06:00", "조": "안내실", "회": "회관근무", "A": "로비", "B": "순찰"},
]

# --- 2. CSS 및 정렬 설정 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 20px; }
    /* 표 내용 중앙 정렬 */
    [data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th { text-align: center !important; font-size: 16px !important; }
    /* 불필요한 공백 제거 */
    .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴", ["📅 교대 근무표", "📍 근무 상황판"])
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업"] + WORKERS)

# --- 4. 메인 화면 로직 ---
now = datetime.now()

if menu == "📅 교대 근무표":
    st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    
    cal_data = []
    curr = now.date()
    # 3/24를 포함하여 향후 40일간 표시
    display_start = min(curr, datetime(2026, 3, 24).date())
    display_end = display_start + timedelta(days=40)
    
    temp_date = display_start
    while temp_date <= display_end:
        diff = (temp_date - START_DATE).days
        if diff % 3 == 0:
            s = (diff // 3) % 3
            wd = temp_date.weekday()
            # [수정] weekday 열을 아예 데이터에 포함시키지 않음
            cal_data.append({
                "날짜": f"{temp_date.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": "황재업",
                "회관": WORKERS[(0+s)%3],
                "의산A": WORKERS[(1+s)%3],
                "의산B": WORKERS[(2+s)%3]
            })
        temp_date += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_data)
    
    # 스타일 함수
    def apply_cal_style(row):
        bg = WORKER_COLORS.get(user_name, "white") if user_name in row.values else "white"
        f_color = "#E53935" if "일" in row["날짜"] else ("#1E88E5" if "토" in row["날짜"] else "black")
        return [f'background-color: {bg}; color: {f_color if c=="날짜" else "black"}; font-weight: {"bold" if c=="날짜" else "normal"}' for c in row.index]

    # 중앙 정렬 레이아웃
    _, mid, _ = st.columns([0.1, 9.8, 0.1])
    with mid:
        st.dataframe(df_cal.style.apply(apply_cal_style, axis=1), use_container_width=True, hide_index=True)

elif menu == "📍 근무 상황판":
    st.markdown("<div class='main-title'>C조 근무 상황판</div>", unsafe_allow_html=True)
    sel_date = st.date_input("📅 날짜 선택", now.date())
    
    diff = (sel_date - START_DATE).days
    if diff % 3 == 0:
        s = (diff // 3) % 3
        w_h, w_a, w_b = WORKERS[(0+s)%3], WORKERS[(1+s)%3], WORKERS[(2+s)%3]
        
        board_data = []
        for r in BASE_PATTERN:
            board_data.append({
                "시간": r["시간"],
                "황재업(조)": r["조"],
                f"{w_h}(회)": r["회"],
                f"{w_a}(A)": r["A"],
                f"{w_b}(B)": r["B"]
            })
        
        df_board = pd.DataFrame(board_data)
        
        def apply_board_style(row):
            is_now = (int(row['시간'].split(':')[0]) == now.hour) and (sel_date == now.date())
            bg = "#FFF9C4" if is_now else "white"
            return [f'background-color: {bg}; border: {"1.5px solid red" if is_now else "1px solid #ddd"}' for _ in row.index]

        _, mid, _ = st.columns([0.1, 9.8, 0.1])
        with mid:
            st.dataframe(df_board.style.apply(apply_board_style, axis=1), use_container_width=True, hide_index=True)
    else:
        st.info(f"💡 {sel_date.strftime('%m/%d')}은 C조 비번(휴무)입니다.")
