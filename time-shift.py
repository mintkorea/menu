import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 데이터 설정 ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]
WORKER_COLORS = {
    "황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"
}

# 시간대별 근무 패턴 데이터
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

# --- 2. 페이지 및 스타일 설정 (불필요 셀 제거 및 폰트 확대) ---
st.set_page_config(page_title="성의교정 C조", layout="centered")
st.markdown("""
    <style>
    /* 표 인덱스 열 숨기기 및 중앙 정렬 */
    thead tr th:first-child, tbody tr td:first-child { display: none; }
    
    /* 전체 폰트 크기 조정 */
    html, body, [data-testid="stTable"] { font-size: 11px !important; text-align: center !important; }
    table { margin-left: auto; margin-right: auto; width: 100% !important; table-layout: fixed !important; }
    th, td { text-align: center !important; padding: 6px 2px !important; border: 1px solid #eee; }
    
    /* 타이틀 및 텍스트 스타일 */
    .main-title { font-size: 22px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 10px; }
    .period-text { font-size: 14px; color: #444; text-align: center; margin-bottom: 20px; font-weight: 500; }
    
    /* 사이드바 폰트 크기 대폭 확대 */
    [data-testid="stSidebar"] { font-size: 16px !important; }
    [data-testid="stSidebar"] .stRadio > label { font-size: 18px !important; font-weight: bold !important; color: #1E3A8A; }
    [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stNumberInput label { 
        font-size: 18px !important; font-weight: bold !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 컨트롤 ---
with st.sidebar:
    st.header("📋 설정")
    menu = st.radio("보기 모드", ["📍 실시간 상황판", "📅 교대 근무표"])
    st.divider()
    user_name = st.selectbox("본인 강조 선택", ["안 함", "황재업"] + WORKERS)
    if menu == "📅 교대 근무표":
        duration = st.number_input("조회 기간(개월)", min_value=1, max_value=12, value=1)

# --- 4. 메인 로직 ---
now = datetime.now()
current_hour = now.hour

if menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>성의교정 C조 실시간 상황판</div>", unsafe_allow_html=True)
    selected_date = st.date_input("날짜 선택", now.date())
    
    days_diff = (selected_date - START_DATE).days
    if days_diff % 3 == 0:
        # 로테이션 계산
        shift = (days_diff // 3) % 3
        w_h, w_a, w_b = WORKERS[(0+shift)%3], WORKERS[(1+shift)%3], WORKERS[(2+shift)%3]
        
        # 현재 근무 요약
        cur = next((r for r in BASE_PATTERN if r["시간"] == current_hour), None)
        if cur and selected_date == now.date():
            st.success(f"⏱️ 현재 위치: {w_h}(회관) - {cur['회']} | {w_a}(의산A) - {cur['A']} | {w_b}(의산B) - {cur['B']}")

        # 상황판 테이블
        df_board = pd.DataFrame([{"시간": r["표시"], "황재업(조)": r["조"], f"{w_h}(회)": r["회"], f"{w_a}(A)": r["A"], f"{w_b}(B)": r["B"]} for r in BASE_PATTERN])

        def apply_board_style(row):
            is_now = (int(row['시간'].split(':')[0]) == current_hour) and (selected_date == now.date())
            styles = []
            for col in df_board.columns:
                bg, text, weight, border = "white", "black", "normal", "none"
                if user_name != "안 함" and user_name in col: bg = WORKER_COLORS.get(user_name, "white")
                if '순찰' in str(row[col]): text = "#1565C0"; weight = "bold"
                elif '식' in str(row[col]): text = "#EF6C00"; weight = "bold"
                if is_now: bg = "#FFF9C4"; border = "1.5px solid red"; weight = "bold"
                styles.append(f'background-color: {bg}; color: {text}; font-weight: {weight}; border: {border};')
            return styles

        st.table(df_board.style.apply(apply_board_style, axis=1))
    else:
        st.warning("휴무일입니다.")

elif menu == "📅 교대 근무표":
    # 기간 설정 및 타이틀 표시
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
                "회관": WORKERS[(0+s)%3], "의산A": WORKERS[(1+s)%3], "의산B": WORKERS[(2+s)%3], "조장": "황재업",
                "weekday": wd # 스타일용 임시 데이터
            })
        curr += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)
    
    def apply_cal_style(row):
        styles = []
        f_color = "black"
        if row['weekday'] == 5: f_color = "#1E88E5" # 토요일
        elif row['weekday'] == 6: f_color = "#E53935" # 일요일
        
        for col in df_cal.columns:
            if col == "weekday": styles.append(""); continue
            bg = "white"
            if user_name != "안 함" and user_name == str(row[col]): bg = WORKER_COLORS.get(user_name, "white")
            s = f'background-color: {bg};'
            if col == "날짜": s += f' color: {f_color}; font-weight: bold;'
            styles.append(s)
        return styles

    # 'weekday' 셀을 완전히 없애고 출력
    st.table(df_cal.style.apply(apply_cal_style, axis=1).hide(axis="columns", subset=["weekday"]))
