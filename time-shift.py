import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 데이터 설정 ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]

# 시간대별 기본 패턴
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

# --- 2. 페이지 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 허브", layout="centered")
st.markdown("""
    <style>
    html, body, [data-testid="stTable"] { font-size: 9px !important; }
    .main-title { font-size: 18px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .status-card { background-color: #F0F9FF; border-left: 4px solid #0EA5E9; padding: 10px; border-radius: 4px; margin-bottom: 10px; }
    .worker-tag { font-weight: bold; color: #0369A1; font-size: 10px; }
    .current-status { font-size: 11px; font-weight: bold; color: #D32F2F; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 컨트롤 (메뉴 전환 및 기간 설정) ---
with st.sidebar:
    st.header("⚙️ 메뉴 설정")
    menu = st.radio("보기 선택", ["📍 실시간 상황판", "📅 교대 근무표"])
    st.divider()
    if menu == "📅 교대 근무표":
        st.subheader("기간 조회")
        start_view = st.date_input("조회 시작일", datetime.now().date())
        duration = st.number_input("조회 기간(개월)", min_value=1, max_value=12, value=1)
        end_view = start_view + timedelta(days=30 * duration)

# --- 4. 메인 로직 ---
now = datetime.now()
current_hour = now.hour

if menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>📋 C조 실시간 근무 상황판</div>", unsafe_allow_html=True)
    selected_date = st.date_input("날짜 선택", now.date())
    
    days_diff = (selected_date - START_DATE).days
    if days_diff % 3 == 0:
        shift = (days_diff // 3) % 3
        w_h, w_a, w_b = WORKERS[(0+shift)%3], WORKERS[(1+shift)%3], WORKERS[(2+shift)%3]

        # [수정] 당일 근무 편성 및 현재 상태 표시
        cur = next((r for r in BASE_PATTERN if r["시간"] == current_hour), None)
        
        st.success(f"✅ 오늘 근무자: **{w_h}(회), {w_a}(A), {w_b}(B)**")
        
        if cur and selected_date == now.date():
            st.markdown(f"""
            <div class='status-card'>
                <div style='margin-bottom:5px;'>⏱️ <b>현재 시간({now.strftime('%H:%M')}) 위치 및 상태</b></div>
                <span class='worker-tag'>황재업(조):</span> {cur['조']} | 
                <span class='worker-tag'>{w_h}(회관):</span> <span class='current-status'>{cur['회']}</span><br>
                <span class='worker-tag'>{w_a}(의산A):</span> <span class='current-status'>{cur['A']}</span> | 
                <span class='worker-tag'>{w_b}(의산B):</span> <span class='current-status'>{cur['B']}</span>
            </div>
            """, unsafe_allow_html=True)

        # 테이블 표시
        display_df = []
        for r in BASE_PATTERN:
            display_df.append({"시간": r["표시"], "황재업(조)": r["조"], f"{w_h}(회)": r["회"], f"{w_a}(A)": r["A"], f"{w_b}(B)": r["B"]})
        
        df = pd.DataFrame(display_df)

        def apply_style(row):
            is_now = (int(row['시간'].split(':')[0]) == current_hour) and (selected_date == now.date())
            styles = []
            for val in row:
                bg, text, weight, border = "transparent", "black", "normal", "none"
                v = str(val); 
                if '순찰' in v: bg = "#E3F2FD"; text = "#1565C0"; weight = "bold"
                elif '식' in v: bg = "#FFF3E0"; text = "#E65100"; weight = "bold"
                elif '로비' in v: text = "#D32F2F"; weight = "bold"
                if is_now: bg = "#FFF9C4"; border = "1.2px solid red"; weight = "bold"
                styles.append(f'background-color: {bg}; color: {text}; font-weight: {weight}; border: {border};')
            return styles

        st.table(df.style.apply(apply_style, axis=1))
    else:
        st.warning("휴무일입니다.")

elif menu == "📅 교대 근무표":
    st.markdown("<div class='main-title'>🗓️ C조 교대 근무 일정 (1개월)</div>", unsafe_allow_html=True)
    
    schedule_data = []
    curr = start_view
    while curr <= end_view:
        diff = (curr - START_DATE).days
        if diff % 3 == 0:
            s = (diff // 3) % 3
            schedule_data.append({
                "날짜": curr.strftime("%m/%d(%a)"),
                "회관": WORKERS[(0+s)%3],
                "의산A": WORKERS[(1+s)%3],
                "의산B": WORKERS[(2+s)%3],
                "조장": "황재업"
            })
        curr += timedelta(days=1)
    
    if schedule_data:
        st.table(pd.DataFrame(schedule_data))
    else:
        st.info("해당 기간에 근무일이 없습니다.")
