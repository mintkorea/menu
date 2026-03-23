import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 정밀 대조 데이터 (수정본 100% 반영) ---
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

st.set_page_config(layout="centered")

# --- 3. 모바일 최적화 및 색상 CSS ---
st.markdown("""
    <style>
    html, body, [data-testid="stTable"] { font-size: 9px !important; }
    table { width: 100% !important; table-layout: fixed !important; }
    th, td { padding: 3px 1px !important; text-align: center !important; border: 1px solid #f0f0f0; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 로직 처리 ---
now = datetime.now()
current_hour = now.hour
selected_date = st.date_input("📅 날짜", now.date())

days_diff = (selected_date - START_DATE).days

if days_diff % 3 == 0:
    shift = (days_diff // 3) % 3
    lineup = [WORKERS[(0+shift)%3], WORKERS[(1+shift)%3], WORKERS[(2+shift)%3]]
    w_h, w_a, w_b = lineup[0], lineup[1], lineup[2]

    st.subheader(f"✅ {selected_date.strftime('%m/%d')} C조 순번")
    
    # 데이터 재구성
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

    # --- 색상 및 강조 스타일 함수 ---
    def apply_style(row):
        is_now = (int(row['시간'].split(':')[0]) == current_hour) and (selected_date == now.date())
        styles = []
        for val in row:
            bg_color = "transparent"
            text_color = "black"
            font_weight = "normal"
            border = "none"

            # 1. 업무별 배경색 지정
            v = str(val)
            if '순찰' in v:
                bg_color = "#E3F2FD"; text_color = "#1565C0"; font_weight = "bold" # 파란색
            elif '휴게' in v or '휴' in v:
                bg_color = "#F5F5F5"; text_color = "#757575" # 회색
            elif '중식' in v or '석식' in v or '식' in v:
                bg_color = "#FFF3E0"; text_color = "#E65100"; font_weight = "bold" # 주황색
            elif '로비' in v:
                text_color = "#D32F2F"; font_weight = "bold" # 빨간색 글자
            
            # 2. 현재 시간 행 강조 (테두리 및 배경)
            if is_now:
                bg_color = "#FFF9C4" # 연노랑
                border = "1.5px solid red"
                font_weight = "bold"

            styles.append(f'background-color: {bg_color}; color: {text_color}; font-weight: {font_weight}; border: {border};')
        return styles

    st.table(df.style.apply(apply_style, axis=1))

    # 하단 범례 추가
    st.write("🎨 **범례**: 🔵순찰 | 🟠식사 | ⚪휴게 | 🔴로비(강조)")
else:
    st.warning("C조 근무일이 아닙니다.")
