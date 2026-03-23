import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 데이터 설정 (이미지 패턴 분석 결과 반영) ---
# 3/24(화) 근무: 회관(이태원), 의산A(김태언), 의산B(이정석)
# 이 날이 패턴의 '마지막'이므로, START_DATE를 3/24로 잡고 로테이션 기준을 설정합니다.
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"] 
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

# [고정] 시간대별 근무 패턴 (image_499070.png 기준)
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

# --- 2. CSS 및 레이아웃 설정 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 20px; }
    [data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th { text-align: center !important; font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴", ["📅 교대 근무표", "📍 근무 상황판"])
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업"] + WORKERS)

# --- 4. 메인 화면 ---
now = datetime.now()

if menu == "📅 교대 근무표":
    st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    
    cal_data = []
    # 3/24부터 표시되도록 설정
    curr_date = datetime(2026, 3, 24).date()
    end_date = curr_date + timedelta(days=45)
    
    while curr_date <= end_date:
        diff = (curr_date - START_DATE).days
        if diff % 3 == 0:
            s = (diff // 3) % 3
            wd_idx = curr_date.weekday()
            # [핵심] weekday 열은 아예 생성하지 않음
            cal_data.append({
                "날짜": f"{curr_date.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd_idx]})",
                "조장": "황재업", # 조장 전진 배치
                "회관": WORKERS[(0+s)%3],
                "의산A": WORKERS[(1+s)%3],
                "의산B": WORKERS[(2+s)%3]
            })
        curr_date += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_data)
    
    def style_cal(row):
        bg = WORKER_COLORS.get(user_name, "white") if user_name in row.values else "white"
        f_color = "#E53935" if "일" in row["날짜"] else ("#1E88E5" if "토" in row["날짜"] else "black")
        return [f'background-color: {bg}; color: {f_color if c=="날짜" else "black"}' for c in row.index]

    # 중앙 정렬
    _, mid, _ = st.columns([0.1, 9.8, 0.1])
    with mid:
        st.dataframe(df_cal.style.apply(style_cal, axis=1), use_container_width=True, hide_index=True)

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
        
        # 현재 시간 하이라이트 (오늘 날짜일 때만)
        def style_board(row):
            is_now = (int(row['시간'].split(':')[0]) == now.hour) and (sel_date == now.date())
            bg = "#FFF9C4" if is_now else "white"
            return [f'background-color: {bg}; border: {"1.2px solid red" if is_now else "none"}' for _ in row.index]

        _, mid, _ = st.columns([0.1, 9.8, 0.1])
        with mid:
            st.dataframe(df_board.style.apply(style_board, axis=1), use_container_width=True, hide_index=True)
    else:
        st.info("💡 해당 날짜는 C조 비번(휴무)입니다.")
