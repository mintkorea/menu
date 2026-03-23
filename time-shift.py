import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 데이터 및 개인/연차 설정 ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]

# [추가] 연차 데이터 관리 (날짜: [이름들])
ANNUAL_LEAVE = {
    "2026-03-24": ["김태언"],  # 예시: 3월 24일 김태언 연차
    "2026-03-27": ["이태원", "이정석"],
}

WORKER_COLORS = {
    "황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"
}

# 기본 근무 패턴 (동일)
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
st.markdown("""
    <style>
    html, body, [data-testid="stTable"] { font-size: 9px !important; text-align: center !important; }
    table { margin-left: auto; margin-right: auto; width: 100% !important; table-layout: fixed !important; }
    th, td { text-align: center !important; padding: 4px 1px !important; border: 1px solid #eee; }
    .leave-text { color: #D32F2F; font-weight: bold; background-color: #FFEBEE; padding: 2px; border-radius: 3px; }
    .sat { color: #1E88E5 !important; font-weight: bold; }
    .sun { color: #E53935 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 공통 로직 ---
now = datetime.now()
current_hour = now.hour

with st.sidebar:
    st.header("⚙️ 메뉴")
    menu = st.radio("보기 선택", ["📍 실시간 상황판", "📅 교대 근무표"])
    user_name = st.selectbox("본인 이름 강조", ["선택 안함", "황재업"] + WORKERS)

# --- 4. 메인 화면 ---
if menu == "📍 실시간 상황판":
    selected_date = st.date_input("날짜 선택", now.date())
    date_key = selected_date.strftime("%Y-%m-%d")
    leaves = ANNUAL_LEAVE.get(date_key, [])

    days_diff = (selected_date - START_DATE).days
    if days_diff % 3 == 0:
        shift = (days_diff // 3) % 3
        w_h, w_a, w_b = WORKERS[(0+shift)%3], WORKERS[(1+shift)%3], WORKERS[(2+shift)%3]
        
        # 연차자 안내 메시지
        if leaves:
            st.error(f"🚩 오늘 연차자: {', '.join(leaves)}")

        # 표 데이터 생성 (연차 시 '연차'로 텍스트 치환)
        df_list = []
        for r in BASE_PATTERN:
            df_list.append({
                "시간": r["표시"],
                "황재업(조)": "연차" if "황재업" in leaves else r["조"],
                f"{w_h}(회)": "연차" if w_h in leaves else r["회"],
                f"{w_a}(A)": "연차" if w_a in leaves else r["A"],
                f"{w_b}(B)": "연차" if w_b in leaves else r["B"]
            })
        df = pd.DataFrame(df_list)

        def style_board(row):
            is_now = (int(row['시간'].split(':')[0]) == current_hour) and (selected_date == now.date())
            styles = []
            for i, val in enumerate(row):
                bg, text, weight, border = "white", "black", "normal", "none"
                col_name = df.columns[i]
                
                if user_name != "선택 안함" and user_name in col_name:
                    bg = WORKER_COLORS.get(user_name, "white")
                
                # 연차 스타일 (빨간 배경/글씨)
                if val == "연차":
                    bg = "#FFEBEE"; text = "#D32F2F"; weight = "bold"
                elif '순찰' in str(val): text = "#1565C0"; weight = "bold"
                elif '식' in str(val): text = "#EF6C00"; weight = "bold"
                
                if is_now: bg = "#FFF9C4"; border = "1.2px solid red"; weight = "bold"
                styles.append(f'background-color: {bg}; color: {text}; font-weight: {weight}; border: {border};')
            return styles

        st.table(df.style.apply(style_board, axis=1))
    else:
        st.warning("비번(휴무) 일자입니다.")

elif menu == "📅 교대 근무표":
    start_v = datetime.now().date()
    cal_data = []
    for i in range(31):
        curr = start_v + timedelta(days=i)
        diff = (curr - START_DATE).days
        if diff % 3 == 0:
            s = (diff // 3) % 3
            d_key = curr.strftime("%Y-%m-%d")
            d_leaves = ANNUAL_LEAVE.get(d_key, [])
            
            # 근무자 이름 옆에 (연차) 표시
            def fmt(name): return f"{name}(연차)" if name in d_leaves else name

            cal_data.append({
                "날짜": curr.strftime("%m/%d(%a)"),
                "회관": fmt(WORKERS[(0+s)%3]),
                "의산A": fmt(WORKERS[(1+s)%3]),
                "의산B": fmt(WORKERS[(2+s)%3]),
                "조장": fmt("황재업"),
                "weekday": curr.weekday()
            })
    
    cal_df = pd.DataFrame(cal_data)
    
    def style_cal(row):
        styles = []
        f_color = "black"
        if row['weekday'] == 5: f_color = "#1E88E5"
        elif row['weekday'] == 6: f_color = "#E53935"
        
        for i, col_name in enumerate(row.index):
            if col_name == "weekday": styles.append(""); continue
            bg = "white"
            val = str(row[col_name])
            if "(연차)" in val: bg = "#FFEBEE"
            if user_name != "선택 안함" and user_name in val:
                bg = WORKER_COLORS.get(user_name, "white")
            
            s = f'background-color: {bg};'
            if col_name == "날짜": s += f' color: {f_color}; font-weight: bold;'
            styles.append(s)
        return styles

    st.table(cal_df.style.apply(style_cal, axis=1).hide(axis="columns", subset=["weekday"]))
