import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 정밀 근무 패턴 데이터 (이미지 100% 대조) ---
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

# --- 2. 로테이션 설정 (3/24 기준) ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]

# --- 3. 페이지 및 CSS 설정 ---
st.set_page_config(layout="centered")
st.markdown("""
    <style>
    html, body, [data-testid="stTable"] { font-size: 9px !important; }
    table { width: 100% !important; table-layout: fixed !important; border-collapse: collapse; }
    th, td { padding: 3px 1px !important; text-align: center !important; border: 1px solid #f0f0f0; }
    .status-box { padding: 10px; border-radius: 5px; background-color: #f8f9fa; margin-bottom: 10px; border-left: 5px solid #007bff; }
    .worker-name { font-size: 11px; font-weight: bold; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 타이틀 및 날짜 처리 ---
st.title("📋 C조 근무 상황판")
now = datetime.now()
current_hour = now.hour
selected_date = st.date_input("날짜 선택", now.date())

days_diff = (selected_date - START_DATE).days

if days_diff % 3 == 0:
    # 로테이션 순번 계산
    shift = (days_diff // 3) % 3
    lineup = [WORKERS[(0+shift)%3], WORKERS[(1+shift)%3], WORKERS[(2+shift)%3]]
    w_h, w_a, w_b = lineup[0], lineup[1], lineup[2]

    # --- 5. 당일 근무자 및 현재 상태 표시 (상단 요약) ---
    st.markdown(f"### 📍 현재 시간 근무 현황 ({now.strftime('%H:%M')})")
    cur = next((r for r in BASE_PATTERN if r["시간"] == current_hour), None)
    
    if cur and selected_date == now.date():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='status-box'><span class='worker-name'>황재업(조):</span> {cur['조']}<br><span class='worker-name'>{w_h}(회관):</span> {cur['회']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='status-box'><span class='worker-name'>{w_a}(의산A):</span> {cur['A']}<br><span class='worker-name'>{w_b}(의산B):</span> {cur['B']}</div>", unsafe_allow_html=True)

    # --- 6. 하단 근무 테이블 ---
    st.markdown("### 🗓️ 전체 시간표")
    display_df = []
    for r in BASE_PATTERN:
        display_df.append({
            "시간": r["표시"],
            "황재업(조)": r["조"],
            f"{w_h}(회)": r["회"],
            f"{w_a}(A)": r["A"],
            f"{w_b}(B)": r["B"]
        })
    df = pd.DataFrame(display_df)

    def apply_style(row):
        is_now = (int(row['시간'].split(':')[0]) == current_hour) and (selected_date == now.date())
        styles = []
        for val in row:
            bg, text, weight, border = "transparent", "black", "normal", "none"
            v = str(val)
            if '순찰' in v: bg = "#E3F2FD"; text = "#1565C0"; weight = "bold"
            elif '휴' in v or '취침' in v: bg = "#F5F5F5"; text = "#757575"
            elif '식' in v: bg = "#FFF3E0"; text = "#E65100"; weight = "bold"
            elif '로비' in v: text = "#D32F2F"; weight = "bold"
            
            if is_now: bg = "#FFF9C4"; border = "1.2px solid red"; weight = "bold"
            styles.append(f'background-color: {bg}; color: {text}; font-weight: {weight}; border: {border};')
        return styles

    st.table(df.style.apply(apply_style, axis=1))
    st.caption("🎨 범례: 🔵순찰 | 🟠식사 | ⚪휴게/취침 | 🔴로비강조")

else:
    st.warning(f"⚠️ {selected_date}은 C조 근무일이 아닙니다.")
