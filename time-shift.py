import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 데이터 및 개인 칼라 설정 ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]

# 근무자별 고유 색상 (본인 근무 확인용)
WORKER_COLORS = {
    "황재업": "#E1F5FE",  # 연하늘
    "이태원": "#F3E5F5",  # 연보라
    "김태언": "#E8F5E9",  # 연초록
    "이정석": "#FFFDE7"   # 연노랑
}

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

# --- 2. 페이지 및 CSS 설정 ---
st.set_page_config(page_title="C조 통합 허브", layout="centered")
st.markdown(f"""
    <style>
    /* 전체 중앙 정렬 및 폰트 최적화 */
    .main {{ display: flex; justify-content: center; }}
    html, body, [data-testid="stTable"] {{ font-size: 9px !important; text-align: center !important; }}
    
    /* 표 중앙 정렬 */
    table {{ margin-left: auto; margin-right: auto; width: 100% !important; table-layout: fixed !important; }}
    th, td {{ text-align: center !important; padding: 4px 1px !important; border: 1px solid #eee; }}

    /* 요일 색상 */
    .sat {{ color: #1E88E5 !important; font-weight: bold; }} /* 토요일 파랑 */
    .sun {{ color: #E53935 !important; font-weight: bold; }} /* 일요일 빨강 */
    
    .main-title {{ font-size: 18px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 10px; }}
    .status-card {{ background-color: #fcfcfc; border: 1px solid #ddd; padding: 10px; border-radius: 8px; margin-bottom: 15px; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 로직 처리 (날짜 및 시간) ---
now = datetime.now()
current_hour = now.hour

with st.sidebar:
    st.header("⚙️ 메뉴")
    menu = st.radio("보기 선택", ["📍 실시간 상황판", "📅 교대 근무표"])
    st.divider()
    user_name = st.selectbox("본인 이름 선택 (강조용)", ["선택 안함"] + ["황재업"] + WORKERS)

# --- 4. 메인 화면 ---
if menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>📋 C조 실시간 상황판</div>", unsafe_allow_html=True)
    
    # 날짜 선택기 중앙 배치용 컬럼
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        selected_date = st.date_input("", now.date())
    
    days_diff = (selected_date - START_DATE).days
    if days_diff % 3 == 0:
        shift = (days_diff // 3) % 3
        w_h, w_a, w_b = WORKERS[(0+shift)%3], WORKERS[(1+shift)%3], WORKERS[(2+shift)%3]
        
        # 상단 현재 상태 요약
        cur = next((r for r in BASE_PATTERN if r["시간"] == current_hour), None)
        if cur and selected_date == now.date():
            st.markdown(f"""
            <div class='status-card'>
                <b>현재({now.strftime('%H:%M')}) 위치</b><br>
                조장: {cur['조']} | 회관({w_h}): {cur['회']} | A({w_a}): {cur['A']} | B({w_b}): {cur['B']}
            </div>
            """, unsafe_allow_html=True)

        # 표 데이터 생성
        df_list = []
        for r in BASE_PATTERN:
            df_list.append({"시간": r["표시"], "황재업(조)": r["조"], f"{w_h}(회)": r["회"], f"{w_a}(A)": r["A"], f"{w_b}(B)": r["B"]})
        df = pd.DataFrame(df_list)

        def style_board(row):
            is_now = (int(row['시간'].split(':')[0]) == current_hour) and (selected_date == now.date())
            styles = []
            for i, val in enumerate(row):
                bg, text, weight, border = "white", "black", "normal", "none"
                col_name = df.columns[i]
                
                # 본인 열 강조 (사이드바 선택 시)
                if user_name != "선택 안함" and user_name in col_name:
                    bg = WORKER_COLORS.get(user_name, "white")
                
                # 업무별 색상
                if '순찰' in str(val): text = "#1565C0"; weight = "bold"
                elif '식' in str(val): text = "#EF6C00"; weight = "bold"
                
                # 현재 시간 줄 강조
                if is_now: bg = "#FFF9C4"; border = "1.5px solid red"; weight = "bold"
                
                styles.append(f'background-color: {bg}; color: {text}; font-weight: {weight}; border: {border};')
            return styles

        st.table(df.style.apply(style_board, axis=1))
    else:
        st.warning("비번(휴무) 일자입니다.")

elif menu == "📅 교대 근무표":
    st.markdown("<div class='main-title'>📅 C조 월간 근무 일정</div>", unsafe_allow_html=True)
    
    start_v = datetime.now().date()
    end_v = start_v + timedelta(days=31)
    
    cal_data = []
    curr = start_v
    while curr <= end_v:
        diff = (curr - START_DATE).days
        if diff % 3 == 0:
            s = (diff // 3) % 3
            # 요일 클래스 결정
            wd = curr.weekday()
            day_str = curr.strftime("%m/%d")
            weekday_name = ["월", "화", "수", "목", "금", "토", "일"][wd]
            
            cal_data.append({
                "날짜": f"{day_str}({weekday_name})",
                "회관": WORKERS[(0+s)%3],
                "의산A": WORKERS[(1+s)%3],
                "의산B": WORKERS[(2+s)%3],
                "조장": "황재업",
                "weekday": wd
            })
        curr += timedelta(days=1)
    
    cal_df = pd.DataFrame(cal_data)
    
    def style_cal(row):
        styles = []
        # 토요일(5), 일요일(6) 색상 구분
        color = "black"
        if row['weekday'] == 5: color = "#1E88E5"
        elif row['weekday'] == 6: color = "#E53935"
        
        for i, val in enumerate(row):
            bg = "white"
            # 본인 근무 강조
            if user_name != "선택 안함" and user_name == str(val):
                bg = WORKER_COLORS.get(user_name, "white")
            styles.append(f'color: {color}; background-color: {bg}; font-weight: bold;' if i==0 else f'background-color: {bg};')
        return styles

    st.table(cal_df.drop(columns=['weekday']).style.apply(style_cal, axis=1))
